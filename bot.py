import os
import time
import shutil
import mimetypes
import subprocess
import asyncio
import logging
import re
import requests
import tempfile
from threading import Thread
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, MessageNotModified, MessageIdInvalid
from dotenv import load_dotenv
from flask import Flask

# Load environment variables
load_dotenv()
API_ID = int(os.getenv("API_ID", ""))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Initialize Pyrogram client
bot = Client("torrent_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Constants
DOWNLOAD_DIR = "downloads"
MAX_SIZE = 1900 * 1024 * 1024  # 1.9GB Telegram upload limit
BUFFER_SIZE = 10 * 1024 * 1024  # 10MB buffer size for file splitting

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("DirectDownloaderBot")

# Initialize Flask app
flask_app = Flask(__name__)
@flask_app.route('/')
def home():
    return "Bot is running ✅"

# Start Flask server in a separate thread
Thread(target=lambda: flask_app.run(host="0.0.0.0", port=8080), daemon=True).start()

# Utility functions
def human_readable_size(size, decimal_places=2):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"

def time_formatter(seconds):
    seconds = int(seconds)
    if seconds == 0:
        return "0s"
    result = []
    intervals = (("hours", 3600), ("minutes", 60), ("seconds", 1))
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            result.append(f"{value} {name}")
    return " ".join(result)

async def safe_edit_message(message, text, max_retries=2):
    """Safely edit message with flood wait handling"""
    retries = 0
    while retries < max_retries:
        try:
            await message.edit_text(text)
            return True
        except FloodWait as e:
            wait_time = min(e.value, 20)
            logger.warning(f"FloodWait: Waiting {wait_time} seconds...")
            await asyncio.sleep(wait_time)
            retries += 1
        except (MessageNotModified, MessageIdInvalid):
            return True
        except Exception as e:
            logger.error(f"Error editing message: {str(e)}")
            return False
    return False

def split_large_file(file_path, chunk_size=MAX_SIZE):
    """Split large files into chunks under Telegram's size limit"""
    part_num = 1
    output_files = []
    base_name = os.path.basename(file_path)
    
    with open(file_path, 'rb') as f:
        chunk = f.read(chunk_size)
        while chunk:
            part_name = f"{base_name}.part{part_num:03d}"
            part_path = os.path.join(os.path.dirname(file_path), part_name)
            with open(part_path, 'wb') as p:
                p.write(chunk)
            output_files.append(part_path)
            part_num += 1
            chunk = f.read(chunk_size)
    
    return output_files

def clean_directory(directory):
    """Completely remove a directory and its contents"""
    try:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            logger.info(f"✅ Cleaned directory: {directory}")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to clean directory {directory}: {str(e)}")
        return False

# Button layout
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("💧𝙰𝙼_𝙵𝙸𝙻𝙼𝚂💦", url="https://t.me/am_films")]
])

# Start command handler
@bot.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    welcome_image = "https://i.ibb.co/j9n6nZxD/Op-log.png"
    caption = (
        "**🤖 Welcome to Torrent Downloader Bot!**\n\n"
        "📤 Send me a magnet link or .torrent file "
        "and I'll download and upload the content for you!\n\n"
        "💡 **Features:**\n"
        "• Torrent & Magnet Link Support\n"
        "• Automatic Video Detection\n"
        "• Large File Splitting\n"
        "• Automatic File Cleanup\n\n"
        "⚙️ **Max File Size:** 1.9GB (Telegram Limit)\n"
        "🧹 **Auto Cleanup:** Enabled ✅"
    )
    
    try:
        await message.reply_photo(
            photo=welcome_image,
            caption=caption,
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Failed to send welcome image: {e}")
        await message.reply_text(
            text=caption,
            reply_markup=keyboard
        )

# Improved torrent handler with proper download monitoring
@bot.on_message(filters.private & filters.text)
async def torrent_handler(client: Client, message: Message):
    user_id = message.from_user.id
    text = message.text.strip()
    
    # Create temporary working directory
    USER_DIR = os.path.join(DOWNLOAD_DIR, f"user_{user_id}_{int(time.time())}")
    os.makedirs(USER_DIR, exist_ok=True)
    logger.info(f"Created working directory: {USER_DIR}")

    # Ensure cleanup happens regardless of success or failure
    try:
        torrent_file_path = None
        # Handle .torrent URLs by downloading them first
        if re.match(r"^https?://.*\.torrent$", text, re.IGNORECASE):
            try:
                # Download the .torrent file
                response = requests.get(text, headers={'User-Agent': 'Mozilla/5.0'})
                response.raise_for_status()
                
                # Get filename from URL or Content-Disposition
                if "content-disposition" in response.headers:
                    fname = re.findall("filename=(.+)", response.headers["content-disposition"])[0]
                else:
                    fname = text.split("/")[-1].split("?")[0]
                
                # Clean filename
                fname = re.sub(r'[^a-zA-Z0-9\._\-]', '_', fname)
                torrent_file_path = os.path.join(USER_DIR, fname)
                
                with open(torrent_file_path, "wb") as f:
                    f.write(response.content)
                
                text = torrent_file_path
                logger.info(f"Downloaded torrent file: {fname} ({human_readable_size(len(response.content))})")
            except Exception as e:
                logger.error(f"Torrent download failed: {str(e)}")
                await message.reply(f"❌ Failed to download torrent file: {str(e)}")
                return

        # Validate input
        if not (text.startswith("magnet:") or (text.endswith(".torrent") and os.path.exists(text))):
            await message.reply("❌ Invalid torrent or magnet link!")
            return

        msg = await message.reply("🔄 Starting download...")

        try:
            # Enhanced aria2c command
            cmd = [
                "aria2c",
                "--dir=" + USER_DIR,
                "--enable-rpc=true",
                "--rpc-listen-all=true",
                "--rpc-allow-origin-all=true",
                "--seed-time=0",
                "--max-connection-per-server=16",
                "--split=16",
                "--max-concurrent-downloads=5",
                "--check-certificate=false",
                "--auto-file-renaming=true",
                "--allow-overwrite=true",
                "--file-allocation=none",
                "--summary-interval=15",
                text
            ]
            
            logger.info(f"Executing: {' '.join(cmd)}")
            
            # Start the download process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            # Monitor download progress
            start_time = time.time()
            timeout = 1800  # 30 minutes timeout
            last_update = time.time()
            download_completed = False
            output_lines = []
            
            while True:
                # Check if process has completed
                if process.poll() is not None:
                    break
                
                # Check for timeout
                elapsed = time.time() - start_time
                if elapsed > timeout:
                    process.kill()
                    await safe_edit_message(msg, "❌ Download timed out after 30 minutes!")
                    return
                
                # Read output
                line = process.stdout.readline()
                if line:
                    output_lines.append(line.strip())
                    logger.info(f"aria2c: {line.strip()}")
                
                # Update status every 15 seconds
                if time.time() - last_update > 15:
                    # Try to extract progress from output
                    progress = "Downloading..."
                    for line in output_lines[-10:]:
                        if "DL:" in line and "ETA:" in line:
                            progress = line.split("|")[0].strip()
                            break
                    
                    await safe_edit_message(
                        msg, 
                        f"⏳ {progress} ({int(elapsed/60)}m {int(elapsed%60)}s elapsed)"
                    )
                    last_update = time.time()
                
                await asyncio.sleep(1)
            
            # Process completed, check results
            exit_code = process.poll()
            if exit_code != 0:
                # Get last 5 lines of output
                error_output = "\n".join(output_lines[-5:]) or "No output"
                error_msg = f"aria2c exited with code {exit_code}: {error_output}"
                
                # Common error patterns
                if "No URI to download" in error_msg:
                    error_msg = "Invalid magnet/torrent link"
                elif "not found" in error_msg:
                    error_msg = "Torrent file not found"
                elif "unrecognized" in error_msg:
                    error_msg = "Unsupported link format"
                elif "No files found" in error_msg:
                    error_msg = "No downloadable content found in torrent"
                
                await safe_edit_message(msg, f"❌ Download failed: {error_msg}")
                logger.error(f"Download failed: {error_msg}")
                return
            
            # Download completed successfully
            await safe_edit_message(msg, "🔍 Searching for downloaded files...")
            
            # Find downloaded files (excluding temporary files)
            files = []
            for root, _, filenames in os.walk(USER_DIR):
                for filename in filenames:
                    filepath = os.path.join(root, filename)
                    # Skip temporary files and the .torrent file
                    if (
                        not filename.endswith(('.aria2', '.tmp')) and
                        (torrent_file_path is None or filepath != torrent_file_path) and
                        os.path.getsize(filepath) > 0
                    ):
                        files.append(filepath)
            
            if not files:
                await safe_edit_message(msg, "❌ No files found after download. Possible causes:\n"
                                          "- Torrent has no files\n"
                                          "- All files were filtered out\n"
                                          "- Download directory structure issue")
                logger.warning(f"No files found in: {USER_DIR}")
                return

            # Process downloaded files
            for filepath in files:
                filename = os.path.basename(filepath)
                size = os.path.getsize(filepath)
                readable_size = human_readable_size(size)

                # Skip files that are too small (likely incomplete)
                if size < 1024:  # 1KB minimum
                    logger.warning(f"Skipping small file: {filename} ({readable_size})")
                    continue

                if size > MAX_SIZE:
                    await safe_edit_message(msg, f"⚠️ Splitting large file: {filename} ({readable_size})")
                    file_parts = split_large_file(filepath)
                    # Remove original file after splitting
                    os.remove(filepath)
                else:
                    file_parts = [filepath]

                # Upload files/parts
                for part in file_parts:
                    part_name = os.path.basename(part)
                    part_size = os.path.getsize(part)
                    await safe_edit_message(msg, f"📤 Uploading: {part_name} ({human_readable_size(part_size)})")
                    
                    mime, _ = mimetypes.guess_type(part)
                    try:
                        if mime and mime.startswith("video"):
                            await message.reply_video(
                                video=part,
                                caption=f"🎬 `{part_name}`",
                                reply_markup=keyboard,
                                supports_streaming=True,
                                progress=lambda c, t: asyncio.run_coroutine_threadsafe(
                                    safe_edit_message(msg, f"📤 Uploading: {part_name} ({int(c*100/t)}%)"),
                                    bot.loop
                                )
                            )
                        else:
                            await message.reply_document(
                                document=part,
                                caption=f"📦 `{part_name}`",
                                reply_markup=keyboard,
                                progress=lambda c, t: asyncio.run_coroutine_threadsafe(
                                    safe_edit_message(msg, f"📤 Uploading: {part_name} ({int(c*100/t)}%)"),
                                    bot.loop
                                )
                            )
                    except Exception as e:
                        await message.reply(f"❌ Failed to upload {part_name}: {str(e)}")
                    finally:
                        # Clean file immediately after upload attempt
                        if os.path.exists(part):
                            os.remove(part)
                            logger.info(f"🧹 Cleaned file: {part}")

            await msg.delete()
            
        except Exception as e:
            await safe_edit_message(msg, f"❌ Critical error: {str(e)}")
            logger.exception("Torrent processing error:")
            
    finally:
        # Final cleanup of user directory
        clean_directory(USER_DIR)

# Periodic cleanup scheduler
async def cleanup_scheduler():
    """Periodically clean up residual files"""
    while True:
        try:
            # Clean up directories older than 1 hour
            now = time.time()
            for dir_name in os.listdir(DOWNLOAD_DIR):
                dir_path = os.path.join(DOWNLOAD_DIR, dir_name)
                if os.path.isdir(dir_path):
                    dir_age = now - os.path.getmtime(dir_path)
                    if dir_age > 3600:  # 1 hour
                        clean_directory(dir_path)
        except Exception as e:
            logger.error(f"Cleanup scheduler error: {str(e)}")
        
        await asyncio.sleep(3600)  # Run every hour

# Start the bot and scheduler
if __name__ == "__main__":
    logger.info("Starting Torrent Downloader Bot...")
    
    # Create downloads directory if not exists
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    # Start cleanup scheduler in background
    bot.loop.create_task(cleanup_scheduler())
    
    # Run the bot
    bot.run()

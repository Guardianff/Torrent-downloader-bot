# Torrent-downloader-bot
- Version: 1.0.1 🎉

A Telegram bot to fetch and handle torrents, with support for environment configuration.

---

## ⚙️ Environment Variables

Use a `.env` file to configure the following:

---

### ✅ Required Variables

```env
API_ID=1234567890
API_HASH=55089a340f2892fd06aea683cbfb738
BOT_TOKEN=455649:AAG2_RNy07VU_3bZGE
BOT_OWNER_ID=6743860398
```

---

### 🧩 Optional Branding & Customization

#### 🔹 Bot Branding Name & Link  
📝 Change the title shown in messages, headers, and footers.  
✅ Variable: `WD_ZONE_NAME`  
🔗 Link: `WD_ZONE_URL`  

📌 Example:

```env
WD_ZONE_NAME=💧𝐖𝐃 𝐙𝐎𝐍𝐄 ™💦
WD_ZONE_URL=https://t.me/Opleech_WD
```

---

#### 🔹 Developer/Team Credit Line  
👤 Customize who gets credit (e.g., your name/team)  
✅ Variable: `CHANNEL_NAME`  
🔗 Link: `CHANNEL_URL`  

📌 Example:

```env
CHANNEL_NAME=⚡❍⊱❁ 𝐖𝐃 𝐙𝐎𝐍𝐄 ™
CHANNEL_URL=https://t.me/Farooq_is_king
```

---

#### 🔹 Bot Display Image (Optional)  
🖼️ Show your own image in welcome/start messages.  
✅ Variable: `WELCOME_URL`  
✅ Variable: `PHOTO_URL`  

📌 Example:

```env
WELCOME_URL=https://i.ibb.co/j9n6nZxD/Op-log.png
PHOTO_URL=https://i.ibb.co/j9n6nZxD/Op-log.png
```

---
## 📸 Screenshots

<p align="center">
  <img src="https://i.ibb.co/3yVXrs7k/op-torrent.png" alt="start" width="300"/>
  &nbsp;&nbsp;
  <img src="https://graph.org/file/4e8a1172e8ba4b7a0bdfa.jpg" alt="torrent" width="300"/>
</p>
---

## 📢 Channels

- WOODcraft Mirror Zone ™ 🦅: [WD ZONE](https://t.me/Opleech_WD)  
- Support: [WOODcraft](https://t.me/Farooq_is_king)

---

## 🐳 Docker Configuration

- Image: ```docker.io/woodcraftbot/torrent-downloader-bot:latest```
- Port: `8080` (default)

## 🚀 Deployment Options

### 1️⃣ Render (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New+" → "Web Service"
3. Configure:
   • Name: your-bot-name
   • Region: Singapore
   • Runtime: Docker
   • Plan: Free
4. Add environment variables
5. Deploy!

### 2️⃣ Koyeb (Alternative)

1. Sign up at [Koyeb](https://www.koyeb.com/)
2. Create App → "Deploy from Docker"
3. Use image:
   docker.io/woodcraftbot/torrent-downloader-bot:latest
4. Add env variables
5. Deploy

### 3️⃣ Heroku (Legacy)

1. Login to [Heroku](https://heroku.com)
2. New → Create app
3. Deploy → Container Registry
4. Run:
   heroku container:push web -a your-app-name
   heroku container:release web -a your-app-name
5. Set config vars

## 🔍 Verification

1. Check deployment logs
2. Verify bot responds to commands
3. Monitor resource usage


## ⚠️ Troubleshooting

• 400 Errors → Check env variables
• Connection Issues → Verify URLs
• Deployment Failures → Check logs


## 📊 Platform Comparison
| Feature        | Render | Koyeb | Heroku |
|---------------|--------|-------|--------|
| Free Tier     | ✅ Yes | ✅ Yes | ⚠ Limited |
| Docker Support| ✅ Yes | ✅ Yes | ✅ Yes |
| Ease of Use   | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

<div align="center" style="background:#e8f8f5;padding:15px;border-radius:8px;margin:20px 0;">
<h3>🚀 Ready to Deploy!</h3>
<p>Choose your platform and follow the steps above</p>
</div>

<details>
<summary>📌 Pro Tips</summary>

1. Start with Render for easiest setup
2. Monitor your free tier limits
3. Use webhooks for notifications
4. Keep your Docker image updated
</details>

---

## ⚖️ Disclaimer

This bot is intended for educational and archival purposes only.  
We do not host or distribute copyrighted content.

---

# 📜 License

MIT License © [SudoR2spr]  
See the [LICENSE](./LICENSE) file for more info.


# Connect with me <img src="https://media.giphy.com/media/iY8CRBdQXODJSCERIr/giphy.gif" width="30px">
<p align="center">
<a href="https://t.me/Opleech_WD"><img src="https://img.shields.io/badge/-𝐖𝐎𝐎𝐃𝐜𝐫𝐚𝐟𝐭 𝐌𝐢𝐫𝐫𝐨𝐫 𝐙𝐨𝐧𝐞™%20%20-0077B5?style=flat&logo=Telegram&logoColor=white"/></a>
<a href="https://t.me/WD_Topic_Group"><img src="https://img.shields.io/badge/-Wᴅ Tᴏᴘɪᴄ Gʀᴏᴜᴘ%20%20-0077B5?style=flat&logo=Telegram&logoColor=white"/></a>
<a href="https://t.me/WD_Request_Bot"><img src="https://img.shields.io/badge/-𝐖𝐎𝐎𝐃𝐜𝐫𝐚𝐟𝐭,𝐬 𝐁𝐨𝐭%20%20-0077B5?style=flat&logo=Telegram&logoColor=white"/></a>
 <br>
<a href="https://t.me/Opleech"><img title="Telegram" src="https://img.shields.io/static/v1?label=WD.Zone&message=TG&color=blue-green"></a> 
 <br>
<img src="https://media.giphy.com/media/jpVnC65DmYeyRL4LHS/giphy.gif" width="20%"> 
</p>
 
-----
♥️ Credits: [𝐖𝐎𝐎𝐃𝐜𝐫𝐚𝐟𝐭](https://t.me/Farooq_is_KING)

[![Contact Me On Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Farooq_is_king)

<hr>
<h3><img src="https://raw.githubusercontent.com/SudoR2spr/SudoR2spr/main/Premium-icon/clock-time.gif" align="center" width="50"> Last Updated: wed,jun,25,2025</h3>

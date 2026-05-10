<p align="center">
  <img src="https://www.uhdpaper.com/2023/07/genshin-impact-furina-game-4k-161m-original.jpg" alt="Bot Banner" width="100%">
</p>

# 🚀 File-to-Link Bot (Private Version)

# 🚀 File-to-Link Bot (Private Version)

A lightweight Telegram bot designed to convert Telegram files into direct, high-speed download links. These links can be opened in **Google Chrome** or any browser to download files directly to your device without needing the Telegram app.

## 🛠 Features
- **Direct Downloads**: Generates links that work instantly in browsers like Chrome.
- **Personal Use Only**: Clean code with no ads, no shortlinks, and no verification systems.
- **Koyeb Optimized**: Specifically configured to prevent crashes during deployment on Koyeb.
- **Secure**: Uses SSL (HTTPS) for safe file streaming.

---

## ⚙️ Essential Configuration

Add these **Environment Variables** in your Koyeb dashboard to get the bot running:

### 1. The Basics (Required)
| Variable | Description |
| :--- | :--- |
| `API_ID` | Your API ID from my.telegram.org |
| `API_HASH` | Your API Hash from my.telegram.org |
| `BOT_TOKEN` | Your token from @BotFather |
| `DATABASE_URL` | Your MongoDB connection string |
| `BIN_CHANNEL` | A private channel ID (starting with -100) to store files. |

### 2. The Link Settings (Crucial)
| Variable | Value | Description |
| :--- | :--- | :--- |
| `FQDN` | `your-app.koyeb.app` | **CRITICAL:** Paste your actual Koyeb app URL here so Chrome can find the files. |
| `HAS_SSL` | `True` | Ensures your links start with `https://`. |
| `PORT` | `8080` | The internal port for the web server. |

---

## 🚀 Deployment Steps

1. **Fork** this repository to your GitHub account.
2. Log in to **Koyeb** and click **"Create Service"**.
3. Select your GitHub repository.
4. Add the **Environment Variables** listed above.
5. Click **Deploy**.
6. Once deployed, copy the **Public URL** Koyeb gives you and paste it back into the `FQDN` variable in settings.

---

## 👤 Credits & Support
- **Developer**: [Mahabul201](https://github.com/Mahabul29)
- **Support**: [@Hindi_Dub_Animes_Official](https://t.me/Hindi_Dub_Animes_Official)

---
*Note: This bot is for personal use. It has been stripped of all monetization scripts for a faster, cleaner experience.*

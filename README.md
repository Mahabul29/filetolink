# 🚀 File-to-Link Bot (Koyeb Optimized)

A powerful Telegram bot that allows you to download Telegram files directly via your Chrome browser by generating a direct streaming/download link. This version is optimized for personal use, removing all monetization and verification hurdles.

## 🌟 Features
- **Fast Link Generation**: Get direct download links instantly.
- **Chrome Compatible**: Works perfectly with browser download managers.
- **Private Mode**: Only you (the Admin) can generate links.
- **No Monetization**: No shortlinks, no ads, no verification.
- **Koyeb Ready**: Pre-configured to run on Koyeb without crashing.

---

## 🛠 Setup & Environment Variables

To get this bot running, you need to add the following variables to your **Koyeb Service Settings**.

### 🔑 Required (The "Must-Haves")
| Variable | Description |
| :--- | :--- |
| `API_ID` | Your Telegram API ID from [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | Your Telegram API Hash from [my.telegram.org](https://my.telegram.org) |
| `BOT_TOKEN` | Your Bot Token from [@BotFather](https://t.me/BotFather) |
| `DATABASE_URL` | Your MongoDB connection string (Atlas recommended) |
| `BIN_CHANNEL` | A private Telegram channel ID where the bot stores files (e.g., `-100...`) |

### ⚙️ System Configuration (Koyeb Specific)
| Variable | Value | Description |
| :--- | :--- | :--- |
| `FQDN` | `your-app.koyeb.app` | Paste your public Koyeb app URL here. |
| `PORT` | `8080` | The internal port the bot listens on. |
| `NO_PORT` | `True` | Set to True so Koyeb handles the routing. |
| `HAS_SSL` | `True` | Ensures links are generated with `https://`. |

### 🚫 Privacy & Anti-Ads (Set these to False)
| Variable | Value | Description |
| :--- | :--- | :--- |
| `VERIFY` | `False` | Disables the "Earn Money/Verify" requirement. |
| `IS_SHORTLINK` | `False` | Disables all third-party shorteners. |
| `FSUB` | `False` | Disables mandatory channel join requirement. |
| `PUBLIC_FILE_STORE`| `False` | Keeps your file links private to the Admin. |

---

## 🚀 How to Deploy on Koyeb

1. **Fork this Repository** to your GitHub account.
2. **Create a New Service** on Koyeb and select your repository.
3. **Configure the Environment Variables** listed above in the "Environment Variables" section.
4. **Deploy!** Once the status turns to `Healthy`, your bot is live.

---

## 👤 Admin & Support
- **Owner ID**: `5733685945` (Update this in `info.py` or via Vars)
- **Support Group**: [@Hindi_Dub_Animes_Official](https://t.me/Hindi_Dub_Animes_Official)

---

## 📄 License
This project is for educational and personal use. Please use responsibly and do not violate Telegram's Terms of Service.

# Vercel Bot - Telegram Bot Handler

This is the Vercel part of the hybrid bot architecture that handles Telegram connections.

## 🚀 Quick Deployment

### Method 1: GitHub + Vercel (Recommended)

1. **Push this folder to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial Vercel bot deployment"
   git remote add origin https://github.com/yourusername/vercel-bot.git
   git push -u origin main
   ```

2. **Connect to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Sign in with GitHub
   - Click "New Project"
   - Import your GitHub repository
   - Deploy!

### Method 2: Manual Upload

1. **Zip this folder**
2. **Go to Vercel Dashboard**
3. **Click "New Project"**
4. **Upload the zip file**

## 🔧 Environment Variables

Set these in Vercel Dashboard:

```
BOT_TOKEN=your_telegram_bot_token
HF_SPACES_URL=https://your-hf-space.hf.space
MAIN_CHANNEL=-1001111111111
LOG_CHANNEL=-1001111111111
OWNER=123456789
```

## 📋 After Deployment

1. **Get your Vercel URL** (e.g., `https://your-app.vercel.app`)
2. **Set Telegram webhook:**
   ```bash
   curl -X POST "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook" \
   -H "Content-Type: application/json" \
   -d '{"url": "https://your-app.vercel.app/webhook"}'
   ```

## 🔗 Integration

This bot forwards messages to your Hugging Face Spaces API at:
`{HF_SPACES_URL}/api/process_message`

Make sure your HF Spaces has:
- `HF_SPACES_MODE=true` environment variable
- `hf_api.py` file
- Flask in requirements.txt

## 📁 File Structure

```
vercel-bot/
├── api/
│   ├── bot.py          # Bot logic
│   └── index.py        # Vercel handler
├── vercel.json         # Vercel config
├── requirements.txt    # Dependencies
└── README.md          # This file
```

## 🆘 Troubleshooting

- **Webhook not working:** Check Vercel URL and bot token
- **HF Spaces not responding:** Check HF_SPACES_URL and API endpoints
- **Environment variables:** Make sure all are set in Vercel dashboard

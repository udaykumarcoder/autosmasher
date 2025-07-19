# 🚀 Render.com Deployment Guide

## 🎯 What This Does

When someone visits your Render.com URL, the Smash Karts bot will **automatically start running on Render's servers** (not the user's browser). The bot will:

1. **Open Smash Karts** in a headless browser on Render
2. **Auto-join a game** without manual input
3. **Run the movement pattern** automatically
4. **Show real-time status** on the web page

## 📁 Files You Need

Make sure you have these files in your repository:

```
your-repo/
├── server.py              # Main Flask server (NEW!)
├── templates/
│   └── trigger.html       # Web interface (NEW!)
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container configuration
├── render.yaml           # Render configuration
└── README.md            # Documentation
```

## 🚀 Step-by-Step Deployment

### Step 1: Upload to GitHub

1. **Create a new GitHub repository**
2. **Upload all the files** from your project
3. **Make sure `server.py` is the main file** (not the old ones)

### Step 2: Deploy to Render.com

1. **Go to [render.com](https://render.com)** and sign up/login
2. **Click "New +"** → **"Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service:**

   - **Name**: `smash-karts-bot` (or any name you want)
   - **Environment**: `Docker`
   - **Region**: Choose closest to you
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave blank (if files are in root)
   - **Build Command**: Leave blank (Dockerfile handles it)
   - **Start Command**: Leave blank (Dockerfile handles it)

5. **Click "Create Web Service"**

### Step 3: Wait for Deployment

- Render will automatically build your Docker container
- This may take 5-10 minutes on first deployment
- You'll see build logs in real-time

### Step 4: Test Your Bot

1. **Visit your Render URL** (e.g., `https://your-bot-name.onrender.com`)
2. **The bot should start automatically** when you visit the page
3. **Watch the status updates** in real-time
4. **The bot runs on Render's servers**, not your PC!

## 🎮 How It Works

### When Someone Visits Your URL:

1. **Flask server starts** (`server.py`)
2. **Web page loads** (`trigger.html`)
3. **Bot triggers automatically** via JavaScript
4. **Headless Chrome starts** on Render server
5. **Smash Karts loads** and auto-joins game
6. **Movement pattern runs** automatically
7. **Real-time status updates** show on web page

### Key Features:

- **🔄 Auto-trigger**: Bot starts when page is visited
- **🤖 Headless**: Runs without GUI on Render servers
- **📊 Real-time**: Status updates every 2 seconds
- **🎯 Auto-join**: No manual input needed
- **❄️ No PC heat**: Everything runs on Render

## 🔧 Technical Details

### Server Architecture:
```
User visits URL → Flask server → Headless Chrome → Smash Karts → Bot automation
```

### Files Explained:

- **`server.py`**: Main Flask server with bot logic
- **`trigger.html`**: Web interface that auto-triggers bot
- **`Dockerfile`**: Container with Chrome + Xvfb for headless operation
- **`requirements.txt`**: Python dependencies

### Bot Movement Pattern:
1. Forward (5 seconds)
2. Forward + Left (5 seconds)
3. Forward + Right (5 seconds)
4. Jump
5. Backward (5 seconds)
6. Backward + Left (5 seconds)
7. Backward + Right (5 seconds)
8. Jump
9. Repeat

## 🐛 Troubleshooting

### Bot won't start:
- Check Render build logs for errors
- Ensure all files are uploaded to GitHub
- Verify Dockerfile is correct

### Game not loading:
- Check if Smash Karts is accessible
- Look at server logs in Render dashboard
- Try visiting the game URL manually

### Build fails:
- Check `requirements.txt` syntax
- Verify Python version compatibility
- Look at Docker build logs

## 💡 Tips

1. **Free Tier**: Render free tier has usage limits
2. **Sleep Mode**: Free services sleep after 15 minutes of inactivity
3. **First Visit**: May take 30-60 seconds to wake up on free tier
4. **Monitoring**: Check Render dashboard for logs and status

## 🔒 Security Notes

- **Public Access**: Anyone with the URL can trigger the bot
- **No Authentication**: Consider adding login if needed
- **Server Logs**: Check Render dashboard for activity logs

## 🎉 Success!

Once deployed, your bot will:
- **Start automatically** when someone visits the URL
- **Run on Render's servers** (no local resources used)
- **Show real-time status** on the web page
- **Keep your PC cool** while playing Smash Karts!

---

**Your bot is now running in the cloud! 🎮☁️** 
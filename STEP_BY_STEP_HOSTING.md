# 🚀 Step-by-Step Hosting Guide for Smash Karts Bot

## 📋 Prerequisites
- A GitHub account (free)
- A Render.com account (free)
- All your bot files ready

---

## Step 1: Create GitHub Repository

### 1.1 Go to GitHub
1. Open [github.com](https://github.com)
2. Click **"Sign up"** if you don't have an account
3. **Sign in** to your account

### 1.2 Create New Repository
1. Click the **"+"** icon in the top right
2. Select **"New repository"**
3. Fill in the details:
   - **Repository name**: `smash-karts-bot`
   - **Description**: `Smash Karts automation bot hosted on Render`
   - **Visibility**: Choose **Public** or **Private**
   - **DO NOT** check "Add a README file"
4. Click **"Create repository"**

### 1.3 Upload Your Files
1. In your new repository, click **"uploading an existing file"**
2. **Drag and drop** these files from your PC:
   - `server.py` ✅
   - `requirements.txt` ✅
   - `Dockerfile` ✅
   - `render.yaml` ✅
   - `templates/trigger.html` ✅
   - `README.md` ✅
3. Click **"Commit changes"**

**✅ Step 1 Complete! Your files are now on GitHub.**

---

## Step 2: Create Render.com Account

### 2.1 Sign Up for Render
1. Go to [render.com](https://render.com)
2. Click **"Get Started"**
3. Choose **"Sign up with GitHub"** (recommended)
4. **Authorize Render** to access your GitHub account

### 2.2 Complete Setup
1. Fill in your details:
   - **Email**: Your email address
   - **Password**: Create a strong password
2. Click **"Create Account"**

**✅ Step 2 Complete! You now have a Render account.**

---

## Step 3: Deploy Your Bot

### 3.1 Create New Web Service
1. In your Render dashboard, click **"New +"**
2. Select **"Web Service"**

### 3.2 Connect Your Repository
1. Click **"Connect a repository"**
2. Find and select your `smash-karts-bot` repository
3. Click **"Connect"**

### 3.3 Configure Your Service
Fill in these exact settings:

**Basic Settings:**
- **Name**: `smash-karts-bot`
- **Environment**: `Docker`
- **Region**: Choose closest to you (e.g., `Oregon (US West)`)

**Advanced Settings:**
- **Branch**: `main` (or your default branch)
- **Root Directory**: Leave **blank**
- **Build Command**: Leave **blank** (Dockerfile handles this)
- **Start Command**: Leave **blank** (Dockerfile handles this)

**Environment Variables:**
- **No environment variables needed** for this bot
- Leave this section **completely blank**
- Your bot works without any API keys or secrets

### 3.4 Deploy
1. Click **"Create Web Service"**
2. **Wait for deployment** (5-10 minutes)

**✅ Step 3 Complete! Your bot is being deployed.**

---

## Step 4: Monitor Deployment

### 4.1 Watch Build Process
1. You'll see **build logs** in real-time
2. Look for these success messages:
   ```
   ✅ Successfully built image
   ✅ Container started successfully
   ```

### 4.2 Check for Errors
If you see errors, they might be:
- **Missing files**: Make sure all files are uploaded to GitHub
- **Docker issues**: Check if Dockerfile is correct
- **Dependencies**: Check if requirements.txt is valid

### 4.3 Get Your URL
1. Once deployment is complete, you'll see:
   - **Status**: `Live`
   - **URL**: `https://your-bot-name.onrender.com`

**✅ Step 4 Complete! Your bot is live!**

---

## Step 5: Test Your Bot

### 5.1 Visit Your Bot
1. Click on your **Render URL**
2. Or copy and paste it into your browser
3. You should see the **bot dashboard**

### 5.2 Test Auto-Trigger
1. **Refresh the page** or visit the URL
2. The bot should **automatically start**
3. You should see:
   - Status: `starting` → `browser_ready` → `game_loaded` → `running`
   - Cycle count increasing
   - Uptime timer running

### 5.3 Check Logs
1. In Render dashboard, click on your service
2. Go to **"Logs"** tab
3. You should see bot activity logs

**✅ Step 5 Complete! Your bot is working!**

---

## Step 6: Share Your Bot

### 6.1 Get Your Public URL
Your bot URL will be something like:
```
https://smash-karts-bot.onrender.com
```

### 6.2 Share with Others
- **Anyone with the URL** can trigger your bot
- **No login required** (unless you add authentication)
- **Bot runs on Render's servers**, not their PC

### 6.3 Monitor Usage
1. In Render dashboard, check:
   - **Logs** for activity
   - **Metrics** for usage
   - **Status** for uptime

**✅ Step 6 Complete! Your bot is public!**

---

## 🎯 What Happens When Someone Visits Your URL

### The Complete Flow:
1. **User visits** your Render URL
2. **Web page loads** with auto-trigger
3. **Flask server** starts the bot
4. **Headless Chrome** opens on Render
5. **Smash Karts loads** and auto-joins
6. **Bot runs movement pattern**
7. **Real-time status** shows on web page
8. **User watches** the bot play

### Resource Usage:
- **User's PC**: Just web browsing (minimal resources)
- **Render servers**: All the heavy lifting (game + bot)
- **Your PC**: Completely free (no resources used)

---

## 🐛 Troubleshooting

### Bot Won't Start:
1. **Check Render logs** for errors
2. **Verify all files** are uploaded to GitHub
3. **Check Dockerfile** syntax
4. **Restart the service** in Render dashboard

### Game Not Loading:
1. **Check if Smash Karts is accessible**
2. **Look at server logs** in Render
3. **Try visiting** smashkarts.io manually
4. **Check internet connectivity** on Render

### Build Fails:
1. **Check requirements.txt** syntax
2. **Verify Python version** compatibility
3. **Look at Docker build logs**
4. **Check file permissions** in GitHub

### Bot Stops Unexpectedly:
1. **Check Render free tier limits**
2. **Look at memory usage** in logs
3. **Check for errors** in bot logic
4. **Restart the service**

---

## 💡 Pro Tips

### Free Tier Optimization:
1. **Service sleeps** after 15 minutes of inactivity
2. **First visit** may take 30-60 seconds to wake up
3. **Monitor usage** to stay within limits

### Performance Tips:
1. **Use paid tier** for better performance
2. **Monitor logs** regularly
3. **Test thoroughly** before sharing

### Security Notes:
1. **Anyone can trigger** your bot (public access)
2. **Consider adding authentication** if needed
3. **Monitor for abuse** in logs

---

## 🎉 Success Checklist

- ✅ **GitHub repository** created and files uploaded
- ✅ **Render account** created
- ✅ **Web service** deployed successfully
- ✅ **Bot starts** when visiting URL
- ✅ **Game loads** and bot plays
- ✅ **Real-time status** updates working
- ✅ **Public URL** accessible
- ✅ **Logs** showing activity

---

## 🚀 Your Bot is Now Live!

**Your Smash Karts bot is now:**
- 🌐 **Hosted on Render.com**
- 🤖 **Runs automatically** when URL is visited
- ❄️ **Keeps your PC cool**
- 📊 **Shows real-time status**
- 🌍 **Accessible from anywhere**

**Share your URL and let others enjoy your bot!** 🎮☁️

---

**Need help? Check the logs in your Render dashboard or refer to the troubleshooting section above.** 
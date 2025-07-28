# 🚀 Render Deployment Guide

## 📋 Prerequisites

1. **GitHub Account** - Free
2. **Render Account** - Free tier available
3. **Git installed** on your computer

## 🎯 Quick Deployment Steps

### Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: Chemical Industry RSS Monitor API"

# Create GitHub repository and push
git remote add origin https://github.com/YOUR_USERNAME/chemical-rss-monitor.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render

1. **Go to [render.com](https://render.com)** and sign up/login
2. **Click "New +"** → **"Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service:**
   - **Name**: `chemical-rss-monitor`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python production_server.py`
   - **Health Check Path**: `/api/summary`

5. **Click "Create Web Service"**

### Step 3: Get Your Public URL

- Render will automatically deploy your app
- You'll get a URL like: `https://chemical-rss-monitor.onrender.com`
- The API will be available at: `https://chemical-rss-monitor.onrender.com/api/news`

## 🌐 API Endpoints

Once deployed, your API will be available at:

| Endpoint | Description |
|----------|-------------|
| `https://your-app.onrender.com/` | API help page |
| `https://your-app.onrender.com/api/news` | Get all articles |
| `https://your-app.onrender.com/api/news?category=Chemical Pricing` | Filter by category |
| `https://your-app.onrender.com/api/news?source=Economic Times` | Filter by source |
| `https://your-app.onrender.com/api/summary` | Get statistics |
| `https://your-app.onrender.com/api/categories` | Available categories |
| `https://your-app.onrender.com/api/sources` | Available sources |

## 🔧 Testing Your Deployed API

### Using curl:
```bash
# Test the API
curl https://your-app.onrender.com/api/summary

# Get chemical pricing news
curl "https://your-app.onrender.com/api/news?category=Chemical Pricing"
```

### Using Python:
```python
import requests

# Test the API
response = requests.get('https://your-app.onrender.com/api/summary')
print(response.json())

# Get all news
response = requests.get('https://your-app.onrender.com/api/news')
articles = response.json()['articles']
print(f"Found {len(articles)} articles")
```

## ⚙️ Environment Variables

Render will automatically set:
- `PORT`: Port number (usually 10000)
- `DEBUG`: Set to false in production

## 📊 Monitoring

- **Logs**: Available in Render dashboard
- **Health Check**: Automatically monitors `/api/summary`
- **Auto-restart**: Service restarts if it crashes

## 🔄 Updates

To update your deployed API:

```bash
# Make changes to your code
git add .
git commit -m "Update API"
git push origin main

# Render will automatically redeploy
```

## 💰 Costs

- **Free Tier**: 750 hours/month (enough for 24/7 operation)
- **Paid Plans**: Start at $7/month for more resources

## 🛠️ Troubleshooting

### Common Issues:

1. **Build Fails**: Check requirements.txt has all dependencies
2. **Service Won't Start**: Check logs in Render dashboard
3. **API Not Responding**: Verify health check path is correct
4. **Memory Issues**: Upgrade to paid plan for more resources

### Check Logs:
- Go to your service in Render dashboard
- Click "Logs" tab
- Look for error messages

## 🎉 Success!

Once deployed, your Chemical Industry RSS Monitor API will be:
- ✅ **Publicly accessible** via internet
- ✅ **Automatically updated** daily at 09:00 and 18:00 IST
- ✅ **Always available** with health monitoring
- ✅ **Scalable** with Render's infrastructure

Share your API URL with anyone who needs chemical industry news! 
# 🚗 Deploy to Streamlit Cloud - Step by Step

## 📋 Prerequisites
- GitHub account
- Groq API key
- 15 minutes

## 🚀 Quick Deploy Guide

### Step 1: Prepare for GitHub
```bash
# Initialize Git (if not done)
git init
git add .
git commit -m "Initial commit - Zambian Road Traffic AI"
```

### Step 2: Push to GitHub
1. Go to [github.com](https://github.com)
2. Create new repository: `zambian-road-traffic-ai`
3. Push your code:
```bash
git remote add origin https://github.com/yourusername/zambian-road-traffic-ai.git
git push -u origin main
```

### Step 3: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Deploy now"
3. Connect your GitHub repository
4. Set environment variable:
   - Name: `GROQ_API_KEY`
   - Value: `your_actual_groq_key_here`
5. Click "Deploy"

### Step 4: Access Your App
- Your app will be live at: `https://yourusername-zambian-road-traffic-ai.streamlit.app`
- Works on PC, phones, tablets!

## 🔧 Alternative Deploy Options

### Railway ($5/month)
```bash
# Add railway.yaml
web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

### VPS (Full control)
- DigitalOcean ($5/month)
- Vultr ($3.50/month)
- Install nginx + streamlit

## 📱 Mobile Optimization
Your app is already mobile-friendly:
- Responsive design
- Touch-friendly buttons
- Works on all browsers

## 🔐 Security Notes
- Never commit real API key to GitHub
- Use environment variables in production
- Enable authentication if needed

## 🎯 After Deployment
Your app will be accessible worldwide:
- 📱 Mobile phones
- 💻 Desktop PCs  
- 📟 Tablets
- 🌐 Any browser

Users can ask about:
- Driver license requirements
- Traffic fines
- Vehicle registration
- RSTA procedures
- Road safety laws

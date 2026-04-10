#!/usr/bin/env python3
"""
Secure deployment script for Zambian Road Traffic AI Assistant
"""

import os
import streamlit as st
import subprocess
import sys

def check_environment():
    """Check if environment is properly configured"""
    print("Checking deployment environment...")
    
    # Check if API key is set
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        print("❌ ERROR: GROQ_API_KEY not properly set!")
        print("\n📋 To fix this:")
        print("1. Set environment variable: set GROQ_API_KEY=your_actual_key")
        print("2. Or update .env file with your actual key")
        return False
    
    # Check if database exists
    if not os.path.exists("chromadb_storage"):
        print("❌ ERROR: Database not found!")
        print("Run: python ingest_data.py")
        return False
    
    print("✅ Environment check passed!")
    return True

def deploy_local():
    """Deploy on local network"""
    print("\n🚀 Deploying to local network...")
    
    # Get local IP
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"📍 Local IP: {local_ip}")
    print(f"🌐 Access URL: http://{local_ip}:8501")
    
    # Start Streamlit with network access
    cmd = [
        "streamlit", "run", "app.py",
        "--server.address", "0.0.0.0",
        "--server.port", "8501",
        "--server.headless", "true"
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Deployment error: {e}")

def setup_production_env():
    """Setup for production deployment"""
    print("\n🏭 Production Setup Guide:")
    print("=" * 40)
    
    print("\n1. 🔐 Environment Variables:")
    print("   - Set GROQ_API_KEY as environment variable")
    print("   - Never commit .env file to version control")
    
    print("\n2. 🌐 Deployment Options:")
    print("   a) Streamlit Cloud (easiest)")
    print("   b) Railway/Heroku")
    print("   c) VPS with nginx")
    
    print("\n3. 📁 Required Files:")
    print("   - app.py")
    print("   - requirements.txt")
    print("   - chromadb_storage/")
    
    print("\n4. 🚀 Quick Deploy Commands:")
    print("   # For local network:")
    print("   python deploy_secure.py")
    print("   ")
    print("   # For production:")
    print("   streamlit run app.py --server.address 0.0.0.0")

if __name__ == "__main__":
    print("🚗 Zambian Road Traffic AI - Secure Deployment")
    print("=" * 50)
    
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        setup_production_env()
    elif check_environment():
        deploy_local()

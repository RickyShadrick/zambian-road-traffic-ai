#!/usr/bin/env python3
"""
Script to clean the ChromaDB database
"""

import os
import shutil
import time

def clean_database():
    """Remove the ChromaDB storage directory"""
    chroma_path = "chromadb_storage"
    
    if os.path.exists(chroma_path):
        print(f"Removing {chroma_path}...")
        try:
            # Try to remove the directory
            shutil.rmtree(chroma_path)
            print(" Database removed successfully!")
        except Exception as e:
            print(f" Error removing database: {e}")
            print(" Please make sure the Streamlit app is stopped first.")
            return False
    else:
        print(" Database directory does not exist.")
    
    return True

if __name__ == "__main__":
    clean_database()

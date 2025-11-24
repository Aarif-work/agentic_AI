#!/usr/bin/env python3

# Simple test to verify imports and basic functionality
try:
    print("Testing imports...")
    
    import os
    print("[OK] os imported")
    
    import requests
    print("[OK] requests imported")
    
    from bs4 import BeautifulSoup
    print("[OK] BeautifulSoup imported")
    
    from flask import Flask
    print("[OK] Flask imported")
    
    from dotenv import load_dotenv
    print("[OK] dotenv imported")
    
    import google.generativeai as genai
    print("[OK] google.generativeai imported")
    
    print("\nAll imports successful!")
    
    # Test API key loading
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        print(f"[OK] API key loaded (length: {len(api_key)})")
    else:
        print("[ERROR] No API key found")
    
except ImportError as e:
    print(f"[ERROR] Import error: {e}")
except Exception as e:
    print(f"[ERROR] Error: {e}")
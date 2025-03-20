import os
import json
import requests
import datetime
from bs4 import BeautifulSoup

# File to store data between runs
DATA_FILE = "last_check_data.json"

# LinkedIn profile to monitor
PROFILE_URL = "https://www.linkedin.com/in/zieglerr/"

# Keywords to look for
KEYWORDS = ["funding", "investment", "million", "secured", "breaking", "raised"]

def get_previous_data():
    """Load data from previous runs"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"last_check": None, "last_post_title": None}

def save_current_data(data):
    """Save data for future runs"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def fetch_linkedin_activity():
    """Fetch recent activity from the LinkedIn profile"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(PROFILE_URL, headers=headers)
        print(f"LinkedIn response status: {response.status_code}")
        
        # We can't extract much without authentication, but can check if page structure changed
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Use title as a simple way to detect changes
        page_title = soup.title.text.strip() if soup.title else "No title found"
        return page_title
    
    except Exception as e:
        print(f"Error fetching LinkedIn data: {e}")
        return None

def main():
    # Get previous data
    previous_data = get_previous_data()
    
    # Record this check
    current_time = datetime.datetime.now().isoformat()
    
    print(f"Starting LinkedIn check at {current_time}")
    print(f"Previous check: {previous_data['last_check']}")
    
    # Check LinkedIn
    page_title = fetch_linkedin_activity()
    
    # Update data
    current_data = {
        "last_check": current_time,
        "last_post_title": page_title
    }
    
    # Compare with previous data
    if previous_data['last_post_title'] != page_title:
        print("Page title has changed!")
        print(f"Previous: {previous_data['last_post_title']}")
        print(f"Current: {page_title}")
        
        # Check for keywords
        if page_title and any(keyword.lower() in page_title.lower() for keyword in KEYWORDS):
            print("ALERT: Keyword detected in title!")
    else:
        print("No change detected in page title")
    
    # Save current data for next run
    save_current_data(current_data)
    print("Data saved for next run")

if __name__ == "__main__":
    main()

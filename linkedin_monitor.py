import os
import json
import requests
import datetime
import smtplib
from email.mime.text import MIMEText

# File to store data between runs
DATA_FILE = "last_check_data.json"

# Profile to monitor - URL will be used for reference only, not for scraping
PROFILE_URL = "https://www.linkedin.com/in/zieglerr/"
PROFILE_NAME = "Lukas Ziegler"

# Keywords to look for
KEYWORDS = ["funding", "investment", "million", "secured", "breaking", "raised"]

# Email settings (get from environment variables in a real setup)
EMAIL_FROM = os.environ.get('EMAIL_FROM', '')
EMAIL_TO = os.environ.get('EMAIL_TO', '')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))

def get_previous_data():
    """Load data from previous runs"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {
        "last_check": None,
        "last_search_time": None,
        "known_headlines": []
    }

def save_current_data(data):
    """Save data for future runs"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def check_new_funding_announcements(person_name, keywords):
    """
    Check for new funding announcements by searching for the person's name
    plus funding-related keywords
    """
    # Simulate finding news/announcements
    # In a real implementation, you could:
    # 1. Use Google News API
    # 2. Check company press releases
    # 3. Search Twitter for mentions
    
    current_time = datetime.datetime.now().isoformat()
    
    # This is a placeholder - in a real implementation, you'd perform 
    # an actual search for news about the person + funding keywords
    return {
        "search_time": current_time,
        "headlines": [
            # Simulated headlines - in a real implementation, these would come from 
            # your news source or search results
        ]
    }

def send_email_notification(headline, details):
    """Send email notification about new funding announcement"""
    if not all([EMAIL_FROM, EMAIL_TO, EMAIL_PASSWORD]):
        print("Email settings not configured, skipping notification")
        return False
    
    subject = f"New Funding Announcement: {headline}"
    
    body = f"Detected a new funding announcement:\n\n"
    body += f"Headline: {headline}\n\n"
    body += f"Details: {details}\n\n"
    body += f"Person: {PROFILE_NAME}\n"
    body += f"LinkedIn Profile: {PROFILE_URL}\n\n"
    
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print("Email notification sent successfully")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def main():
    # Get previous data
    previous_data = get_previous_data()
    
    # Record this check
    current_time = datetime.datetime.now().isoformat()
    
    print(f"Starting funding announcement check at {current_time}")
    print(f"Previous check: {previous_data['last_check']}")
    
    # Check for new funding announcements
    search_results = check_new_funding_announcements(PROFILE_NAME, KEYWORDS)
    
    # Get new headlines (not in our known list)
    known_headlines = set(previous_data.get('known_headlines', []))
    new_headlines = []
    
    for headline in search_results.get('headlines', []):
        if headline not in known_headlines:
            new_headlines.append(headline)
            # Add to known headlines so we don't notify again
            known_headlines.add(headline)
    
    # Send notifications for new headlines
    for headline in new_headlines:
        print(f"New funding announcement: {headline}")
        send_email_notification(headline, f"Found on {search_results['search_time']}")
    
    # Update data for next run
    current_data = {
        "last_check": current_time,
        "last_search_time": search_results.get('search_time'),
        "known_headlines": list(known_headlines)
    }
    
    # Save current data for next run
    save_current_data(current_data)
    print("Data saved for next run")
    
    # Summary
    if new_headlines:
        print(f"Found {len(new_headlines)} new funding announcements")
    else:
        print("No new funding announcements found")

if __name__ == "__main__":
    main()

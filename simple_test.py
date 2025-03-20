import os
import json
import datetime

# File to store data between runs
DATA_FILE = "last_run_data.json"

def get_previous_data():
    """Load data from previous runs"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return None

def save_current_data(data):
    """Save data for future runs"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# Get data from previous run
previous_data = get_previous_data()

# Create current run data
current_data = {
    "timestamp": datetime.datetime.now().isoformat(),
    "message": "Script executed successfully"
}

# Print information
print(f"Current run: {current_data['timestamp']}")

if previous_data:
    print(f"Previous run: {previous_data['timestamp']}")
else:
    print("This is the first run")

# Save data for next run
save_current_data(current_data)
print("Data saved for next run")

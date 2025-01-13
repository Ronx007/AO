import os
import shutil
import schedule
import time
from datetime import datetime, timedelta
import threading
import argparse

# Path to your JSON file
json_file_path = 'bookings.json'
backup_dir = 'backups'

# Ensure the backup directory exists
os.makedirs(backup_dir, exist_ok=True)

def backup_json():
    """Function to create a backup of the JSON file with a timestamp."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file_name = f'bookings_backup_{timestamp}.json'
    backup_file_path = os.path.join(backup_dir, backup_file_name)
    shutil.copy(json_file_path, backup_file_path)
    print(f"Backup created at {backup_file_path}")
    delete_old_backups()

def delete_old_backups():
    """Function to delete backup files older than 5 minutes."""
    now = datetime.now()
    cutoff = now - timedelta(minutes=2)
    for filename in os.listdir(backup_dir):
        file_path = os.path.join(backup_dir, filename)
        if os.path.isfile(file_path):
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_time < cutoff:
                os.remove(file_path)
                print(f"Deleted old backup: {file_path}")

def run_scheduler(interval):
    """Function to run the scheduler."""
    schedule.every(interval).minutes.do(backup_json)
    while not stop_event.is_set():
        schedule.run_pending()
        time.sleep(1)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Backup JSON file periodically.")
parser.add_argument('interval', type=int, help='Backup interval in minutes')
args = parser.parse_args()

# Create a stop event
stop_event = threading.Event()

# Start the scheduler thread
scheduler_thread = threading.Thread(target=run_scheduler, args=(args.interval,))
scheduler_thread.start()

try:
    # Keep the main thread running to allow scheduler to run
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Stop the scheduler when interrupted
    print("Stopping the backup script...")
    stop_event.set()
    scheduler_thread.join()
    print("Backup script stopped.")

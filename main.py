import time
import os
import json
from parser import get_reels_url
from downloader import yt_dlp_downloader
from identifier import identify_video
from mal import add_to_ptw

CHECKPOINT_FILE = "checkpoint.json"

def save_checkpoint(index):
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump({"last_index": index}, f)

def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            return json.load(f)["last_index"]
    return 0

urls = get_reels_url()
start_index = load_checkpoint()
print(f"Starting from index {start_index}")

for i, url in enumerate(urls[start_index:], start=start_index):
    try:
        file_path = yt_dlp_downloader(url)
        title = identify_video(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists("temp/frame.jpg"):
            os.remove("temp/frame.jpg")
        if title:
            add_to_ptw(title)
        save_checkpoint(i + 1)
        time.sleep(3)
    except Exception as e:
        print(f"Failed for {url}: {e}")
        continue
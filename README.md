# Anime Importer

A CLI tool that automatically identifies anime from your Instagram saved reels and adds them to your MyAnimeList plan-to-watch list.

## How It Works

1. Parses your Instagram data export to extract saved reel URLs
2. Downloads each reel using yt-dlp
3. Extracts a frame from the middle of the video
4. Sends the frame to trace.moe for anime identification
5. Searches MAL for the identified anime
6. Adds it to your plan-to-watch list via the MAL API

## Requirements

- Python 3.10+
- Firefox or Chrome with Instagram logged in
- A MyAnimeList account and API client ID

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/ishanroy12/anime_importer.git
cd anime_importer
```

**2. Create a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install yt-dlp opencv-python requests python-dotenv
```

**4. Create a temp folder**
```bash
mkdir temp
```

## Setup

**1. Get your Instagram data export**
- Go to Instagram → Settings → Your activity → Download your information
- Select JSON format and request your data
- Wait for the email and download the zip
- Extract `saved_collections.json` and place it in the project folder

**2. Get a MAL API client ID**
- Go to myanimelist.net/apiconfig
- Create a new app with app type set to `other`
- Set redirect URL to `http://localhost`
- Copy your client ID

**3. Create a `.env` file**
## Usage

```bash
python main.py
```

On first run, a browser window will open asking you to authorize with MAL. After approving, paste the authorization code from the URL into the terminal.

The script will then process all your saved reels automatically. Progress is saved after each reel so if it stops you can resume by running it again.

## Notes

- Only reels from the first collection are processed — change this in `parser.py` if needed
- Reels that are not anime (manhwa, manga panels etc.) are automatically skipped
- Only matches with 80%+ confidence from trace.moe are added to MAL
- A 3 second delay between requests prevents rate limiting

## Stack

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — video downloading
- [trace.moe](https://trace.moe) — anime identification by image
- [opencv-python](https://opencv.org) — video frame extraction
- [MAL API](https://myanimelist.net/apiconfig) — updating your anime list
- [AniList API](https://anilist.co) — fetching clean anime titles

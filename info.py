# info.py

import os

# Get these from https://my.telegram.org
API_ID = int(os.getenv("API_ID", "123456"))  # Replace with your API ID
API_HASH = os.getenv("API_HASH", "your_api_hash")

# Bot token from @BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

# MongoDB connection URI
MONGO_DB_URI = os.getenv("MONGO_DB_URI", "mongodb+srv://username:password@cluster.mongodb.net/dbname?retryWrites=true&w=majority")

# Your updates channel username (for force subscribe), e.g., "MyChannel"
UPDATES_CHANNEL = os.getenv("UPDATES_CHANNEL", "MyChannel")

# List of Telegram user IDs who are bot admins
AUTH_USERS = list(map(int, os.getenv("AUTH_USERS", "123456789").split()))

# Start pic URL (used in /start message)
START_PIC = os.getenv("START_PIC", "https://te.legra.ph/file/your_start_pic.jpg")

# Bot owner username
BOT_OWNER = os.getenv("BOT_OWNER", "YourUsername")

# Optional - daily limit for free users (in MB)
FREE_USER_LIMIT = int(os.getenv("FREE_USER_LIMIT", 2048))  # 2GB

# Optional - maximum concurrent rename jobs per user
MAX_CONCURRENT_JOBS = int(os.getenv("MAX_CONCURRENT_JOBS", 3))

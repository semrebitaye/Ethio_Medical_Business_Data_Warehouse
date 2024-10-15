# scraping/telegram_scraper.py

import os
import logging
import yaml
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import MessageMediaPhoto

# Ensure logs directory exists
os.makedirs('object_detection/logs', exist_ok=True)

# Set up logging
logging.basicConfig(filename='object_detection/logs/object_detection.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

# Load configuration
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

api_id = config['telegram']['api_id']
api_hash = config['telegram']['api_hash']
phone = config['telegram']['phone']

# Initialize Telegram client
client = TelegramClient('session_name', api_id, api_hash)

async def scrape_channel(channel):
    """
    Scrapes images from a specified Telegram channel.

    Args:
        channel (str): The Telegram channel URL.

    Returns:
        None
    """
    try:
        await client.start(phone)
        logging.info(f'Successfully connected to Telegram for channel: {channel}')
        
        # Get messages from the channel
        messages = await client.get_messages(channel, limit=2000)  # Adjust limit as needed
        
        # Ensure images directory exists
        os.makedirs('object_detection/images', exist_ok=True)
        
        for message in messages:
            if message.media and isinstance(message.media, MessageMediaPhoto):
                image_path = f'object_detection/images/{message.id}.jpg'
                await message.download_media(image_path)
                logging.info(f'Downloaded image {message.id}.jpg from {channel}')
                
        logging.info(f'Successfully scraped images for channel: {channel}')
        
    except SessionPasswordNeededError:
        logging.error('Session password is needed. Please check your credentials and try again.')
    except Exception as e:
        logging.error(f'Error scraping channel {channel}: {str(e)}')

if __name__ == '__main__':    
    image_channels = [
        'https://t.me/Chemed',
        'https://t.me/lobelia4cosmetics'
    ]
    
    with client:
        # Scrape images from specific channels
        for channel in image_channels:
            client.loop.run_until_complete(scrape_channel(channel))
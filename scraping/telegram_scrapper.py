# scraping/telegram_scraper.py

import os
import csv
import logging
import yaml
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import MessageMediaPhoto

# Ensure logs directory exists
os.makedirs('scraping/logs', exist_ok=True)

# Set up logging
logging.basicConfig(filename='scraping/logs/telegram_scraper.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

# Load configuration
with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), 'r') as config_file:
    config = yaml.safe_load(config_file)

api_id = config['telegram']['api_id']
api_hash = config['telegram']['api_hash']
phone = config['telegram']['phone']

# Initialize Telegram client (more descriptive session name)
client = TelegramClient('scraper_session', api_id, api_hash)

async def scrape_channel(channel, collect_images=False):
    """
    Scrapes messages from a specified Telegram channel.

    Args:
        channel (str): The Telegram channel name.
        collect_images (bool): Whether to download images from the messages.

    Returns:
        None
    """
    try:
        await client.start(phone)
        logging.info(f'Successfully connected to Telegram for channel: {channel}')
        
        # Get messages from the channel
        messages = await client.get_messages(channel, limit=100)  # Adjust limit as needed
        
        # Ensure data directories exist
        os.makedirs('scraping/data/raw', exist_ok=True)
        if collect_images:
            os.makedirs('scraping/data/raw/media', exist_ok=True)
        
        csv_filename = f'scraping/data/raw/{channel}.csv'
        with open(csv_filename, mode='w', encoding='utf-8') as file:
            writer = csv.writer(file)
            if collect_images:
                writer.writerow(['message_id', 'date', 'sender_id', 'message', 'media_path'])
            else:
                writer.writerow(['message_id', 'date', 'sender_id', 'message'])
            
            for message in messages:
                media_path = None
                if collect_images and message.media and isinstance(message.media, MessageMediaPhoto):
                    media_path = f'scraping/data/raw/media/{message.id}.jpg'
                    await message.download_media(media_path)
                if collect_images:
                    writer.writerow([message.id, message.date, message.sender_id, message.message, media_path])
                else:
                    writer.writerow([message.id, message.date, message.sender_id, message.message])
                
        logging.info(f'Successfully scraped and saved data for channel: {channel}')
        
    except SessionPasswordNeededError:
        logging.error('Session password is needed. Please check your credentials and try again.')
    except Exception as e:
        logging.error(f'Error scraping channel {channel}: {str(e)}')

if __name__ == '__main__':
    # Use channel names instead of URLs
    channels = [
        'DoctorsET',
        'lobelia4cosmetics',
        'yetenaweg',
        'EAHCI'
    ]
    
    image_channels = [
        'Chemed',
        'lobelia4cosmetics'
    ]
    
    with client:
        # Scrape messages from all channels
        for channel in channels:
            client.loop.run_until_complete(scrape_channel(channel))
        
        # Scrape images from specific channels
        for channel in image_channels:
            client.loop.run_until_complete(scrape_channel(channel, collect_images=True))

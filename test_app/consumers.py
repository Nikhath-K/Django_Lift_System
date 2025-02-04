import json
import os
import time
from channels.generic.websocket import WebsocketConsumer
from concurrent.futures import ThreadPoolExecutor
from test_app.modbus_client import get_lift_data, get_modbus_client
import feedparser

# Path to the static images folder
IMAGE_FOLDER = 'test_app/static/images/'

executor = ThreadPoolExecutor(max_workers=3)

def get_rss_feed():
    """Fetches and returns the latest 5 news items from an RSS feed."""
    rss_url = 'http://rss.cnn.com/rss/edition.rss'
    feed = feedparser.parse(rss_url)
    return [{'title': entry.title, 'link': entry.link} for entry in feed.entries[:5]]

def get_image_list():
    """Fetch all available image filenames from the folder."""
    try:
        images = [img for img in os.listdir(IMAGE_FOLDER) if img.lower().endswith(('.jpg', '.png', '.jpeg'))]
        images.sort()
        return images
    except FileNotFoundError:
        return []

def fetch_modbus_data():
    """Fetch live lift data from Modbus without blocking other updates."""
    port = "COM1"  # Change based on your system
    client = get_modbus_client(port)

    if client:
        modbus_data = get_lift_data(client)
        client.close()
        floor_number = modbus_data['floor_number'][0] if isinstance(modbus_data['floor_number'], list) else 1
        up_value = modbus_data.get('up_arrow', 0)
        down_value = modbus_data.get('down_arrow', 0)
    else:
        floor_number, up_value, down_value = 1, 0, 0

    return {
        'floor_number': floor_number,
        'up': up_value,
        'down': down_value
    }

class LiftDataConsumer(WebsocketConsumer):
    def connect(self):
        """Runs the WebSocket connection."""
        self.accept()
        executor.submit(self.send_updates)

    def send_updates(self):
        """Continuously send lift data and images every second without blocking."""
        while True:
            modbus_result = fetch_modbus_data()
            floor_number = modbus_result['floor_number']
            image_list = get_image_list()

            if image_list:
                image_index = (floor_number - 1) % len(image_list)
                floor_image_path = f'static/images/{image_list[image_index]}'
            else:
                floor_image_path = ''

            direction_image = "static/images/up_arrow.gif" if modbus_result['down'] == 1 else "static/images/down_arrow.gif"
            news_feed = get_rss_feed()

            self.send(text_data=json.dumps({
                'lift_data': modbus_result,
                'floor_image_path': floor_image_path,
                'direction_image': direction_image,
                'rss_feed': news_feed
            }))

            time.sleep(1)  # Non-blocking sleep to keep updates parallel

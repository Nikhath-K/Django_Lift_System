import os
from django.shortcuts import render
import feedparser
import json
from concurrent.futures import ThreadPoolExecutor
from test_app.modbus_client import get_lift_data, get_modbus_client
from django.http import JsonResponse

# Path to the static images folder (adjust this path if necessary)
IMAGE_FOLDER = 'test_app/static/Stock Images/'

def get_rss_feed():
    """Fetch and return the first 5 news items from an RSS feed."""
    rss_url = 'http://rss.cnn.com/rss/edition.rss'
    feed = feedparser.parse(rss_url)
    return [{'title': entry.title, 'link': entry.link} for entry in feed.entries[:5]]

def get_image_list():
    """Return a list of image filenames from the images folder (only image files)."""
    try:
        images = [img for img in os.listdir(IMAGE_FOLDER)
                  if img.lower().endswith(('.jpg', '.jpeg', '.png'))]
        images.sort()  # Optional: sort alphabetically
        return images
    except FileNotFoundError:
        return []

def fetch_modbus_data():
    """Fetch real lift data from the Modbus device."""
    port = "COM3"  # Change this to your actual COM port
    client = get_modbus_client(port)
    # Defaults in case of failure
    floor_number = 1
    up_value = 0
    down_value = 0
    if client:
        modbus_data = get_lift_data(client)
        client.close()
        # Extract the floor number from the list if available
        if modbus_data.get('floor_number') and isinstance(modbus_data['floor_number'], list):
            floor_number = modbus_data['floor_number'][0]
        up_value = modbus_data.get('up_arrow', 0)
        down_value = modbus_data.get('down_arrow', 0)
    return {'floor_number': floor_number, 'up': up_value, 'down': down_value}

def lift_data_api(request):
    """
    API endpoint to fetch the current lift data, floor image, and RSS feed.
    This view runs the Modbus data retrieval and RSS feed fetching in parallel.
    """
    with ThreadPoolExecutor(max_workers=2) as executor:
        # Launch modbus and rss feed calls in parallel
        future_modbus = executor.submit(fetch_modbus_data)
        future_rss = executor.submit(get_rss_feed)

        modbus_result = future_modbus.result()
        rss_feed = future_rss.result()

    # Get the list of images
    image_list = get_image_list()
    floor_number = modbus_result.get('floor_number', 1)
    if image_list:
        # Use the floor number (1-indexed) to select an image. If floor number is higher than
        # the number of images, it will cycle through.
        image_index = (floor_number - 1) % len(image_list)
        selected_image = image_list[image_index]
        floor_image_path = f'static/Stock Images/{selected_image}'
    else:
        # If no images are found, fallback to empty string (or you could choose to display nothing)
        floor_image_path = ''

    # Determine the direction GIF based on the Modbus data, but swap the logic:
    # If up_arrow is 1, then display the down arrow GIF (since the readings are reversed)
    if modbus_result.get('up') == 1:
        direction_image = "static/down_arrow.gif"
    elif modbus_result.get('down') == 1:
        direction_image = "static/up_arrow.gif"
    else:
        direction_image = ""  # Fallback for no direction

    # Compose the JSON response
    data = {
        'lift_data': modbus_result,
        'floor_image_path': floor_image_path,
        'direction_image': direction_image,
        'rss_feed': rss_feed,
        'company_name': "Technologics Global"
    }
    return JsonResponse(data)

def home_view(request):
    """
    Main page that renders the HTML template.
    Data updates will be handled via JavaScript polling the API.
    """
    return render(request, 'test_app/home.html')

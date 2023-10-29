import os
import requests
import xml.etree.ElementTree as ET
import random

# Gelbooru API endpoint
API_URL = "https://gelbooru.com/index.php?page=dapi&s=post&q=index"

# Request user for search tags
search_tags = input("Enter tags for image search: ")

# Request user for the starting page ID
page_id = int(input("Enter the starting page ID: "))

# Read a list of user agents from a file
with open("agent.txt", "r") as agent_file:
    user_agents = agent_file.read().splitlines()

# Track downloaded post IDs
downloaded_ids = set()

while True:

    # Create 'downloaded.txt' if it doesn't exist
    if not os.path.exists("downloaded.txt"):
        open("downloaded.txt", "w").close()

    # Load already downloaded IDs from 'downloaded.txt'
    with open("downloaded.txt", "r") as downloaded_file:
        downloaded_ids.update(downloaded_file.read().splitlines())

    try:
        while True:
            # Choose a random user agent from the list
            headers = {
                'User-Agent': random.choice(user_agents),
            }

            # Make a request to the Gelbooru API with the page ID and custom user agent
            response = requests.get(API_URL, params={'tags': search_tags, 'limit': 100, 'pid': page_id}, headers=headers)

            if response.status_code == 200:
                # Parse the response as XML
                response_xml = ET.fromstring(response.text)
                posts = response_xml.findall("post")  # Use .findall() to get all <post> elements

                if not posts:
                    break  # No more posts to retrieve

                # Create the 'output' directory if it doesn't exist
                if not os.path.exists("output"):
                    os.makedirs("output")

                for post in posts:
                    post_id = post.find("id").text

                    # Check if the post has already been downloaded
                    if post_id in downloaded_ids:
                        print(f"Skipped image {post_id} as it's already downloaded.")
                        continue

                    file_url = post.find("file_url").text
                    tags = post.find("tags").text

                    # Define the file name
                    filename = f"output/{post_id}.jpg"

                    # Download the image, bypassing SSL verification
                    image_response = requests.get(file_url, verify=False, headers=headers)
                    if image_response.status_code == 200:
                        # Save the image with the determined filename
                        with open(filename, "wb") as image_file:
                            image_file.write(image_response.content)

                        # Save tags to a text file with the same name as the image
                        with open(filename.replace(".jpg", ".txt"), "w") as text_file:
                            # Replace spaces with ", " for tags
                            tags = tags.replace(" ", ", ")
                            text_file.write(tags)

                        # Add the post ID to the downloaded set and 'downloaded.txt'
                        downloaded_ids.add(post_id)
                        with open("downloaded.txt", "a") as downloaded_file:
                            downloaded_file.write(post_id + "\n")

                        print(f"Downloaded image {post_id} with tags: {tags}")
                    else:
                        print(f"Failed to download image {post_id}")
            else:
                print("Error connecting to Gelbooru API. Changing user agent and retrying...")
                continue

            # Increment page ID for each new page
            page_id += 1

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e} \n\n\n ---\n\n RESTARTING")

    

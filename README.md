# Gelbooru Downloader

This script allows you to download images from Gelbooru based on specified tags.

## Requirements
- Python 3.x
- `requests` library (`pip install requests`)

## Usage

1. Clone or download the `downloader.py` file.

2. Create a file named `agent.txt` and add a list of user agents that the script will use for requests.

3. Run the `downloader.py` script.

4. Upon execution, the script will prompt you for:
    - Tags for image search
    - Starting page ID for the search

5. The script will continuously download images from Gelbooru based on the provided tags, avoiding duplicates.

6. Images will be saved in the `output` directory with associated tag information.

## Notes
- The script creates a `downloaded.txt` file to keep track of downloaded image IDs, avoiding re-downloading.

- In case of a connection error to the Gelbooru API, the script will attempt to retry using a different user agent.

- If an image fails to download, the script will log the failure.

- If the `output` directory doesn't exist, the script will create it automatically.

- To stop the script, use Ctrl+C to terminate the process.

## Disclaimer
- Respect copyright and usage rights when downloading and using images.

## Troubleshooting
If you encounter issues or errors while using the script, feel free to create an issue or seek help.


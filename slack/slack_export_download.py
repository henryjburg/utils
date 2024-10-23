# slack_export_download.py
# Extract download URLs from exported Slack data

import json
import os
import re
import urllib.request

PARENT_FOLDER = "Brain Development and Disorders Lab Slack export Apr 15 2022 - Sep 16 2024"
FILENAME_PATTERN = re.compile("^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$")

def start():
  parent_dir = os.path.join(os.getcwd(), PARENT_FOLDER)

  # Iterate through each channel's folder
  for subdir, dirs, files in os.walk(parent_dir):
    channel_name = subdir.split("/").pop()
    if channel_name == PARENT_FOLDER:
      continue

    # Iterate through current channel, create download directory
    print("Channel:", channel_name)
    if not os.path.exists(os.path.join(subdir, "files")):
      os.mkdir(os.path.join(subdir, "files"))

    for file in files:
        # Check if filename matches the YYYY-MM-DD.json format
        if (FILENAME_PATTERN.match(file.split(".")[0])):
          print("File:", file)
          data_file_path = os.path.join(subdir, file)

          # Open and read each data file, and check for the "files" key
          with open(data_file_path) as data_file:
            raw_data = json.load(data_file)

            # Iterate over each message in the data file
            for message in raw_data:
              if ("files" in message) and (len(message["files"]) > 0):
                # For each message, check if the "files" key exists
                for message_file in message["files"]:
                  # Iterate over each file and print the "url_private_download" URL
                  if "name" in message_file:
                    file_name = message_file["id"] + "_" + message_file["name"]
                    print("Downloading:", file_name)
                    urllib.request.urlretrieve(message_file["url_private_download"], os.path.join(subdir, "files", file_name))
                  else:
                    print("Skipping:", message_file["id"])

if __name__ == "__main__":
  start()

# slack_export_clean.py
# After downloading, extract the list of users, and generate plaintext files of channel messages


import json
import os
import re
from datetime import datetime


PARENT_FOLDER = "Brain Development and Disorders Lab Slack export Apr 15 2022 - Sep 16 2024"
FILENAME_PATTERN = re.compile("^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$")


def start():
  parent_dir = os.path.join(os.getcwd(), PARENT_FOLDER)

  # Load users and generate user map
  user_file_path = os.path.join(parent_dir, "users.json")
  user_dict = {}
  with open(user_file_path) as user_file:
    raw_user_data = json.load(user_file)

    for user in raw_user_data:
      user_dict[user["id"]] = user["name"]

  # Iterate through each channel's folder
  for subdir, dirs, files in os.walk(parent_dir):
    channel_name = subdir.split("/").pop()
    if channel_name == PARENT_FOLDER or channel_name == "files":
      continue

    # Iterate through current channel, create text output
    print("Channel:", channel_name)
    messages_file_path = os.path.join(subdir, "messages.txt")
    with open(messages_file_path, "w") as messages_file:
      for file in sorted(files):
        # Check if filename matches the YYYY-MM-DD.json format
        if (FILENAME_PATTERN.match(file.split(".")[0])):
            print("File:", file)
            data_file_path = os.path.join(subdir, file)

            # Open and read each data file, and check for the "files" key
            with open(data_file_path) as data_file:
              raw_data = json.load(data_file)

              # Iterate over each message in the data file
              for message in raw_data:
                # Get the user's name from their ID
                try:
                  message_user = user_dict[message["user"]]
                except:
                  message_user = "unknown"

                message_text = str(message["text"])

                # Extract tags and substitute with usernames
                tags_locations = [m.start() for m in re.finditer("\<@(.*?)\>", message_text)]
                if (len(tags_locations) > 0):
                  for user_tags in reversed(tags_locations):
                    try:
                      tagged_user = "@" + user_dict[message_text[user_tags + 2:user_tags + 13]]
                    except:
                      tagged_user = "@unknown"
                    pre_tag = message_text[:user_tags]
                    post_tag = message_text[user_tags + 14:]
                    message_text = pre_tag + tagged_user + post_tag

                # Check for file-only messages
                if message_text == "" and len(message["files"]) > 0:
                  file_names = []
                  for message_file in message["files"]:
                    try:
                      file_names.append(message_file["name"])
                    except:
                      file_names.append("File: " + message_file["id"])
                  message_text = ", ".join(file_names)

                messages_file.write("(" + str(datetime.fromtimestamp(float(message["ts"]))) + ") " + message_user + ":" + " " + message_text + "\n")


if __name__ == "__main__":
  start()

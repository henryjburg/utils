# find_encrypted.py
# Utility to recursively search a directory, and generate lists of Microsoft files that are password protected


import os


PARENT_FOLDER = "/Users/henryburgess/Downloads"


def start():
  print("Searching:", PARENT_FOLDER)
  file_count = 0
  encrypted_file_paths = []

  # Iterate through each channel's folder
  for subdir, dirs, files in os.walk(PARENT_FOLDER):
    for file in sorted(files):
      file_path = os.path.join(subdir, file)
      opened_file = open(file_path, "rb")

      with opened_file:
        # Read the contents of the file and parse directly to a string
        contents = str(opened_file.read())

        # This is a hack to tell if a Microsoft XML-like format file is encrypted
        if "<encryption" in contents and "</encryption>" in contents:
          encrypted_file_paths.append(file_path)

      opened_file.close()
      file_count += 1

      # Update the progress text
      print("Searching... \t\t\t " + str(file_count) + " files", end="\r", flush=True)

  # Generate and print a summary
  print("\nDone.")
  print("Reviewed " + str(file_count) + " files, found " + str(len(encrypted_file_paths)) + " encrypted files.")
  if len(encrypted_file_paths) > 0:
    print("Files:")
    print("\n".join(encrypted_file_paths))


if __name__ == "__main__":
  start()

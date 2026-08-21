'''Open, read, and process the attached data file. Use the attached `junk.txt` file to:
1. Calculate and report the total number of lines in the file.
2. Add a new line at the end of the file containing exactly: `text file nanalyssis`
3. Convert all text in the `junk.txt` file to lowercase.
4. Save the processed file. Share your GitHub repository link here once you have completed the task.'''

# Read the original content and count lines
with open("junk.txt", "r") as file:
    original_content = file.read()

line_count = len(original_content.splitlines())
print(f"Total lines: {line_count}")
print("Content before any changes:")
print(original_content)

# Add a new line at the end of the file
with open("junk.txt", "a") as file:
    file.write("text file nanalyssis\n")

with open("junk.txt", "r") as file:
    content_after_add = file.read()

print("Content after adding the new line:")
print(content_after_add)

# Convert everything to lowercase and save it
with open("junk.txt", "r") as file:
    lower_content = file.read().lower()

with open("junk.txt", "w") as file:
    file.write(lower_content)

with open("junk.txt", "r") as file:
    final_content = file.read()

print("Content after converting to lowercase:")
print(final_content)

import json

# Input JSON file path
input_file_path = r"C:\Users\thaop\Desktop\TikTok_Data_1730873450\user_data_tiktok.json"

# Output text file path (save it to the Desktop)
output_file_path = r"C:\Users\thaop\Desktop\output.txt"

try:
    # Load JSON data from the file with UTF-8 encoding
    with open(input_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Convert JSON to a string
    json_string = json.dumps(data, indent=4)

    # Write JSON string to the specified output file
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(json_string)

    print(f"JSON data has been written to {output_file_path}")
except Exception as e:
    print(f"An error occurred: {e}")
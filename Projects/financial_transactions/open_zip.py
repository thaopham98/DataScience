import zipfile

file_path = "archive.zip" # input file

# def extractingZipFiles(option, archive):
#     if option == 'a': 
#         # print(f'Option is {option}')
#         archive.extractall("data/raw_dir/") 
#     elif option == 's': # ask the user to input which files to extract

# file_names = []
## Verify the file actually exists and check its size/ display all files stored inside the Zip archive
try:
    # size = os.path.getsize(file_path)
    # print(f'File exists, size: {size}')
    with zipfile.ZipFile(file_path, mode = "r") as archive:
        archive.printdir() # displays the list of files stored inside the Zip archive
        # extractingZipFiles(input("Enter an option: "), archive)
        archive.extractall("data/raw_dir/")
except zipfile.BadZipFile as error:
    print(error)
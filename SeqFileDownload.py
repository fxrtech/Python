import time
import requests

# set the base URL and file extension
base_url = "http://example.com/files/file"
file_extension = ".txt"

# set the range of files to download
start_number = 1
end_number = 10

# set the time delay between downloads in seconds (5 minutes = 300 seconds)
time_delay = 300

for i in range(start_number, end_number+1):
    # create the URL for the current file
    current_url = base_url + str(i) + file_extension
    
    # send a request to download the file
    response = requests.get(current_url)
    
    # check if the request was successful
    if response.status_code == 200:
        # write the contents of the file to a local file
        with open("file" + str(i) + file_extension, "wb") as f:
            f.write(response.content)
        print("Downloaded", current_url)
    else:
        print("Failed to download", current_url)
    
    # delay the next download by the specified time
    time.sleep(time_delay)

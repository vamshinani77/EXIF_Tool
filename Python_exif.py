import os
import sys
from PIL import Image
from PIL.ExifTags import GPSTAGS, TAGS


# Helper function
def create_google_maps_url(gps_coords):            
    
    dec_deg_lat = convert_decimal_degrees(float(gps_coords["lat"][0]),  float(gps_coords["lat"][1]), float(gps_coords["lat"][2]), gps_coords["lat_ref"])
   
    dec_deg_lon = convert_decimal_degrees(float(gps_coords["lon"][0]),  float(gps_coords["lon"][1]), float(gps_coords["lon"][2]), gps_coords["lon_ref"])
    return f"https://maps.google.com/?q={dec_deg_lat},{dec_deg_lon}"


# Converting to decimal degrees for latitude and longitude is from degree/minutes/seconds format is the same for latitude and longitude. So we use DRY principles, and create a seperate function.
def convert_decimal_degrees(degree, minutes, seconds, direction):
    decimal_degrees = degree + minutes / 60 + seconds / 3600
    # A value of "S" for South or West will be multiplied by -1
    if direction == "S" or direction == "W":
        decimal_degrees *= -1
    return decimal_degrees
        


while True:
    output_choice = input("How do you want to receive the output:\n\n1 - File\n2 - Terminal\nEnter choice here: ")
    try:
        conv_val = int(output_choice)
        if conv_val == 1:
            
            sys.stdout = open("exif_data.txt", "w")
            break
        elif conv_val == 2:
            
            break
        else:
            print("You entered an incorrect option, please try again.")
    except:
        print("You entered an invalid option, please try again.")



cwd = os.getcwd()

os.chdir(os.path.join(cwd, "images"))

files = os.listdir()


if len(files) == 0:
    print("You don't have have files in the ./images folder.")
    exit()

for file in files:
    
    try:
        
        image = Image.open(file)
        print(f"_______________________________________________________________{file}_______________________________________________________________")
        # The ._getexif() method returns a dictionary. .items() method returns a list of all dictionary keys and values.
        gps_coords = {}
        # We check if exif data are defined for the image. 
        if image._getexif() == None:
            print(f"{file} contains no exif data.")
        # If exif data are defined we can cycle through the tag, and value for the file.
        else:
            for tag, value in image._getexif().items():
                # If you print the tag without running it through the TAGS.get() method you'll get numerical values for every tag. We want the tags in human-readable form. 
                # You can see the tags and the associated decimal number in the exif standard here: https://exiv2.org/tags.html
                tag_name = TAGS.get(tag)
                if tag_name == "GPSInfo":
                    for key, val in value.items():
                        # Print the GPS Data value for every key to the screen.
                        print(f"{GPSTAGS.get(key)} - {val}")
                        # We add Latitude data to the gps_coord dictionary which we initialized in line 110.
                        if GPSTAGS.get(key) == "GPSLatitude":
                            gps_coords["lat"] = val
                        # We add Longitude data to the gps_coord dictionary which we initialized in line 110.
                        elif GPSTAGS.get(key) == "GPSLongitude":
                            gps_coords["lon"] = val
                        # We add Latitude reference data to the gps_coord dictionary which we initialized in line 110.
                        elif GPSTAGS.get(key) == "GPSLatitudeRef":
                            gps_coords["lat_ref"] = val
                        # We add Longitude reference data to the gps_coord dictionary which we initialized in line 110.
                        elif GPSTAGS.get(key) == "GPSLongitudeRef":
                            gps_coords["lon_ref"] = val   
                else:
                    # We print data not related to the GPSInfo.
                    print(f"{tag_name} - {value}")
            # We print the longitudinal and latitudinal data which has been formatted for Google Maps. We only do so if the GPS Coordinates exists. 
            if gps_coords:
                print(create_google_maps_url(gps_coords))
            # Change back to the original working directory.
    except IOError:
        print("File format not supported!")

if output_choice == "1":
    sys.stdout.close()
os.chdir(cwd)

# Facebook Photo Renamer

I recently decided to download all my photos from Facebook. However, my usual renamer program doesn't work because the EXIF data of the Facebook photos is replaced with the date the data package was created.  Facebook puts the metadata in associated with each picture in a JSON file.  

The associated script will read the JSON file and put the appropriate date and time in the EXIF data in the picture file.  Then it will rename the file.  

# How to use

You'll need to download your facebook data file.  Instructions on that should be [here](https://www.facebook.com/help/1701730696756992?helpref=hc_global_nav).  Be sure to download it as a JSON file as the program here reads JSON metadata.  

Extract the zip file and locate the `<ROOT_DIR>/photos_and_videos/` folder.

Modify the program to ensure that `root_folder = "C:/Users/seang/Downloads/"` is changed to `root_folder = <ROOT_DIR>`. (On or around line 96, if I feel like it I'll add an argument parse at some point)  

You should be able to run it as is.  

It _does not_ modify video files or the thumbnail files.  

# Requirements

I built it in Python 3.7.4, the EXIF date created editor can only work on Windows.  

Packages:

    piexif==1.1.3
    pytz==2019.3
    pywin32==225
    tqdm==4.36.1

Well, `tqdm` is optional.  
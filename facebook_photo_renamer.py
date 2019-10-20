import datetime
import json
import os
import win32file

import piexif
import pywintypes
import win32con
from tqdm import tqdm


def changeFileCreationTime(fname, newtime):
    """ From https://stackoverflow.com/questions/4996405/how-do-i-change-the-file-creation-date-of-a-windows-file"""
    wintime = pywintypes.Time(newtime)
    winfile = win32file.CreateFile(
        fname, win32con.GENERIC_WRITE,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None, win32con.OPEN_EXISTING,
        win32con.FILE_ATTRIBUTE_NORMAL, None)

    win32file.SetFileTime(winfile, wintime, None, None)

    winfile.close()


def get_metadata_file(root, album_meta_folder, file):
    try:
        with open(root + album_meta_folder + file) as jsonfile:
            data = json.load(jsonfile)
    except FileNotFoundError or IOError:
        print(f"Could not read {file}")
    else:
        return data


def overwrite_exif(photo, root):
    # with photo as _photo:
    unix_time = photo.get('creation_timestamp')
    normal_time = datetime.datetime.fromtimestamp(unix_time)
    exif_time_string = datetime.datetime.strftime(normal_time, "%Y:%m:%d %H:%M:%S")
    filename = root + photo.get('uri')
    exif_dict = piexif.load(filename)
    exif_ifd = {piexif.ExifIFD.DateTimeOriginal: exif_time_string,
                piexif.ExifIFD.DateTimeDigitized: exif_time_string
                }
    exif_dict["Exif"] = exif_ifd
    exif_bytes = piexif.dump(exif_dict)
    piexif.remove(filename)
    piexif.insert(exif_bytes, filename)
    changeFileCreationTime(filename, unix_time)


def rename_file(idx, photo, root, time_fmt, other_info):
    unix_time = photo.get('creation_timestamp')
    normal_time = datetime.datetime.fromtimestamp(unix_time)
    normal_time_string = datetime.datetime.strftime(normal_time, time_fmt)
    source_file = root + photo.get('uri')
    root, file = os.path.split(source_file)
    name, ext = os.path.splitext(file)
    try:
        renamed_file = f'{root}/{normal_time_string}_{idx}_{other_info}{ext}'
        os.rename(source_file, renamed_file)
    except:
        renamed_file = f'{root}/{normal_time_string}_{idx}{ext}'
        os.rename(source_file, renamed_file)
    pass


def facebook_photo_renamer(root=None, *, time_fmt='%Y_%m_%d_%H%M%S'):
    album_meta_folder = "./photos_and_videos/album/"
    meta_files = os.listdir(root + album_meta_folder)
    for meta_file in meta_files:
        print(f"Working on File : {meta_file}")
        data = get_metadata_file(root, album_meta_folder, meta_file)
        print(f"Working on Album : {data.get('name')}")
        for idx, photo in tqdm(enumerate(data.get('photos', [])),
                               desc=f"processing Files {data.get('name')}",
                               total=len(data.get('photos', []))):

            try:
                overwrite_exif(photo, root)
                rename_file(idx, photo, root, time_fmt, data.get('name').replace(" ", "_"))
            except:
                # if the file doesn't exist anymore...
                pass
            pass


if __name__ == '__main__':
    root_folder = "C:/Users/seang/Downloads/"
    facebook_photo_renamer(root_folder)

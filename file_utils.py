from PIL import Image
from PIL.ExifTags import TAGS

def get_file_info(file):
    im = Image.open(file)
    exif_data = im._getexif()
    # print(im.format, im.size, im.mode)
    # print(im.info)

    if exif_data is not None:
        # Convert EXIF tag IDs to human-readable names
        metadata = {TAGS.get(tag): value for tag, value in exif_data.items()}
        width = metadata['ExifImageWidth']
        height = metadata['ExifImageHeight']

        iso = metadata['ISOSpeedRatings']
        fnumber = metadata['FNumber']
        exposure = metadata['ExposureTime']
        wb = metadata['WhiteBalance']
        focal_length = metadata['FocalLength']
        focal_length_in_35mm = metadata['FocalLengthIn35mmFilm']

        date = metadata['DateTime'][:10]
        time = metadata['DateTime'][11:]
        time_offset = metadata['OffsetTime']

        camera = metadata['Model']
        lens = metadata['LensModel']




        print(width, height, iso, fnumber, exposure, wb, focal_length, focal_length_in_35mm, date, time, time_offset, camera, lens)
        # for tag, value in metadata.items():
        #     pass
        #     print(f"{tag}: {value}")
    else:
        print("No EXIF metadata found.")

# get_file_info(r"C:\Users\matsv\Pictures\AlienWallpaperCool.jpg")

# get_file_info(r"C:\Users\matsv\Pictures\Camera Roll\WIN_20250430_10_42_11_Pro.jpg")

get_file_info(r"F:\School 24-25\s2\Camera&Studio\w2_images\DSC00322.JPG")
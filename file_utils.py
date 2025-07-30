from PIL import Image
from PIL.ExifTags import TAGS
import dbm
from datetime import datetime
import os

EXT_EXTRACTION_LIST = [
    ''
]

def save_file(app, file_list, user):
    saved_files = []
    for file in file_list:
        if file:
            current_time = datetime.now()

            filename = file.filename
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)
            saved_files.append(filename)

            im = Image.open(file)

            exif_data = im._getexif()
            if exif_data is not None:
                save_exif_file_to_db(im, filename, app.config['UPLOAD_FOLDER'], exif_data, user, current_time)

            else:
                im = Image.open(file)
                width, height = im.size

                dbm.add_item(
                    filename=filename,
                    filepath=app.config['UPLOAD_FOLDER'],
                    creator=user,
                    width=width,
                    height=height
                )
    return {'message': 'Files uploaded successfully', 'files': saved_files}

def save_exif_file_to_db(im, filename, filepath, exif_data, user, upload_datetime):
        metadata = {TAGS.get(tag): value for tag, value in exif_data.items()}

        width, height = im.size

        iso = metadata.get('ISOSpeedRatings')
        fnumber = metadata.get('FNumber')
        exposure = metadata.get('ExposureTime')
        wb = metadata.get('WhiteBalance')
        focal_length = metadata.get('FocalLength')
        focal_length_in_35mm = metadata.get('FocalLengthIn35mmFilm')

        create_datetime = metadata.get('DateTime')
        time_offset = metadata.get('OffsetTime')

        camera = metadata.get('Model')
        lens = metadata.get('LensModel')

        for k, v in {
            "iso": iso,
            "shutter": fnumber,
            "exposure": exposure,
            "width": width,
            "height": height,
            "focal_length": focal_length
        }.items():
            print(f"{k} = {v} (type: {type(v)})")

        dbm.add_item(
            filename=filename,
            filepath=filepath,
            creator=user,
            create_datetime=create_datetime,
            upload_datetime=upload_datetime,
            iso=iso,
            shutter=fnumber,
            exposure=exposure,
            width=width,
            height=height,
            focal_length=focal_length
        )
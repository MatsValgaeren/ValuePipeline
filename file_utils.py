from PIL import Image
from PIL.ExifTags import TAGS
import db_manager
from datetime import datetime
import os

IMAGE_EXT_LIST = {
    '.jpg', '.jpeg',
    '.png',
    '.gif',
    '.bmp',
    '.tiff', '.tif',
    '.webp'
}

PROJECTS = {
    'TEST'
}

class IO_Manager():
    def __init__(self):
        self.current_time = datetime.now()


    def save_file(self, app, file_list, user):
        saved_files = []
        for file in file_list:
            self.proj, self.seq, self.shot, self.version = '', None, None, 1
            if file:
                filename = file.filename
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                # file.save(save_path)
                # saved_files.append(filename)

                filename_no_ext, file_extension = os.path.splitext(filename)
                parts = filename_no_ext.split('_')
                if len(parts) > 5 and parts[0] in PROJECTS and parts[1].isdigit() and parts[2].isdigit():
                    self.proj = parts[0]
                    self.seq = parts[1]
                    self.shot = parts[2]
                    self.version = parts[-1][1:]
                print(self.proj ,self.seq)

                if file_extension in IMAGE_EXT_LIST:
                    self.save_image_file(file, filename, file_extension, app.config['UPLOAD_FOLDER'], user)
            return {'message': 'Files uploaded successfully', 'files': saved_files}

    def save_image_file(self, file, filename, file_extension, filepath, user):
            im = Image.open(file)

            exif_data = im._getexif()
            if exif_data is not None:
                self.save_exif_file_to_db(im, filename, file_extension, filepath, exif_data, user)

            else:
                im = Image.open(file)
                width, height = im.size

                db_manager.add_item(
                    filepath=filepath,
                    filename=filename,
                    version=self.version,
                    extension=file_extension,
                    creator=user,
                    width=width,
                    height=height,
                    upload_datetime = self.current_time
                    )


    def save_exif_file_to_db(self, im, filename, file_extension, filepath, exif_data, user):
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

            # for k, v in {
            #     "iso": iso,
            #     "shutter": fnumber,
            #     "exposure": exposure,
            #     "width": width,
            #     "height": height,
            #     "focal_length": focal_length
            # }.items():
            #     print(f"{k} = {v} (type: {type(v)})")

            db_manager.add_item(
                filepath=filepath,
                filename=filename,
                version=self.version,
                extension=file_extension,
                creator=user,
                create_datetime=create_datetime,
                upload_datetime=self.current_time,
                iso=iso,
                shutter=fnumber,
                exposure=exposure,
                width=width,
                height=height,
                focal_length=focal_length,
                project=self.proj,
                sequence=self.seq,
                shot=self.shot
            )
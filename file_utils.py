from PIL import Image
from PIL.ExifTags import TAGS
import db_manager
from datetime import datetime
import os



PROJECTS = {
    'TEST'
}

class IO_Manager():
    def __init__(self):
        self.current_time = datetime.now()

    def get_data(self, upload_folder, file):
        file_data = {}

        filename = str(file)
        print(filename)
        save_path = os.path.join(upload_folder, filename)


        file_data['filename_no_ext'], file_data['file_extension'] = os.path.splitext(filename)
        parts = file_data['filename_no_ext'].split('_')
        if len(parts) > 5 and parts[0] in PROJECTS and parts[1].isdigit() and parts[2].isdigit():
            file_data["proj"] = parts[0]
            file_data["seq"] = parts[1]
            file_data["shot"] = parts[2]
            file_data["version"] = parts[-1][1:]

        return file_data

    def get_process_data(self, file_list, upload_folder):
        files_data = []
        print('file list:', file_list)
        for file in file_list:
            file_data = self.get_data(upload_folder, file)
            files_data.append(file_data)
        return files_data



    def save_image_file(self, file, file_data, filepath, user):
            im = Image.open(file)

            exif_data = im._getexif()
            if exif_data is not None:
                self.save_exif_file_to_db(im, file_data, filepath, exif_data, user)

            else:
                im = Image.open(file)
                width, height = im.size

                db_manager.add_item(
                    filepath=filepath,
                    filename=file_data['filename'],
                    version=file_data['version'],
                    extension=file_data['file_extension'],
                    creator=user,
                    width=width,
                    height=height,
                    upload_datetime = self.current_time
                    )


    def save_exif_file_to_db(self, im, file_data, filepath, exif_data, user):
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
                filename=file_data['filename'],
                version=file_data['version'],
                extension=file_data['file_extension'],
                creator=user,
                create_datetime=create_datetime,
                upload_datetime=self.current_time,
                iso=iso,
                shutter=fnumber,
                exposure=exposure,
                width=width,
                height=height,
                focal_length=focal_length,
                project=file_data['proj'],
                sequence=file_data['seq'],
                shot=file_data['shot']
            )
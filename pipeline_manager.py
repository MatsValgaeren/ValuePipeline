import file_utils
import db_manager
import os
from werkzeug.utils import secure_filename
import subprocess
from redis import Redis
from rq import Queue
from render_tasks import render_file
redis_conn = Redis()
q = Queue('render', connection=redis_conn)


IMAGE_EXT_LIST = {
    '.jpg', '.jpeg',
    '.png',
    '.gif',
    '.bmp',
    '.tiff', '.tif',
    '.webp'
}
RENDER_EXT_LIST = {
    '.blend'
}

def render_blend(file_path):
    import subprocess
    output_path = file_path.replace(".blend", ".png")
    subprocess.run([
        "blender", "-b", file_path, "-o", output_path, "-f", "1"
    ])
    return f"Rendered: {output_path}"


class WebManager():
    def __init__(self):
        self.io_manager = file_utils.IO_Manager()


    def get_process_info(self, file_list, upload_folder):
        return self.io_manager.get_process_data(file_list, upload_folder)

    def save_file(self, file_list, output_folder, user):
        saved_files = []
        for file in file_list:
            if file:
                file_data = self.io_manager.get_data(file, os.path.join(output_folder, file))
                ext = file_data['file_extension']
                # If file is an image
                if ext in IMAGE_EXT_LIST:
                    self.io_manager.save_image_file(file, file_data, user)
                # if ext in RENDER_EXT_LIST:
                    # if ext == '.blend':
                        # job = q.enqueue(render_file, r"renderer/test.blend")

                        # print(f"Job {job.id} added to queue")
                else:
                    self.io_manager.save_file(file, file_data, user)

            return {'message': 'Files uploaded successfully', 'files': saved_files}

    def render(self, files, output_folder):
        for file in files:
            file_data = self.io_manager.get_data(file, os.path.join(output_folder, file))
            print('file data: ', file_data)
            ext = file_data['file_extension']
            if ext in RENDER_EXT_LIST:
                if ext == '.blend':
                    job = q.enqueue(render_file, file_data['filepath'])

                    print(f"Job {job.id} added to queue")
        
    def render_blend(self, file_path):
        output_path = file_path.replace(".blend", ".png")
        subprocess.run([
            "blender", "-b", file_path, "-o", output_path, "-f", "1"
        ])
        return f"Rendered: {output_path}"

    def process_files(self, files_to_process, processed_files, process_folder, upload_folder):
        base_dir = os.path.abspath(os.path.dirname(__file__))
        abs_process_folder = '/'.join([base_dir, process_folder])
        os.makedirs(abs_process_folder, exist_ok=True)  # Ensure folder exists
        
        files = []
        for file in files_to_process:
            filename = secure_filename(file.filename)
            save_path = os.path.join(abs_process_folder, filename)
            print('save path', save_path)
            file.save(save_path)
            files.append(save_path)


        for item in self.get_process_info(files, process_folder):
            processed_files.append(item)

        return processed_files

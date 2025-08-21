from redis import Redis
from rq import Worker, Queue
import subprocess


def render_file(file_path):
    import subprocess
    output_path = file_path.replace(".blend", ".png")
    blende_loc = "/home/mval/Applications/blender-4.5.2-linux-x64/blender"
    subprocess.run([
        blende_loc, "-b", file_path, "-o", output_path, "-f", "1"
    ])
    return f"Rendered: {output_path}"


if __name__ == "__main__":
    listen = ['render']
    redis_conn = Redis()
    worker = Worker([Queue(name, connection=redis_conn) for name in listen])
    worker.work()


import contextlib
import os
import subprocess
import tempfile
import time

import psutil

import eel


def _eel_server(start_html, html_dir):
    eel.init(html_dir)
    eel.start(start_html, port=0, block=True, mode=None)


@contextlib.contextmanager
def get_eel_server(example_py, start_html):
    """Run an Eel example with the mode/port overridden so that no browser is launched and a random port is assigned"""
    with tempfile.NamedTemporaryFile(mode='w', dir=os.path.dirname(example_py)) as test:
        test.write(f"""
import eel
eel._start_args['mode'] = None
eel._start_args['port'] = 0

import {os.path.splitext(os.path.basename(example_py))[0]}
""")
        test.flush()

        proc = subprocess.Popen(['python', test.name], cwd=os.path.dirname(example_py))

        psutil_proc = psutil.Process(proc.pid)
        while not any(conn.status == 'LISTEN' for conn in psutil_proc.connections()):
            time.sleep(0.01)

        conn = next(filter(lambda conn: conn.status == 'LISTEN', psutil_proc.connections()))
        eel_port = conn.laddr.port

        yield f"http://localhost:{eel_port}/{start_html}"

        proc.terminate()

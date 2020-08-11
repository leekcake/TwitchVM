import subprocess
import sys

import streamlink
from streamlink import Streamlink

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Need to provide streamer id.")
        exit(1)

    id = sys.argv[1]
    print(f"Start with streamer: {id}")

    session = Streamlink()
    session.set_plugin_option('twitch', 'low-latency', True)
    streams = streamlink.streams("http://twitch.tv/{0}".format(id))
    stream = streams['best']
    reader = stream.open()

    p = subprocess.Popen(['ffplay', '-x', '1280', '-y', '720', '-probesize', '8192', '-'], stdout=sys.stdout.buffer, stdin=subprocess.PIPE, stderr=sys.stderr.buffer)

    while True:
        readed = reader.read(1024 * 1024)
        p.stdin.write(readed)
import keyboard

import numpy as np
import pyaudio

CHUNK = 2**12
RATE = 48000

p = pyaudio.PyAudio()

info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
idi = int(input(">"))
for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
        print("Output Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
odi = int(input(">"))

stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK, input_device_index = idi)
player = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, output=True, frames_per_buffer=CHUNK, output_device_index = odi)

data = np.zeros((CHUNK, 1))

frozen = False

def freeze():
    global frozen
    frozen = not frozen
    print(f"frozen:{frozen}")

if __name__ == "__main__":
    keyboard.add_hotkey('ctrl+f', freeze, suppress=True, trigger_on_release=True)
    while True:
        if not frozen:
            data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
        player.write(data, CHUNK)
    keyboard.remove_hotkey('ctrl+f')

p.terminate()
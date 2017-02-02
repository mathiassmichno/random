import sounddevice as sd
from scipy.io import wavfile
import numpy as np
from pprint import pprint
import begin

@begin.start(auto_convert=True)
def main(sound_device: 'Sound Device Name' = '',
         channel_map: 'Channel Mapping' = [1,2],
         duration : 'Duration of recording' = 1.,
         out_file: 'Wavfile to save recording in' = 'out.wav',
         blocksize: 'Block size (0 is optimal but may vary)' = 0,
         loops: 'Number of recordings in loop' = 1,
         format: 'dtype of recording' = 'float32'):
    dev = sd.query_devices(sound_device)
    pprint(dev)
    sd.default.device = sound_device
    sd.default.dtype = format
    sd.default.blocksize = blocksize
    print('Starting Recording')
    channel_map = [int(c) for c in channel_map]
    for i in range(loops):
        print('Loop #', i)
        rec = None
        with sd.InputStream(samplerate=int(dev['default_samplerate'])) as s:
            rec, overflow = s.read(int(duration * dev['default_samplerate']))
        # rec = sd.rec(int(duration * dev['default_samplerate']), samplerate=int(dev['default_samplerate']), mapping=channel_map)
        # print('  sd.wait() ->', sd.wait())
        if overflow:
            print('Overflow!')
        for channel in range(rec.shape[1]):
            non_silence = np.where(rec[:,channel] > float(0))[0]
            print('  Ch. {}, initial silence {} samples'.format(channel, non_silence[0]))
        wavfile.write(str(i) + out_file, int(dev['default_samplerate']), rec)

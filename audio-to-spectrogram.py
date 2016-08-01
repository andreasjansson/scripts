# -*- coding: utf-8 -*-

import argparse
import re
import librosa

BEATS_FORMAT = r'^(?P<seconds>[0-9.]+)\s+(?P<beat>[0-9]+)$'
BEATS_REGEX = re.compile(BEATS_FORMAT)

def read_audio_file(filename, sample_rate):
    y, sr = librosa.load(filename)
    y = librosa.resample(y, sr, sample_rate)
    return y

def make_spectrogram(audio, sample_rate, window_length, hop_length, do_hpss, return_cqt, cqt_bins):
    if do_hpss:
        audio = librosa.effects.harmonic(audio)

    if return_cqt:
        return librosa.cqt(
            audio, sr=sample_rate, hop_length=hop_length, n_bins=cqt_bins)
    else:
        return librosa.stft(
            audio, n_fft=window_length, win_length=window_length,
            hop_length=hop_length)

def read_beats(beats_file):
    pass

def beat_align_spectrogram(spectrogram, beats):
    pass

def write_spectrogram(spectrogram, output_file):
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sample-rate', default=11025, type=int, help='Sample rate to downsample/resample to')
    parser.add_argument('-w', '--window', default=2048, type=int, help='Window length in samples. Ignored if --cqt')
    parser.add_argument('-h', '--hop', default=1024, type=int, help='Hop length in samples')
    parser.add_argument('--hpss', type=bool, default=False, help='Harmonic-Percussive Source Separation filtering of the spectrogram')
    parser.add_argument('--cqt', type=bool, default=False, help='Return Constant-Q Transformed spectrogram instead of normal spectrogram')
    parser.add_argument('--cqt-bins', help='CQT bins. Ignored if not --cqt')
    parser.add_argument('-o', '--output-file', default='-', help='Output filename, "-" is stdout')
    parser.add_argument('-b', '--beats-file', required=False, type=file, help='Beats file in /%s/ format' % BEATS_FORMAT)
    parser.add_argument('audio-file', type=file, help='Input audio file')
    args = parser.parse_args()

    audio = read_audio_file(args.audio_file, args.sample_rate)
    spectrogram = make_spectrogram(audio, args.sample_rate, args.window, args.hop, args.hpss, args.cqt, args.cqt_bins)
    if args.beats_file:
        beats = read_beats(args.beats_file)
        spectrogram = beat_align_spectrogram(spectrogram, beats)

    write_spectrogram(spectrogram, args.output_file)
    

if __name__ == '__main__':
    main()

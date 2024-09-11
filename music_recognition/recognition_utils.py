import numpy as np
from collections import Counter
import random

from fingerprint_utils import generate_spectrogram, generate_fingerprints_from_spectrogram
import settings

def add_random_noise(audio_data: np.array, volume_ratio: float) -> np.array:
    """
    Adds random gaussian noise to audio of length `length` at a random index
    """
    if volume_ratio == 0:
        return audio_data
    data = audio_data.astype(np.float64)
    mean_noise_level = np.mean(np.abs(data))
    print(f'Mean noise level: {mean_noise_level}')
    noise = np.random.normal(0, volume_ratio * mean_noise_level, len(data))
    data += noise
    return data, noise

# Find the most common value in the list of matching tracks
def recognise_audio(target_audio_data: np.array, audio_database, sample_rate_hz = 44100) -> str:
    target_spectrogram, target_frequencies = generate_spectrogram(sample_rate_hz=sample_rate_hz, audio_data=target_audio_data)
    target_fingerprints = generate_fingerprints_from_spectrogram(spectrogram=target_spectrogram, frequencies=target_frequencies, sampling_rate_hz=sample_rate_hz)
    timestamps = [(i * settings.HOP_SIZE) / sample_rate_hz for i in range(len(target_fingerprints))]

    matching_tracks = []
    for i, target_fingerprint in enumerate(target_fingerprints):
        timestamp = timestamps[i]
        matches = [row for row in audio_database if row[1] == target_fingerprint]
        track_ids = [row[0] for row in matches]
        offsets = [round((row[2] - timestamp), 4) for row in matches]
        matching_tracks += list(zip(track_ids, offsets))
    if len(matching_tracks) == 0:
        return None, 0
    track_id, count = Counter(matching_tracks).most_common(1)[0]
    track_id = track_id[0]
    confidence = count / len(matching_tracks)
    return track_id, confidence

# For random testing
def truncate_audio_to_seconds_length(audio_data: np.array, seconds: int, sample_rate_hz = 44100) -> np.array:
    """
    Truncates the audio to a random sample of the given number of seconds
    """
    random.seed(42)
    start = random.randint(0, len(audio_data) - int(seconds * sample_rate_hz))
    end = start + int(seconds * sample_rate_hz)
    return audio_data[start:end]
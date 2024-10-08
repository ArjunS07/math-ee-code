WINDOW_SIZE = 4_096
HOP_SIZE = 2_048

FREQUENCY_BUCKETS_FOR_FINGERPRINTS = [(40, 80), (80, 120), (120, 180), (180, 300), (300, 500), (500, 800), (800, 1200), (1200, 1800)]

TRACKS_DATABASE_PATH = "./tracks_database.csv"
FINGERPRINTS_DATABASE_PATH = "./fingerprints_database.csv"

NOISE_LEVELS = [0.0, 0.5, 1.0, 2.5, 5.0, 7.5, 10.0]
CLIP_LENGTHS = [0.1, 0.5, 1, 2.5, 5, 7.5, 10.0]
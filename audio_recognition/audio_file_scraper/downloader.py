import requests
import os
import audio_recognition.settings as settings

# 1. Get an index of all the pages containing audio links
ROOT_ARCHIVE_URL = "http://www.openmusicarchive.org/"
RAW_LINKS_HTML = open("./raw_links.txt").read()
def find_links():
    links = []
    for line in RAW_LINKS_HTML.split("</a>"):
        if '<a href="browse_tag.php?tag=' in line:
            link = line.split('<a href="')[1].split('"')[0]
            links.append((ROOT_ARCHIVE_URL + link))
    return links
LINKS = find_links()
print(f'{LINKS=}')

# 2. Get all the raw download links
AUDIO_DOWNLOAD_LINKS = []
for link in LINKS:
    page = requests.get(link)
    # Find the <main> element
    main = page.text.split('<main class="content')[1].split("</main>")[0]
    for line in main.split("</a>"):
        if '<a href="audio/' in line:
            mp3_url = line.split('<a href="')[1].split('"')[0]
            print(mp3_url)
            mp3_url = ROOT_ARCHIVE_URL + mp3_url
            AUDIO_DOWNLOAD_LINKS.append(mp3_url)
with open("download_links.txt", "w") as f:
    for link in AUDIO_DOWNLOAD_LINKS:
        f.write(link + "\n")

# 3. Download the files from the URLs to a local folder  
directory = "../recordings"
if not os.path.exists(directory):
    os.makedirs(directory)

tracks_database = []

AUDIO_DOWNLOAD_LINKS = open("download_links.txt", "r").read().split("\n")
for download_link in AUDIO_DOWNLOAD_LINKS:
    try:
    
        audio_name = download_link.split("/")[-1].split(".mp3")[0].replace("%20", "_").replace(" ", "_")
        mp3_output_path = r"recordings/" + audio_name + ".mp3"
        wav_output_path = r"recordings/" + audio_name + ".wav"
        if os.path.exists(wav_output_path): continue

        print(f'Downloading {download_link}...')
        mp3 = requests.get(download_link)

        with open(mp3_output_path, "wb") as f:
            f.write(mp3.content)
        os.system(f'ffmpeg -i "{mp3_output_path}" "{wav_output_path}"')
        os.remove(mp3_output_path)
        
        tracks_database.append((audio_name, wav_output_path))
        print(f"Downloaded {audio_name}")
    except Exception as e:
        print(f"Failed to download {download_link}: {e}")
        continue

with open(settings.TRACKS_DATABASE_PATH, 'w') as f:
    for name, path in tracks_database:
        f.write(f"{name},{path}\n")
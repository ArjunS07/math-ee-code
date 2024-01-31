import requests
import os

# 1. Get an index of all the pages containing audio links
ROOT_ARCHIVE_URL = "http://www.openmusicarchive.org/"
RAW_LINKS_HTML = """
<p>
  <a href="browse_tag.php?tag=1920s" class="browselink" style="line-height:120%">1920s</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=1926" class="browselink" style="line-height:120%">1926</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=1927" class="browselink" style="line-height:120%">1927</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=1928" class="browselink" style="line-height:120%">1928</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=1929" class="browselink" style="line-height:120%">1929</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=ATL 2067" class="browselink" style="line-height:120%">ATL 2067</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=Atlanta" class="browselink" style="line-height:120%">Atlanta</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=banjo" class="browselink" style="line-height:120%">banjo</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=Beat" class="browselink" style="line-height:120%">Beat</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=blues" class="browselink" style="line-height:120%">blues</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=british music hall" class="browselink" style="line-height:120%">british music hall</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=Camden, NJ" class="browselink" style="line-height:120%">Camden, NJ</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=charlie poole" class="browselink" style="line-height:120%">charlie poole</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=Chicago" class="browselink" style="line-height:120%">Chicago</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=Clara Smith" class="browselink" style="line-height:120%">Clara Smith</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=cornet" class="browselink" style="line-height:120%">cornet</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=country" class="browselink" style="line-height:120%">country</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=dallas" class="browselink" style="line-height:120%">dallas</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=dance lessons" class="browselink" style="line-height:120%">dance lessons</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=death" class="browselink" style="line-height:120%">death</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=Diamond Disc" class="browselink" style="line-height:120%">Diamond Disc</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=Don't go 'way nobody" class="browselink" style="line-height:120%">Don't go 'way nobody</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=Eddie Lang" class="browselink" style="line-height:120%">Eddie Lang</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=Edison" class="browselink" style="line-height:120%">Edison</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=female vocal" class="browselink" style="line-height:120%">female vocal</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=fiddle" class="browselink" style="line-height:120%">fiddle</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=folk" class="browselink" style="line-height:120%">folk</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=Free-to-air" class="browselink" style="line-height:120%">Free-to-air</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=group" class="browselink" style="line-height:120%">group</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=guitar" class="browselink" style="line-height:120%">guitar</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=happy" class="browselink" style="line-height:120%">happy</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=instrumental" class="browselink" style="line-height:120%">instrumental</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=jazz" class="browselink" style="line-height:120%">jazz</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=Johnny Dodds Trio" class="browselink" style="line-height:120%">Johnny Dodds Trio</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=male vocal" class="browselink" style="line-height:120%">male vocal</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=Memphis" class="browselink" style="line-height:120%">Memphis</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=money" class="browselink" style="line-height:120%">money</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=murder" class="browselink" style="line-height:120%">murder</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=music" class="browselink" style="line-height:120%">music</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=New York" class="browselink" style="line-height:120%">New York</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=Okeh" class="browselink" style="line-height:120%">Okeh</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=parallel anthology" class="browselink" style="line-height:120%">parallel anthology</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=piano" class="browselink" style="line-height:120%">piano</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=Pinetop Smith" class="browselink" style="line-height:120%">Pinetop Smith</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=poop" class="browselink" style="line-height:120%">poop</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=remix" class="browselink" style="line-height:120%">remix</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=solo" class="browselink" style="line-height:120%">solo</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=violin" class="browselink" style="line-height:120%">violin</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=Virginia Liston" class="browselink" style="line-height:120%">Virginia Liston</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=vocal" class="browselink" style="line-height:120%">vocal</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=Vocalion" class="browselink" style="line-height:120%">Vocalion</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=washboard" class="browselink" style="line-height:120%">washboard</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=weird" class="browselink" style="line-height:120%">weird</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=When The Deal Goes Down" class="browselink" style="line-height:120%">When The Deal Goes Down</a> <span style="color:#ccc;">/</span> <a href="browse_tag.php?tag=work" class="browselink" style="line-height:120%">work</a> <span style="color:#ccc;">/</span>                     
                    
              </p>
"""
def find_links():
    links = []
    for line in RAW_LINKS_HTML.split("</a>"):
        if '<a href="browse_tag.php?tag=' in line:
            link = line.split('<a href="')[1].split('"')[0]
            links.append((ROOT_ARCHIVE_URL + link))
    return links
LINKS = find_links()
print(LINKS)

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

# 3. Download the files at the links locally  
directory = "recordings"
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

with open('../music_recognition/tracks_database.csv', 'w') as f:
    for name, path in tracks_database:
        f.write(f"{name},{path}\n")
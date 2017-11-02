import os
import shutil


def load_tags(song):
    """Load an mp3 file and decode it with utf-8 or latin1 encoding. 
    Return a substring containing the Title, Artist and Album tags.
    """
    tags = song.read(128)
    tags = tags.decode("latin-1")

    # check if the file actually has any ID3v2 tags
    if tags.startswith("ID3"):
        return tags
    else:
        print("No ID3v2 tags found")


def sanitize_tag(tag):
    """Remove leftover ASCII control characters"""
    for i in tag:
        for j in range(32):
            if chr(j) == i:
                tag = tag.strip(i)
    return tag


def extract_tags(tags):
    """Return a tuple containing extracted Title, Artist and Album tags from
    the surrounding bytes.
    """

    title = tags[tags.find("TIT2") + 4:tags.find("TPE1")]
    artist = tags[tags.find("TPE1") + 4: tags.find("TALB")]
    album = tags[tags.find("TALB") + 4: tags.find("TYER")]

    return title, artist, album


def create_dirs(title, artist, album):
    songdir = os.path.join(artist, album, title)
    os.makedirs(songdir, exist_ok=True)
    return songdir


def get_songs():
    files = os.listdir()
    songs = []
    for file in files:
        if file.endswith(".mp3"):
            songs.append(file)
    return songs


# with open("03 - Rihanna - Hard.mp3", "rb") as song:
#    tags = load_tags(song)
#    title, artist, album = extract_tags(tags)
#    title = sanitize_tag(title)
#    artist = sanitize_tag(artist)
#    album = sanitize_tag(album)


songs = get_songs()


print(songs)

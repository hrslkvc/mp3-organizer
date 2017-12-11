"""
A bare bones script that organizes all the .mp3 files in the current directory by
creating Artist/Album/ dirs and subdirs. Finally moving the .mp3 files into the
newly created dirs they belong in
"""
import os
import shutil


def get_songs():
    """Return a list containing the filenames of all the .mp3 files in the directory"""
    files = os.listdir()
    songs = []
    for file in files:
        if file.endswith(".mp3"):
            songs.append(file)
    return songs


def load_tags(song):
    """Load an mp3 file and decode it with utf-8 or latin1 encoding.
    Return a substring containing the Title, Artist and Album tags.
    """
    tags = song.read(128)
    tags = tags.decode("latin-1")

    # check if the file actually has any ID3v2 tags
    if tags.startswith("ID3"):
        return tags
    return None


def sanitize_tag(tag):
    """Remove leftover ASCII control characters"""
    for i in tag:
        for j in range(32):
            if chr(j) == i:
                tag = tag.replace(i, "")
    return tag


def extract_tags(tags):
    """Return a tuple containing extracted Title, Artist and Album tags from
    the surrounding bytes.
    """

    title = tags[tags.find("TIT2") + 4:tags.find("TPE1")]
    artist = tags[tags.find("TPE1") + 4: tags.find("TALB")]
    album = tags[tags.find("TALB") + 4: tags.find("TYER")]

    return title, artist, album


def rename_song(file, artist, title):
    """Rename file based on the artist and title arguments. Return the new filename"""

    new_name = "{} - {}.{}".format(artist, title, "mp3")
    os.rename(file, new_name)
    return new_name


def create_dir(artist, album):
    """Construct a path from the artist and album args and create the directories based on them"""
    songdir = os.path.join(artist, album)
    os.makedirs(songdir, exist_ok=True)
    return songdir


def main():
    current_dir = os.getcwd()
    songs = get_songs()

    for song in songs:

        with open(song, "rb") as s:
            tags = load_tags(s)
            if tags is None:
                print("No tags found in {}".format(song))
                continue

            title, artist, album = extract_tags(tags)
            title = sanitize_tag(title)
            artist = sanitize_tag(artist)
            album = sanitize_tag(album)

            print(title, artist, album)

            new_name = rename_song(os.path.join(current_dir, song), artist, title)
            songdir = create_dir(artist, album)
            shutil.move(new_name, songdir)


if __name__ == "__main__":
    main()

"""
A bare bones script that organizes all the .mp3 files in the current directory by
creating Artist/Album/ dirs and subdirs. Finally moving the .mp3 files into the
newly created dirs they belong in
"""
import os
import shutil


def get_songs():
    """
    Get a list of .mp3 files from the current directory

    Returns:
        songs (list): A list of .mp3 filenames


    """
    files = os.listdir()
    songs = []
    for file in files:
        if file.endswith(".mp3"):
            songs.append(file)
    return songs


def load_tags(song):
    """
    Load an mp3 file and decode it with latin1 encoding.

    Args:
        song (file): An mp3 file

    Returns:
         None: if no tags are present
         tags (str): a substring containing the Title, Artist and Album tags.
    """
    tags = song.read(128)
    tags = tags.decode("latin-1")

    # check if the file actually has any ID3v2 tags
    if tags.startswith("ID3"):
        return tags
    else:
        return None


def extract_tags(tags):
    """
    Extract and slice the full tag string into Title, Artist, and Album tags

    Args:
        tags (str): string containing all 3 tags

    Returns:
        (title, artist, album) (tuple): a tuple containing the three split tags

    """

    title = tags[tags.find("TIT2") + 4:tags.find("TPE1")]
    artist = tags[tags.find("TPE1") + 4: tags.find("TALB")]
    album = tags[tags.find("TALB") + 4: tags.find("TYER")]

    return title, artist, album


def sanitize_tag(tag):
    """
    Remove leftover ASCII control characters and null bytes.

    Args:
        tag (str): raw tag string

    Returns:
        tag (str): a cleaned up string
    """
    for i in tag:
        for j in range(32):
            if chr(j) == i:
                tag = tag.replace(i, "")
    return tag


def rename_song(file, artist, title):
    """
    Rename file based on the artist and title arguments.
    Return a new filename after renaming.

    Args:
        file, artist, title (string): strings containing the three tags

    Returns:
        new_name (string): name of the file after renaming

    """

    new_name = "{} - {}.{}".format(artist, title, "mp3")
    os.rename(file, new_name)
    return new_name


def create_dir(artist, album):
    """
    Construct a path from the artist and album args and create the directories based on them

    Args:
        artist, album (string): artist and album tags

    Returns:
        songdir (string): the newly created directory path

    """
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

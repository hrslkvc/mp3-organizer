import os


def load_tags():
    try


os.chdir("/home/haris/Music/Deezloader")

with open("03 - Rihanna - Hard.mp3", "rb") as song:

    tags = song.read(128)
    tags = tags.decode("latin-1")

    title = tags[tags.find("TIT2") + 4:tags.find("TPE1")].strip("\x00\t")

    print(title)
    artist = tags[tags.find("TPE1") + 4: tags.find("TALB")].strip("\x00\t")

    print(artist)
    album = tags[tags.find("TALB") + 4: tags.find("TYER")].strip("\x00\t")

    print(album)


             
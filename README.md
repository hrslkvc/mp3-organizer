# mp3-organizer

A bare-bones script that reads ID3v2 tags of an .mp3 file and based on the extracted info:

1. Renames the .mp3 file to reflect the embedded info (Artist - Title)
2. Creates a new directory for every artist 
3. Creates a new directory for every extracted album tag by that artist
4. Moves all the .mp3 files to their respective directories, based on the Artist/Album/Title.mp3 scheme

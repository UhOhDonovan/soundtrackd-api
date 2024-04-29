from ascii_magic import AsciiArt
from PIL import ImageEnhance

END = "\033[0m"

cover_url = input("Paste an album cover's URL: ")
album_cover = AsciiArt.from_url(cover_url)
string_ver = album_cover.to_ascii(columns=20)
array_ver = string_ver.split("\n")
for i in range(len(array_ver)):
    print(array_ver[i], END + "Option", i)

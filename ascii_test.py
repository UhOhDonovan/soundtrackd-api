from ascii_magic import AsciiArt
from PIL import ImageEnhance

END = "\033[0m"
print("|\33[42m\033[1m Rating: 5 \33[0m|")
test = "the dog went woof"
for char in reversed("woof"):
    test = test.rstrip(char)
print(test)
cover_url = input("Paste an album cover's URL: ")
album_cover = AsciiArt.from_url(cover_url)
string_ver = album_cover.to_ascii(columns=50)
array_ver = string_ver.split("\n")
for i in range(len(array_ver)):
    print(array_ver[i], END + "Option", i)

import requests
import re
import io
from PIL import Image
from PIL import ImageOps

#r = requests.get("https://minionmasters.gamepedia.com/Category:Cards")
r = requests.get("https://minionmasters.gamepedia.com/index.php?title=Category:Cards&pagefrom=Swarmers#mw-pages")

if(r.status_code != 200):
    quit(1)

html = r.text
pattern = re.compile("<li><a href=\"(/[^\"]*)")
cards = []

result = pattern.findall(html)

nameP = re.compile("<meta property=\"og:title\" content=\"([^\"]*)\"/>")
costP = re.compile("title=\"Category:Mana cost: (\\d)")
imageP = re.compile("<meta property=\"og:image\" content=\"([^\"]*)\"")

for n in result:
    cardPage = requests.get("https://minionmasters.gamepedia.com" + n)
    if (r.status_code != 200):
        print("Failed to get page for card:" + n)
        continue

    name = nameP.search(cardPage.text).group(1)
    cost = costP.search(cardPage.text).group(1)
    imagePath = imageP.search(cardPage.text).group(1)
    format = ".jpg" if "jpg" in imagePath else ".png"

    print(name, cost, imagePath, format)

    r = requests.get(imagePath, stream=True)

    if(r.status_code != 200):
        print("Failed to get image for card:" + n)
        continue

    image = Image.open(io.BytesIO(r.content))
    image.thumbnail((107, 138), Image.ANTIALIAS)

    width, height = image.size
    left = 5
    top = height / 4
    right = width - 10
    bottom = height - 50

    image = image.crop((left, top, right, bottom))

    image.save(r'./out/' + name + "#" + cost + format)

    #with open(r'./out/' + name + "#" + cost + "_original" + format, 'wb') as imageFile:
    #   imageFile.write(r.content)

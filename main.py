from PIL import Image
from PIL import ImageOps
import pytesseract
import pyautogui
import keyboard
#import time
from enum import Enum
#from python_imagesearch.imagesearch import *
from methods import *
from random import randint
import os

class GAME_MODE(Enum):
    SOLO = 0,
    TEAM = 1

class STATE(Enum):
    DISABLED = 0,
    IN_MENU = 1,
    SEARCHING_SOLO = 2,
    SEARCHING_TEAM = 3,
    LOADING = 4,
    PLAYING = 5,
    GETTING_REWARDS = 6

# 0 - solo, 1 - team
mode = GAME_MODE.TEAM
currentState = STATE.DISABLED
handCardCost = [0,0,0,0]
mana = 0
manaCondition = 0
checksToRewards = 0

upperLineSpawnPos = [353, 343]
lowerLineSpawnPos = [324, 433]

card1Borders_solo = [530, 740, 660, 880]
card2Borders_solo = [660, 740, 790, 880]
card3Borders_solo = [797, 740, 920, 880]
card4Borders_solo = [920, 740, 1050, 880]

card1Borders_team = [330, 770, 440, 815]
card2Borders_team = [440, 770, 550, 815]
card3Borders_team = [550, 770, 660, 815]
card4Borders_team = [660, 770, 770, 815]

cardNameArea_solo = [433, 473, 433+545, 473+304]
cardNameArea_team = [433, 473, 433+545, 473+304]

# mode: 0 - solo, 1 - team
def getMana(mode) -> int:
    if (mode == GAME_MODE.SOLO):
        region = region_grabber((500, 800, 1100, 1000))
    else:
        region = region_grabber((255, 880, 770, 950))
    n = 10
    for n in range(10, 0, -1):
        pos = imagesearcharea("./resources/" + ("manabar/" if mode == GAME_MODE.SOLO else "team_manabar/") + str(n) + ".png", 0, 0, 0, 0, 0.9 if n == 10 else 0.8, region)
        if (pos[0] != -1):
            return n
    return 0

# mode: 0 - solo, 1 - team
def getCardPlayPos(cardIndex, mode) -> list:
    if (cardIndex == 1):
        return [card1Borders_solo[0]+50, card1Borders_solo[1]+100] if mode == 0 else [card1Borders_team[0]+50, card1Borders_team[1]+100]
    elif (cardIndex == 2):
        return [card2Borders_solo[0]+50, card2Borders_solo[1]+100] if mode == 0 else [card2Borders_team[0]+50, card2Borders_team[1]+100]
    elif (cardIndex == 3):
        return [card3Borders_solo[0]+50, card3Borders_solo[1]+100] if mode == 0 else [card3Borders_team[0]+50, card3Borders_team[1]+100]
    elif (cardIndex == 4):
        return [card4Borders_solo[0]+50, card4Borders_solo[1]+100] if mode == 0 else [card4Borders_team[0]+50, card4Borders_team[1]+100]
    return [-1,-1]

# mode: 0 - solo, 1 - team
def getCardBorders(cardIndex, mode) -> list:
    if (cardIndex == 1):
        return card1Borders_solo if mode == 0 else card1Borders_team
    elif (cardIndex == 2):
        return card2Borders_solo if mode == 0 else card2Borders_team
    elif (cardIndex == 3):
        return card3Borders_solo if mode == 0 else card3Borders_team
    elif (cardIndex == 4):
        return card4Borders_solo if mode == 0 else card4Borders_team
    return [-1,-1,-1,-1]

# cardIndex: sequential index of a card (1–4)
def getManaCostForCard(cardIndex) -> int:
    cardPos = getCardBorders(cardIndex, mode)

    #print("card #" + str(cardIndex) + " pos:", cardPos)

    region = region_grabber((cardPos[0], cardPos[1], cardPos[2], cardPos[3]))
    #print("Region:", region)
    n = 10
    for n in range(10, -1, -1):
        pos = imagesearcharea("./resources/" + ("mana/" if mode == 0 else "tmana/") + str(n) + ".png", 0, 0, 0, 0, 0.8, region)
        if (pos[0] != -1):
            return n
            # pyautogui.click(pos[0]+500, pos[1]+700)
            #print("Card [" + str(cardIndex) + "] cost:", n)
    return -1

def getCardNames(mode) -> list:
    result = ["NULL", "NULL", "NULL", "NULL"]
    cardImages = []


    # Getting a BW inverted screenshots of the area
    pyautogui.moveTo(card1Borders_solo[0] if mode == GAME_MODE.SOLO else card1Borders_team[0] + 50, card1Borders_solo[1] if mode == GAME_MODE.SOLO else card1Borders_team[1] + 100)
    cardImages.append(ImageOps.invert(region_grabber(cardNameArea_solo if mode == GAME_MODE.SOLO else cardNameArea_team).convert("L")))

    pyautogui.moveTo(card2Borders_solo[0] if mode == GAME_MODE.SOLO else card2Borders_team[0] + 50, card2Borders_solo[1] if mode == GAME_MODE.SOLO else card2Borders_team[1] + 100)
    cardImages.append(ImageOps.invert(region_grabber(cardNameArea_solo if mode == GAME_MODE.SOLO else cardNameArea_team).convert("L")))

    pyautogui.moveTo(card3Borders_solo[0] if mode == GAME_MODE.SOLO else card3Borders_team[0] + 50, card3Borders_solo[1] if mode == GAME_MODE.SOLO else card3Borders_team[1] + 100)
    cardImages.append(ImageOps.invert(region_grabber(cardNameArea_solo if mode == GAME_MODE.SOLO else cardNameArea_team).convert("L")))

    pyautogui.moveTo(card4Borders_solo[0] if mode == GAME_MODE.SOLO else card4Borders_team[0] + 50, card4Borders_solo[1] if mode == GAME_MODE.SOLO else card4Borders_team[1] + 100)
    cardImages.append(ImageOps.invert(region_grabber(cardNameArea_solo if mode == GAME_MODE.SOLO else cardNameArea_team).convert("L")))

    start_time = time.time()

    for i in range(0, 4, +1):
        ocrWords = pytesseract.image_to_string(cardImages[i]).split("\n", 2)
        print("Card #" + str(i+1) + " OCR:", ocrWords)
        result[i] = ocrWords[0]

    print("image_to_string execution time: ", time.time() - start_time, "s")

    return result

def getCardNamesFromImages(mode) -> list:
    region1 = region_grabber(card1Borders_solo)
    region2 = region_grabber(card2Borders_solo)
    region3 = region_grabber(card3Borders_solo)
    region4 = region_grabber(card4Borders_solo)

    #print(region1)

    result = ["NULL", "NULL", "NULL", "NULL"]

    for filename in os.listdir("./resources/cards"):
        fullFilename = "./resources/cards/" + filename

        #print(fullFilename)

        if(result[0] == "NULL"):
            res = imagesearcharea(fullFilename, 0, 0, 0, 0, 0.7, region1)
            if(res[0] != -1):
                result[0] = filename

        if (result[1] == "NULL"):
            res = imagesearcharea(fullFilename, 0, 0, 0, 0, 0.7, region2)
            if (res[0] != -1):
                result[1] = filename

        if (result[2] == "NULL"):
            res = imagesearcharea(fullFilename, 0, 0, 0, 0, 0.7, region3)
            if (res[0] != -1):
                result[2] = filename

        if (result[3] == "NULL"):
            res = imagesearcharea(fullFilename, 0, 0, 0, 0, 0.7, region4)
            if (res[0] != -1):
                result[3] = filename

    print(result)
    return result

    img = Image.open("./resources/ls.png")
    img.thumbnail((107, 138), Image.ANTIALIAS)
    img.save("./resources/ls-small.png")

    result[0] = imagesearcharea("./resources/ls-small.png", 0, 0, 0, 0, 0.9, region1)[0] != -1
    result[1] = imagesearcharea("./resources/ls-small.png", 0, 0, 0, 0, 0.9, region2)[0] != -1
    result[2] = imagesearcharea("./resources/ls-small.png", 0, 0, 0, 0, 0.9, region3)[0] != -1
    result[3] = imagesearcharea("./resources/ls-small.png", 0, 0, 0, 0, 0.9, region4)[0] != -1

    print(result)

    return result

for i in range(0,10,+1):
    print("\n")

print("Current state:", currentState)

# Main logic
while True:
    if keyboard.is_pressed("g"):
        quit(0)

    #cardNames = getCardNames(mode)
    #print(cardNames)
    #getCardNamesFromImages(mode)
    #continue

    # Enabling/disabling the bot
    if keyboard.is_pressed("F4"):
        currentState = STATE.IN_MENU if currentState != STATE.IN_MENU else STATE.PLAYING
        print("Current state:", currentState)
        time.sleep(0.2)

    if currentState == STATE.DISABLED:
        continue

    elif currentState == STATE.IN_MENU:
        if mode == GAME_MODE.TEAM and imageSearchAndClick("./resources/team-battle-start.png", 0.8):
            currentState = STATE.SEARCHING_TEAM
            print("Current state:", currentState)
        elif mode == GAME_MODE.SOLO and imageSearchAndClick("./resources/battle.png", 0.8):
            currentState = STATE.SEARCHING_SOLO
            print("Current state:", currentState)
        else:
            #currentState = STATE.GETTING_REWARDS
            print("Current state:", currentState)

    elif currentState == STATE.SEARCHING_SOLO or currentState == STATE.SEARCHING_TEAM:
        if imagesearch("./resources/loading.png", 0.8)[0] != -1:
            currentState = STATE.LOADING
            print("Current state:", currentState)

    elif currentState == STATE.LOADING:
        if (getMana(mode) > 0):
            currentState = STATE.PLAYING
            print("Current state:", currentState)

    elif currentState == STATE.PLAYING:
        # obtaining mana
        mana = getMana(mode)

        # obtaining card mana costs
        for i in range (0, 4):
            handCardCost[i] = getManaCostForCard(i+1)
        print("[",handCardCost[0]," ",handCardCost[1]," ",handCardCost[2]," ",handCardCost[3],"]")
        print("Mana: " + str(mana) + "/10")

        # TODO: obtaining card names

        if (manaCondition not in handCardCost):
            manaCondition = 0

        # playing random card with the highest cost
        if (mana >= manaCondition):
            indexesToPlay = []
            lastMaxCost = manaCondition

            for i in range(0,4):
                if(handCardCost[i] > -1 and handCardCost[i] >= lastMaxCost and mana >= handCardCost[i]):
                    lastMaxCost = handCardCost[i]
                    indexesToPlay.append(i)

            if(indexesToPlay):
                # 25% chance not to play any of the available 1+ cards and wait for the most expensive card instead
                if (manaCondition == 0 and len(indexesToPlay) < 4 and handCardCost[indexesToPlay[0]] > 0 and randint(1,100) <= 25):
                        manaCondition = max(handCardCost)
                        print("Set manaCondition to", manaCondition)
                else:
                    randomIndexToPlay = random.choice(indexesToPlay)

                    print("lastMaxCost: ", lastMaxCost)
                    print("indexesToPlay: ", indexesToPlay)
                    print("randomIndexToPlay: ", randomIndexToPlay)

                    cardPos = getCardPlayPos(randomIndexToPlay+1, mode)
                    pyautogui.moveTo(cardPos[0], cardPos[1], 0.2)
                    pyautogui.click()
                    linePos = random.choice([upperLineSpawnPos, lowerLineSpawnPos])
                    linePos[0] += randint(0,2)
                    linePos[1] += randint(0, 2)
                    print("Playing card #" + str(randomIndexToPlay + 1) + " at", linePos)
                    pyautogui.moveTo(linePos[0], linePos[1], 0.1)
                    pyautogui.click()
                    manaCondition = 0

        # checking if the screen is blocked because of the chest
        if(mana == 0):
            checksToRewards += 0 #1
        else:
            checksToRewards = 0

        if(checksToRewards == 4):
            currentState = STATE.GETTING_REWARDS
            print("Current state:", currentState)
        else:
            #print("Sleeping...")
            time.sleep(0.8)

    elif currentState == STATE.GETTING_REWARDS:
        pos = imagesearcharea("./resources/close.png", 500, 670, 1100, 890, 0.95)

        if (pos[0] == -1):
            pos = imagesearcharea("./resources/back.png", 500, 670, 1100, 890, 0.95)

        if (pos[0] == -1):
            pos = imagesearcharea("./resources/continue.png", 500, 670, 1100, 890, 0.95)

        if pos[0] != -1:
            pyautogui.moveTo(pos[0] + 500, pos[1] + 670)
            pyautogui.click()
        else:
            pyautogui.moveTo(580, 525)
            pyautogui.click()
            print("Clicked at reward area")

        currentState = STATE.IN_MENU
        print("Current state:", currentState)




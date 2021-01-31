# - TO-DO: Add stages.py
# - TO-DO: Add config.py
from PIL import Image
import aubio
import pygame
import pyaudio
import numpy as np
import glob

from stages import *
from config import *

# Mouth region (x, y, w, h)
REGION_MOUTH = (260, 370, 470, 210)

stage = BLANK

screen = None
avatars, outfits, animations = None, None, None
outfit_current = None

# Get image size to make canvas fit image
img_size = 0, 0
with Image.open(glob.glob(f"{PATH_AVATARS}/*.png")[0]) as img:
    img_size = img.size

# Setup Volume
def vtuberSetupVolume():
    pass

# Load Avatars
def vtuberLoadAvatars():
    avatars = []

    for image in glob.glob(f"{PATH_AVATARS}/*.png"):
        avatars.append(pygame.image.load(image))

    return avatars

# Load Outfits
# - TO-DO: Add outfit names
# - TO-DO: Add keybind option
# - TO-DO: Add outfits automatically
def vtuberLoadOutfits():
    outfits = {}

    for image in glob.glob(f"{PATH_OUTFITS}/outfit_*.png"):
        print(image)
        outfits[(image.split("\\")[image.count("\"") - 1]).split("_")[1][0]] = pygame.image.load(image)

    print("Outfits:")
    for k in outfits:
        print(f" - {k}")

    return outfits

# Load Animations
# - TO-DO: Add names to animations automatically
def vtuberLoadAnimations():
    animations = {
        "bobnoarms": pygame.image.load(f"{PATH_AVATARS}/bobisdancing/bobnoarms.png"),
        "walkin": [],
        "dance": []
    }

    for image in glob.glob(f"{PATH_AVATARS}/bobiswalking/*.png"):
        animations["walkin"].append(pygame.image.load(image))

    for image in glob.glob(f"{PATH_AVATARS}/bobisdancing/wobble*.png"):
        animations["dance"].append(pygame.image.load(image))

    return animations

# Change avatar
def vtuberChangeAvatar(n, pos=(0, 0)):
    screen.blit(avatars[n], pos)

# Change outfit
def vtuberChangeOutfit(outfit = None):
    global outfit_current
    if (outfit == None):
        if (outfit_current == None):
            screen.blit(avatars[0], (0, 0))
        else:
            screen.blit(outfits[outfit_current], (0, 0))
    else:
        outfit_current = outfit
        screen.blit(outfits[outfit_current], (0, 0))

# Handle keypresses
# - TO-DO: Add outfit handling
# - TO-DO: Add avatar handling
# - TO-DO: Add stage handling
def vtuberHandleKey():
    pass

# Redraw screen
def vtuberRedraw(step = 0):
    screen.fill((255, 255, 255))
    if (stage == TALK):
        screen.blit(avatars[step], (0, 0))

# Initiate pygame and variables
def vtuberInit():
    # Microphone
    pA = pyaudio.PyAudio()
    mic = pA.open(
        format = pyaudio.paFloat32, channels = 1,
        rate = RATE, input = True,
        frames_per_buffer = FRAMES_PER_BUFFER
    )

    # Pygame
    pygame.init()
    size = img_size
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    return (mic, size, screen, clock)

def main():
    global stage
    global screen, avatars, outfits, animations

    # Get avatars, outfits and animations ready
    avatars = vtuberLoadAvatars()
    outfits = vtuberLoadOutfits()
    animations = vtuberLoadAnimations()

    init = vtuberInit()
    mic = init[0]
    size, screen, clock = init[1], init[2], init[3]

    # Set variables
    step_prev = 0
    step = 0
    steps = len(avatars) - 1

    running = True

    # Draw loop
    while running:
        for event in pygame.event.get():
            # Quit
            if (event.type == pygame.QUIT):
                running = False
                break
            # Extras
            elif (event.type == pygame.KEYUP):
                # Intro
                if ((event.key == pygame.K_i) and ((stage == BLANK) or (stage == None) or (stage == IDLE))):
                    stage = INTRO
                # Idle (no mouth movement)
                elif ((event.key == pygame.K_s) and (
                    (stage == TALK) or
                    (stage == IDLE) or
                    (stage == DANCE) or
                    (stage == None))):

                    if (stage == None):
                        stage = TALK
                    else:
                        stage = IDLE
                # Reload
                elif (event.key == pygame.K_r):
                    vtuberRedraw()
                    pygame.display.update()
                else:
                    # Talk
                    if (stage == TALK):
                        if (event.key == pygame.K_n):
                            screen.blit(avatars[0], (0, 0))
                            pygame.display.update()
                        elif (event.key == pygame.K_o):
                            stage = OUTRO
                            step = len(animations["walkin"]) - 1
                        elif (event.key == pygame.K_d):
                            stage = DANCE
                            step = 0
                        else:
                            key = pygame.key.name(event.key)

                            if (key in outfits):
                                vtuberChangeOutfit(key)
                                pygame.display.update()

        # Intro stage
        if (stage == INTRO):
            screen.fill((255, 255, 255))

            if ((step // 10) < len(animations["walkin"])):
                screen.blit(animations["walkin"][step // 10], (0, 0))
                step += 1
            else:
                screen.blit(avatars[0], (0, 0))
                step = 0
                stage = TALK

            pygame.display.update()

        # Talk stage
        elif (stage == TALK):
            # READ MIC
            data = mic.read(FRAMES_PER_BUFFER)
            samples = np.frombuffer(data, dtype = aubio.float_type)
            volume = (np.sum(samples * samples) / len(samples)) * 1000

            if (volume > 25):
                step = 4
            elif (volume > 19):
                step = 3
            elif (volume > 12):
                step = 2
            elif (volume > 6):
                step = 1
            elif (volume <= 6):
                step = 0

            #print(volume)
            #print(step)

            # Only draw if something needs to be updated
            if (step_prev != step):
                step_prev = step
                vtuberChangeAvatar(step, (0, 0))

                # Mouth region
                pygame.display.update(REGION_MOUTH)

        # Outro stage
        elif (stage == OUTRO):
            screen.fill((255, 255, 255))

            if ((step // 10) < len(animations["walkin"])):
                screen.blit(animations["walkin"][(-(step // 10) - 1)], (0, 0))
                pygame.display.update()
                step += 1
            else:
                screen.blit(avatars[0], (0, 0))
                step = 0
                stage = BLANK

        # Dance
        elif (stage == DANCE):
            if ((step // 2) < len(animations["dance"])):
                screen.fill((255, 255, 255))
                screen.blit(animations["bobnoarms"], (0, 0))
                screen.blit(animations["dance"][step // 2], (0, 0))
                pygame.display.update()
                step += 1
            else:
                pygame.display.update()
                step = 0
                stage = TALK

        # Idle
        elif (stage == IDLE):
            screen.fill((255, 255, 255))
            vtuberChangeOutfit()
            stage = None
            pygame.display.update()

        # Draw blank screen (only once)
        if (stage == BLANK):
            screen.fill((255, 255, 255))
            pygame.display.update()
            stage = None

        clock.tick(50)

    pygame.quit()
    quit()

main()

from PIL import Image
import aubio
import pygame
import pyaudio
import numpy as np
import glob

# Paths
PATH_AVATARS = "avatar"
PATH_COSTUMES  = "costumes"

# Mouth region to be updated (x, y, w, h)
REGION_MOUTH = (260, 370, 470, 210)

BLANK   = 0
INTRO   = 1
TALK    = 2
OUTRO   = 3
DANCE   = 4
stage   = BLANK

FRAMES_PER_BUFFER = 2048 // 2
pA = pyaudio.PyAudio()
mic = pA.open(
    format = pyaudio.paFloat32, channels = 1,
    rate = 44100, input = True,
    frames_per_buffer = FRAMES_PER_BUFFER
)


# Get image size to make canvas fit image
img_size = 0, 0
with Image.open(glob.glob(f"{PATH_AVATARS}/*.png")[0]) as img:
    img_size = img.size

pygame.init()

size = width, height = img_size

clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)

avatars = []
costumes = {}

# TO-DO: (ADD ANIMATIONS AUTOMATICALLY FROM PATH_AVATARS SUBFOLDERS)
animations = {
    "bobnoarms": pygame.image.load(f"{PATH_AVATARS}/bobisdancing/bobnoarms.png"),
    "walkin": [],
    "dance": []
}

for image in glob.glob(f"{PATH_AVATARS}/*.png"):
    avatars.append(pygame.image.load(image))

# Costumes
# - TO-DO: Add costumes automatically
for image in glob.glob(f"{PATH_COSTUMES}/costume_*.png"):
    costumes[(image.split("\\")[image.count("\"") - 1]).split("_")[1][0]] = pygame.image.load(image)

# Animations
# - TO-DO: Add names to animations automatically
for image in glob.glob(f"{PATH_AVATARS}/bobiswalking/*.png"):
    animations["walkin"].append(pygame.image.load(image))

for image in glob.glob(f"{PATH_AVATARS}/bobisdancing/wobble*.png"):
    animations["dance"].append(pygame.image.load(image))

# TO-DO: Add costume names
print("Costumes:")
for k in costumes:
    print(f" - {k}")

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
            if ((event.key == pygame.K_i) and ((stage == BLANK) or (stage == None))):
                stage = INTRO
                step = 0
            else:
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

                        if (key in costumes):
                            screen.blit(costumes[key], (0, 0))
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
            screen.blit(avatars[step], (0, 0))

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

    # Draw blank screen (only once)
    if (stage == BLANK):
        screen.fill((255, 255, 255))
        pygame.display.update()
        stage = None
        
    clock.tick(50)

pygame.quit()
quit()

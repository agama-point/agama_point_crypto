import pygame
import time, datetime
from lib.agama_umbrel_lib import get_block_info

DEBUG = False
TXT_FILE = False
SAVE_HISTOGRAM = True


FROM_BLOCK = 770000 # 50000
NUM_TX = 5000 # 5000
STEP = 1 # 1

SCREEN_W = 1000
SCREEN_H = 620


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_W , SCREEN_H))

# Create a font object for text rendering
font = pygame.font.Font(None, 20)
text = font.render("AgamaPoint | Umbrel | Blockchain - num txs FROM_BLOCK "+str(FROM_BLOCK), True, (255, 255, 255))
screen.blit(text, (10, SCREEN_H - 70))
text = font.render("TXS =2 (RED) | >2 (GREEN) | >10 (BLUE) | >100 (YELL) |", True, (128, 128, 128))
screen.blit(text, (500, SCREEN_H - 70))
text = font.render("TXS >1000 (WHI) | >2000 (VIOL) | >3000 (CYAN) |", True, (128, 128, 128))
screen.blit(text, (500, SCREEN_H - 50))

dt = get_block_info(FROM_BLOCK)[1]
dt2 = get_block_info(FROM_BLOCK+NUM_TX*STEP)[1]
print("date_time", FROM_BLOCK, dt, dt2)

text = font.render("From "+str(dt) + " to "+ str(dt2) + " | STEP " + str(STEP), True, (128, 128, 128))
screen.blit(text, (10, SCREEN_H - 50))
pygame.display.update()

if TXT_FILE:
    txt_file = "data/block_"+str(FROM_BLOCK)+".txt" 
    with open(txt_file, "a") as file:
        file.write("--- FROM_BLOCK: " + str(FROM_BLOCK)+"\n")


# Define the size and position of each square
x, y = 0, 0
last_color = (0,0,0)

# ToDo histogram
n = 10
hist_array = [0] * n
#histogram = {}

for i in range(1, NUM_TX + 1):
    try:
        lentx, dt = get_block_info(i * STEP + FROM_BLOCK)
    except:
        print("Err.get_block_info()")
        lentx = -1
        color = last_color
        hist_array[0] += 1 

    if lentx > 1 and TXT_FILE:
        with open(txt_file, "a") as file:
            file.write(str(i) + " | " + str(lentx) + " | " + str(dt) + "\n")

    if lentx == 1:
        color = (128, 128, 128)
        hist_array[1] += 1 
    if lentx == 2:
        color = (255, 0, 0)
        hist_array[2] += 1 
    if lentx > 2 and lentx < 10:
        color = (0, 255, 0)
        hist_array[3] += 1 
    if lentx >= 10 and lentx < 100:
        color = (0, 0, 255)
        hist_array[4] += 1 
    if lentx >= 100 and lentx < 1000:
        color = (255, 255, 0)
        hist_array[5] += 1 
    if lentx >= 1000 and lentx < 2000:
        color = (255, 255, 255)
        hist_array[6] += 1 
    if lentx >= 2000 and lentx < 3000:
        color = (255, 0, 255)
        hist_array[7] += 1 
    if lentx > 3000:
        color = (0, 255, 255)
        hist_array[8] += 1 
    
    last_color = color

    print(lentx, hist_array)

    pygame.draw.rect(screen, color, pygame.Rect(x, y, 9, 9))
    x += 10
    if x >= 1000:
        x = 0
        y += 10
    pygame.display.update()
    time.sleep(0.01)

text = font.render(str(hist_array[1]), True, (128, 128, 128))
screen.blit(text, (500, SCREEN_H - 30))

text = font.render(str(hist_array[2]), True, (255, 0, 0))
screen.blit(text, (550, SCREEN_H - 30))

text = font.render(str(hist_array[3]), True, (0, 255, 0))
screen.blit(text, (600, SCREEN_H - 30))

text = font.render(str(hist_array[4]), True, (0, 0, 255))
screen.blit(text, (650, SCREEN_H - 30))

text = font.render(str(hist_array[5]), True, (255, 255, 0))
screen.blit(text, (700, SCREEN_H - 30))

text = font.render(str(hist_array[6]), True, (255, 255, 255))
screen.blit(text, (750, SCREEN_H - 30))

text = font.render(str(hist_array[7]), True, (255, 0, 255))
screen.blit(text, (800, SCREEN_H - 30))

text = font.render(str(hist_array[8]), True, (0, 255, 255))
screen.blit(text, (850, SCREEN_H - 30))

pygame.display.update()

# Save the image to a file
now = datetime.datetime.now()
filename = f"data/block_{FROM_BLOCK}-{now.day}_{now.hour}_{now.minute}.png"
print("save image - filename",filename)
pygame.image.save(screen, filename)


if SAVE_HISTOGRAM:
    print("save histogram")
    txt_file = "data/block_histogram.txt"
    with open(txt_file, "a") as file:
        file.write(str(FROM_BLOCK) + " (" + str(dt) + ") " + str(hist_array) + str(STEP)+ "\n")


# Wait for the user to close the window
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


# Quit Py
pygame.quit()

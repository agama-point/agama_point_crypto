import pygame
import sys

# Inicializace Pygame
pygame.init()

# Nastavení velikosti okna
window_size = (640, 320)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Cisyercial Numerus")

black = (0, 0, 0)
white = (255, 255, 255)
pen = 3 # pen size

# Velikost buňky a odsazení
cell_size = 10
padding = 35

# Body
ca = (0, 3)
cb = (2, 3)
cc = (0, 1)
cd = (2, 1)

# transormace tx,ty
t1 = (1,1)  # 1
t2 = (-1,1)   # 10
t3 = (1,-1)  # 100
t4 = (-1,-1) # 1000
# Definice čárek pro jednotlivé číslice
numbers = {
    '0': [ca, cc],
    '1': [ca, cb],
    '2': [cc, cd],
    '3': [cb, ca, cc, cd],
    '4': [ca, cd, cc],
    '5': [ca, cb, cc],
    '6': [cd, cb],
    '7': [ca, cb, cd],
    '8': [cc, cd, cb],
    '9': [cc, cd, cb, ca]
}

def draw_digits(num, pos=100):
    digits = str(num).zfill(4)
    dig_arr = []
    for index, digit in enumerate(digits):
         dig_arr.append(digit)

    cistercial_digit(screen, dig_arr[3], t1, pos)
    cistercial_digit(screen, dig_arr[2], t2, pos)
    cistercial_digit(screen, dig_arr[1], t3, pos)
    cistercial_digit(screen, dig_arr[0], t4, pos)


def cistercial_digit(screen, digit, tx, x_offset):
    y_offset = padding
    dl = numbers[digit] # digit_lines

    pygame.draw.line(screen, black, (x_offset, cell_size + padding) , (x_offset, 7* cell_size + padding), pen)
        
    for i in range(len(dl) - 1):
            start_pos = (x_offset + tx[0] * dl[i][0] * cell_size, y_offset + (4 - tx[1] * dl[i][1]) * cell_size)
            end_pos = (x_offset + tx[0] * dl[i + 1][0] * cell_size, y_offset + (4 - tx[1] * dl[i + 1][1]) * cell_size)
            pygame.draw.line(screen, black, start_pos, end_pos, pen)

# Hlavní smyčka programu
def main():
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(white)

        for i in range(10):
             draw_digits(i+i*1000, i*60)
        """  
        draw_digits(21, 100)
        draw_digits(1234, 200)
        draw_digits(2047, 300)
        """
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

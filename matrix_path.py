import pygame
import sys

DEBUG = True
GRID = True
# Konstanty pro velikost buňky a mřížky
CELL_SIZE = 20
GRID_COUNT = 31        # 51x51 buněk (souřadnice od -25 do 25)
WINDOW_SIZE = GRID_COUNT * CELL_SIZE  # 510x510 px

# Střed canvasu (0,0) bude uprostřed okna
CENTER = (WINDOW_SIZE // 2, WINDOW_SIZE // 2)

def hex_to_bin_pairs(hex_str):
    """Převede hexadecimální řetězec na binární řetězec a rozdělí ho na dvojice."""
    hex_str = hex_str.strip()
    if hex_str.startswith("0x") or hex_str.startswith("0X"):
        hex_str = hex_str[2:]
    # Každá hex cifra se převede na 4-bitový řetězec
    bin_str = ''.join(f"{int(c, 16):04b}" for c in hex_str)
    # Pokud by byl počet bitů lichý, doplníme úvodní nulou (obvykle není nutné)
    if len(bin_str) % 2 != 0:
        bin_str = "0" + bin_str
    # Rozdělíme do dvojic
    return [bin_str[i:i+2] for i in range(0, len(bin_str), 2)]

DIRECTIONS = {
    "00": (0, 1),   # up
    "01": (-1, 0),  # left
    "10": (0, -1),  # down
    "11": (1, 0)    # right
}

def get_direction(pair):
    return DIRECTIONS.get(pair)

def grid_to_screen(grid_pos):
    """
    Převádí mřížkové souřadnice (kde střed je (0,0)) na souřadnice obrazovky.
    Pozn.: V pygame souřadnice Y roste směrem dolů, proto odečítáme.
    """
    x, y = grid_pos
    screen_x = CENTER[0] + x * CELL_SIZE
    screen_y = CENTER[1] - y * CELL_SIZE
    return (screen_x, screen_y)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Cesta podle vstupního klíče")
    clock = pygame.time.Clock()

    # 
    hex_input = input("Zadej hexadecimální vstup: ")
    pairs = hex_to_bin_pairs(hex_input)
    if DEBUG: 
        print(pairs)
    
    # start (0,0)
    path = []
    current_pos = (0, 0)
    path.append(current_pos)
    for pair in pairs:
        dx, dy = get_direction(pair)
        # Aktualizace mřížkové pozice
        current_pos = (current_pos[0] + dx, current_pos[1] + dy)
        path.append(current_pos)
    
    # main_loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        if GRID:
            for x in range(0, WINDOW_SIZE, CELL_SIZE):
                pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, WINDOW_SIZE))
            for y in range(0, WINDOW_SIZE, CELL_SIZE):
                pygame.draw.line(screen, (200, 200, 200), (0, y), (WINDOW_SIZE, y))

        # path
        if len(path) > 1:
            for i in range(len(path) - 1):
                start_pos = grid_to_screen(path[i])
                end_pos = grid_to_screen(path[i+1])
                pygame.draw.line(screen, (0, 0, 255), start_pos, end_pos, 3)
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

"""
abc123abc123 ?195

"""

import pygame
from crypto_agama.agama_transform_tools import norm_hex, hex_to_wif, wif_to_private_key, measure_time  # , gen_pub_ecdsa

# ----- secp256k1 Parameters -----
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F  # Modulus
A = 0
B = 7

# ----- Base Point G -----
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

# ----- Point Addition -----
def point_addition(x1, y1, x2, y2, p):
    if x1 == x2 and y1 == y2:
        m = (3 * x1**2 + A) * pow(2 * y1, -1, p) % p  # Point doubling
    else:
        m = (y2 - y1) * pow(x2 - x1, -1, p) % p  # Point addition

    x3 = (m**2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p

    return x3, y3

# ----- Scalar Multiplication -----
@measure_time
def scalar_multiplication(k, x, y, p):
    x_res, y_res = None, None
    binary_k = bin(k)[2:]
    for bit in binary_k:
        if x_res is None:
            x_res, y_res = x, y
        else:
            x_res, y_res = point_addition(x_res, y_res, x_res, y_res, p)  # Point doubling
            if bit == '1':
                x_res, y_res = point_addition(x_res, y_res, x, y, p)  # Point addition
    return x_res, y_res

# Initialize Pygame
pygame.init()

# Constants
MARGIN = 60
WIDTH, HEIGHT = 600 + 2 * MARGIN, 600 + 2 * MARGIN  # Window size in pixels
CANVAS_SIZE = 100  # Canvas size in units
PIXELS_PER_UNIT = 6  # Conversion from units to pixels
NUM_LINES = 10  # Number of grid lines
GRID_SPACING = 600 // NUM_LINES  # Spacing between grid lines in pixels

# Set up the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Public Key Points on Elliptic Curve')

# Font for rendering indices
font = pygame.font.SysFont(None, 20)

# Function to draw the grid
def draw_grid():
    for x in range(0, 600 + 1, GRID_SPACING):
        pygame.draw.line(screen, (128, 128, 128), (x + MARGIN, MARGIN), (x + MARGIN, 600 + MARGIN))
    for y in range(0, 600 + 1, GRID_SPACING):
        pygame.draw.line(screen, (128, 128, 128), (MARGIN, y + MARGIN), (600 + MARGIN, y + MARGIN))

# Generating sixty public key points
points = []
for i in range(1, 61):
    key1 = norm_hex(str(i))
    k = int(key1, 16)  # Convert hex to int
    Kx_manual, Ky_manual = scalar_multiplication(k, Gx, Gy, P)
    # Normalize coordinates to range 0-99
    x = (Kx_manual % P) * CANVAS_SIZE // P
    y = (Ky_manual % P) * CANVAS_SIZE // P
    x = int(x)
    y = int(y)
    print(f"Point {i}: ({x}, {y})")
    points.append((x, y))

# Main program loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with black
    screen.fill((0, 0, 0))

    # Draw the grid
    draw_grid()

    # Draw the points and connect them
    for idx, point in enumerate(points):
        x_pixel = point[0] * PIXELS_PER_UNIT + MARGIN
        y_pixel = point[1] * PIXELS_PER_UNIT + MARGIN

        # Set the point size
        if idx == 0:
            point_radius = 10  # First point is 2x bigger
        else:
            point_radius = 5

        # Draw the point
        pygame.draw.circle(screen, (255, 165, 0), (x_pixel, y_pixel), point_radius)

        # Render the index number
        text = font.render(str(idx + 1), True, (255, 255, 255))
        screen.blit(text, (x_pixel + 5, y_pixel - 5))

        # Connect to the previous point
        if idx > 0:
            prev_x_pixel = points[idx - 1][0] * PIXELS_PER_UNIT + MARGIN
            prev_y_pixel = points[idx - 1][1] * PIXELS_PER_UNIT + MARGIN

            # Set the line color based on index
            if idx <= 20:
                line_color = (255, 0, 0)  # Red
            elif idx <= 40:
                line_color = (255, 165, 0)  # Orange
            else:
                line_color = (255, 255, 0)  # Yellow

            pygame.draw.line(screen, line_color, (prev_x_pixel, prev_y_pixel), (x_pixel, y_pixel), 1)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()

"""
--- point G ---
55066263022277343669578718895168534326250603453777594175500187360389116729240
32670510020758816978083085130507043184471273380659243275938904335757337482424

--- 0000000000000000000000000000000000000000000000000000000000000001 ---
--- pubKey (x, y):
55066263022277343669578718895168534326250603453777594175500187360389116729240
32670510020758816978083085130507043184471273380659243275938904335757337482424
len: 77 77
--- 0000000000000000000000000000000000000000000000000000000000000002 ---
--- pubKey (x, y):
89565891926547004231252920425935692360644145829622209833684329913297188986597
12158399299693830322967808612713398636155367887041628176798871954788371653930
...
"""
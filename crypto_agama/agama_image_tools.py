from PIL import Image as PILimage
import numpy as np
import os, random, copy
import hashlib # info()

__version__ = "0.5.1" # 2024/08
 
"""
# Example usage:
from crypto_agama.agama_image_tools import Image21

img = Image21()
# img.create(32, 16, (255, 255, 255))
img.load("data/img1.png")
img.info()
img.infilt_hard("0123456789ABCDEF", 0, 0, "R")

img.print_matrix(0, 0, 40)
#img.add_noise("G", 10)
img.save("data/img2.png")

img.set_pixel(10, 10, (255, 0, 0))
img.print_matrix(0, 0, 10)
img.add_noise("G", 10)
img.save("output.png")
img.clear((0, 0, 0))
img.print_matrix(0, 0, 10)

hex_str = "0c1e24e5917779d297e14d45f14e1a1a"
bin_str = hex2bin(hex_str)
img.infilt_bin(bin_str)
img.print_matrix(0, 0, 40, hexa=True)

bin_str = img.parse_bin(0,0,"R",128)
print(bin_str, "\n", bin2hex(bin_str))

img2 = Image21()
img2.copy(img1, 2) 
img2.add_noise("G",100)
...
"""

# ----------------- temp ----------------------
def bin2hex(bin_str):
    hex_str = ""
    # Zpracuj celý řetězec po čtveřicích
    for i in range(0, len(bin_str), 4):
        chunk = bin_str[i:i+4]
        if len(chunk) == 4:
            # Převést čtveřici bitů na hexadecimální hodnotu
            hex_value = hex(int(chunk, 2))[2:].upper()
            hex_str += hex_value
        else:
            # Pokud je čtveřice neúplná, přidat hvězdičky
            hex_value = hex(int(chunk.ljust(4, '0'), 2))[2:].upper()
            hex_str += hex_value + "*" * (4 - len(chunk))
    return hex_str


def hex2bin(hex_str):
    bin_str = ""
    for char in hex_str:
        if char == "*":
            # Přidej odpovídající počet hvězdiček
            bin_str += "*"
        else:
            # Převést hexadecimální znak na 4-bitovou binární hodnotu
            bin_value = bin(int(char, 16))[2:].zfill(4)
            bin_str += bin_value
    return bin_str



# ================ main Class =========================
class Image21:
    def __init__(self, width=64, height=32, color=(255, 255, 255)):
        self.width = width   #self.width = None
        self.height = height #self.height = None
        self.image = PILimage.new("RGB", (self.width, self.height), color)
        self.pixels = self.image.load()
        self.filename = None
        self.temp_filepath = "data/temp.png"


    def create(self, width=32, height=16, color=(0, 0, 0)):
        self.width = width
        self.height = height
        self.image = PILimage.new("RGB", (width, height), color)
        self.pixels = np.array(self.image)


    def info(self, hash = True):
        if self.filename:
            file_size = os.path.getsize(self.filename)
            with open(self.filename, "rb") as f:
                file_data = f.read()
            resolution = self.image.size
            color_depth = self.image.mode  # Should typically return "RGB" or "RGBA"
            print(f"--- [ image info] --- | File: {self.filename} | size: {file_size} Bytes")
            print(f"Resolution: {resolution[0]}x{resolution[1]} | Color depth: {color_depth}")
            if hash:
                md5_hash = hashlib.md5(file_data).hexdigest()
                sha256_hash = hashlib.sha256(file_data).hexdigest()
                print(f"MD5: {md5_hash}")
                print(f"SHA-256: {sha256_hash}")
            print("-"*32)


    def save(self, name="temp.png", reload="True"):
        if self.image:
            self.image.save(name)
            self.filename = name
            if reload:
                self.load(name)


    def copyx(self, img_src):
        """
        self.width = img_src.width
        self.height = img_src.height
        self.image = img_src.image.copy()
        self.pixels = self.image.load()
        """
        self.__dict__ = copy.deepcopy(img_src.__dict__)
        self.pixels = self.image.load()


    def copy(self, img_src, zoom=1):
        if zoom > 1:
            # new * zoom
            new_width = img_src.width * zoom
            new_height = img_src.height * zoom
            self.create(new_width, new_height)
            
            for y in range(img_src.height):
                for x in range(img_src.width):
                    color = img_src.get_pixel(x, y)
                    
                    # Pokud je barva ve formátu RGBA, odebereme alfa kanál
                    if len(color) == 4:
                        color = color[:3]
                        
                    for i in range(zoom):
                        for j in range(zoom):
                            self.set_pixel(x * zoom + i, y * zoom + j, color)
        else:
            img_src.save(self.temp_filepath)
            self.load(self.temp_filepath)


    def load(self, name):
        self.image = PILimage.open(name)
        self.pixels = np.array(self.image)
        self.width, self.height = self.image.size
        self.filename = name


    def set_pixel(self, x, y, color):
        if self.image:
            self.image.putpixel((x, y), color)
            self.pixels[y, x] = color


    def get_pixel(self, x, y):
        if self.image:
            return self.image.getpixel((x, y))


    def set_pixel(self, x, y, color):
        if self.image:
            self.image.putpixel((x, y), color)
            self.pixels[y, x] = color


    def print_matrix(self, x=0, y=0, first=10, hexa=True):
        if self.image:
            h, w = self.pixels.shape[:2]
            matrix = []
            for i in range(y, min(y + first, h)):
                for j in range(x, min(x + first, w)):
                    matrix.append((i, j, self.pixels[i, j]))

            for idx, (i, j, color) in enumerate(matrix[:first]):
                if idx % 8 == 0:  # Only print coordinates at the start of a new line
                    coord_str = f"({i:03},{j:03})"
                    print(f"{coord_str} ", end="")                
                if hexa:
                    color_str = f"{color[0]:02X}{color[1]:02X}{color[2]:02X}"
                else:
                    color_str = f"({color[0]}, {color[1]}, {color[2]})"
                print(f"{color_str} ", end="")

                if (idx + 1) % 8 == 0: print() # Break line after 8 entries

            # Final newline if the last line didn't have exactly 8 entries
            if len(matrix) % 8 != 0:
                print()


    def create_noise(self, ch="R", fill=10):
        if self.image:
            channel_idx = {"R": 0, "G": 1, "B": 2}.get(ch.upper(), 0)
            num_pixels = self.width * self.height
            num_noise_pixels = int(num_pixels * (fill / 80))
            for _ in range(num_noise_pixels):
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                current_color = list(self.pixels[y, x])
                current_color[channel_idx] = random.randint(0, 255)
                self.set_pixel(x, y, tuple(current_color))


    def add_noise(self, ch="R", noise_range=3):
        if self.image:
            channel_idx = {"R": 0, "G": 1, "B": 2}.get(ch.upper(), 0)
            for y in range(self.height):
                for x in range(self.width):
                    current_color = list(self.pixels[y, x])
                    current_value = int(current_color[channel_idx]) # uint8 ti int
                    noise = random.randint(-noise_range, noise_range)
                    new_value = current_value + noise
                    
                    if new_value < 0: new_value = 0
                    elif new_value > 255: new_value = 255

                    current_color[channel_idx] = np.uint8(new_value)
                    self.set_pixel(x, y, tuple(current_color))


    def add_noisex(self, ch="R", noise_range=3):
        if self.image:
            channel_idx = {"R": 0, "G": 1, "B": 2}.get(ch.upper(), 0)
            for y in range(self.height):
                for x in range(self.width):
                    try:
                        if x < self.width and y < self.height:  # Tento blok je teď nadbytečný, protože for loop zajišťuje platné indexy
                            current_color = list(self.pixels[x, y])
                            current_value = int(current_color[channel_idx])
                            noise = random.randint(-noise_range, noise_range)
                            new_value = current_value + noise
                            if new_value < 0:
                                new_value = 0
                            elif new_value > 255:
                                new_value = 255
                            current_color[channel_idx] = np.uint8(new_value)
                            self.set_pixel(x, y, tuple(current_color))
                    except IndexError:
                        print(f"IndexError at x={x}, y={y}, image size={self.width}x{self.height}")
                        raise

    def clear(self, color=(0, 0, 0)):
        self.create(self.width, self.height, color)


    def hline(self, y=0, color=(128, 128, 128)):
        if self.image and 0 <= y < self.height:
            for x in range(self.width):
                self.set_pixel(x, y, color)


    def vline(self, x=0, color=(128, 128, 128)):
        if self.image and 0 <= x < self.width:
            for y in range(self.height):
                self.set_pixel(x, y, color)


    def border(self, th=2, color=(128, 128, 128)):
        if self.image:
            for i in range(th):
                self.hline(i, color)
                self.hline(self.height - 1 - i, color)       
            for i in range(th):
                self.vline(i, color)
                self.vline(self.width - 1 - i, color)


    def infilt_hard(self, data, x=0, y=0, ch="R"):
        if self.image:
            channel_idx = {"R": 0, "G": 1, "B": 2}.get(ch.upper(), 0)
            index = 0
            h, w = self.pixels.shape[:2]

            for i in range(y, h):
                for j in range(x, w):
                    if index < len(data):
                        current_color = list(self.pixels[i, j])
                        hex_value = int(data[index:index+2], 16)
                        current_color[channel_idx] = hex_value
                        self.set_pixel(j, i, tuple(current_color))
                        index += 2
                    else:
                        return
                x = 0  # Reset x to 0 after the first row


    def parse(self, x=0, y=0, ch="R", length=16):
        if self.image:
            channel_idx = {"R": 0, "G": 1, "B": 2}.get(ch.upper(), 0)
            data = []
            h, w = self.pixels.shape[:2]

            for i in range(y, h):
                for j in range(x, min(x + length, w)):
                    pixel = self.pixels[i, j]
                    data.append(f"{pixel[channel_idx]:02X}")
                    if len(data) >= length:
                        return ''.join(data)
                x = 0  # Reset x to 0 after the first row

        return ''.join(data)  # In case the loop finishes without reaching 'length'


    def normalize(self, ch="R"):
        if self.image:
            channel_idx = {"R": 0, "G": 1, "B": 2}.get(ch.upper(), 0)
            h, w = self.pixels.shape[:2]

            for i in range(h):
                for j in range(w):
                    current_color = list(self.pixels[i, j])
                    if (current_color[channel_idx] - 1) % 2 == 0:  # Pokud je (barva - 1) sudá
                        current_color[channel_idx] -= 1  # Snížíme hodnotu o 1
                    self.set_pixel(j, i, tuple(current_color))


    def infilt_bin(self, bin_str, x=0, y=0, ch="R"):
        if self.image:
            channel_idx = {"R": 0, "G": 1, "B": 2}.get(ch.upper(), 0)
            index = 0
            h, w = self.pixels.shape[:2]

            for i in range(y, h):
                for j in range(x, w):
                    if index < len(bin_str):
                        current_color = list(self.pixels[i, j])
                        if bin_str[index] == '1':  # if 1, + 1
                            current_color[channel_idx] = min(current_color[channel_idx] + 1, 255)
                        self.set_pixel(j, i, tuple(current_color))
                        index += 1
                    else:
                        return
                x = 0  # Reset x to 0 after the first row


    def parse_bin(self, x=0, y=0, ch="R", length=32):
        if self.image:
            channel_idx = {"R": 0, "G": 1, "B": 2}.get(ch.upper(), 0)
            binary_data = []
            h, w = self.pixels.shape[:2]

            for i in range(y, h):
                for j in range(x, min(x + length, w)):
                    pixel = self.pixels[i, j]
                    if pixel[channel_idx] % 2 == 0:
                        binary_data.append('0')
                    else:
                        binary_data.append('1')

                    if len(binary_data) >= length:
                        return ''.join(binary_data)
                x = 0  # Reset x to 0 after the first row

        return ''.join(binary_data)  # In case the loop finishes without reaching 'length'


# -------------------------old 2020----------------------------
def hexa_noise_to_png(hex_data,image_path):
    byte_data = bytes.fromhex(hex_data)    
    num_data = np.frombuffer(byte_data, dtype=np.uint8)
    """
    width = int(np.sqrt(len(num_data)))
    height = len(num_data) // width
    image_array = np.reshape(num_data, (height, width))
    """
    width = int(np.ceil(np.sqrt(len(num_data))))
    height = int(np.ceil(len(num_data) / width))

    padding = width * height - len(num_data)
    num_data = np.pad(num_data, (0, padding), mode='constant')
    image_array = np.reshape(num_data, (height, width)) # 2D arr

    image = PILimage.fromarray(image_array)   
    image.save(image_path)


def noise_png_to_hexa(image_path):
    image = PILimage.open(image_path)   
    image_array = np.array(image)    
    num_data = image_array.flatten()    
    byte_data = bytes(num_data)
    hex_data = byte_data.hex()

    return hex_data


def hexa_noise_to_bmpline(hex_data,image_path):
    byte_data = bytes.fromhex(hex_data) # hex2bytesArr
    num_data = np.frombuffer(byte_data, dtype=np.uint8) # 2nums

    image = PILimage.new('1', (len(num_data) * 8, 1))

    for i, value in enumerate(num_data):
        for j in range(8):
            bit = (value >> j) & 1
            image.putpixel((i * 8 + j, 0), int(bit))

    image.save(image_path, 'BMP')


def noise_bmpline_to_hexa(image_path):
    image = PILimage.open(image_path)
    image_array = np.array(image, dtype=np.uint8)

    bit_data = np.unpackbits(image_array).reshape(-1, 8)
    num_data = np.packbits(bit_data).tobytes()
    hex_data = num_data.hex()

    return hex_data


def hexa_arr_noise_to_bmp(hex_array_data,image_path):
    num_elements = len(hex_array_data)
    num_pixels = max(len(hex_data) * 4 for hex_data in hex_array_data)

    image = PILimage.new('1', (num_pixels, num_elements))

    for i, hex_data in enumerate(hex_array_data):
        byte_data = bytes.fromhex(hex_data.zfill(num_pixels // 4))  # hex to bytes
        num_data = np.frombuffer(byte_data, dtype=np.uint8)  # 2 nums

        for j, value in enumerate(num_data):
            for k in range(8):
                if j * 8 + k < num_pixels:
                    bit = (value >> k) & 1
                    image.putpixel((j * 8 + (7 - k), i), int(bit))

    image.save(image_path, 'BMP')


def noise_bmp_to_hexa_arr(image_path):
    image = PILimage.open(image_path)
    image_array = np.array(image, dtype=np.uint8)
    rows, width = image_array.shape
    hex_array_data = []

    for i in range(rows):
        binary_row = ''.join([str(bit) for bit in image_array[i]])
        hex_data = hex(int(binary_row, 2))[2:].zfill(width // 4)
        hex_array_data.append(hex_data)

    return hex_array_data


def cut_image(image_path,image_name,m=3,n=3):
    input_image_path = f"{image_path}/{image_name}.png"

    original_image = PILimage.open(input_image_path)
    width, height = original_image.size

    print(f"src: {width}x{height} Px")

    small_images = []
    for i in range(n):
        for j in range(m):
            x = j * int(width / m)
            y = i * int(height / n)
            cropped_image = original_image.crop((x, y, x + int(width / m), y + int(height / n)))
            small_images.append(cropped_image)

    # save m x n images
    for index, image in enumerate(small_images):
        image_index = str(index+1).zfill(2)
        image.save(f'{image_path}/{image_name}_{image_index}.png')
        print(f'{image_path}/{image_name}_{image_index}.png')


def margin_cut_image(image_path,image_name,mx=3,my=-1,mx2=-1,my2=-1,save=False):
    if my == -1: my = mx
    if mx2 == -1: mx2 = mx
    if my2 == -1: my2 = mx
    input_image_path = f"{image_path}/{image_name}.png"

    original_image = PILimage.open(input_image_path)
    width, height = original_image.size
    print(f"src size: {width}x{height} Px")
    cropped_image = original_image.crop((mx, my, width-mx2, height-my2))
    width, height = cropped_image.size
    print(f"cut size: {width}x{height} Px")
    if save:
        cropped_image.save(f"{image_path}/{image_name}m{mx}{my}.png")

    return cropped_image


# ----------------- pgt/.png ---------------
def print_rgb(img,width=32,height=32,xy=True,all=True,len=32):
    print("DEBUG print_rgb",int(len/width))
    if all:
        jmax = height
    else:
        jmax = int(len/(width-1)) # ¯_(ツ)_/¯
    
    for j in range(jmax):
        for i in range(width): #min(width,len)):
            #print(f"[{i}{j}]", end="")
            try:
                r, g, b, a = img.get_at((i, j))
                if xy:
                    print(f"[{i}{j}]",r, end=" ")
                else:
                    print(f"[{r},{g},{b}]", end=" ") # alpha ¯_(ツ)_/¯
            except:
                print(f"[{i}{j}]","?", end="!")
        print()
    print()


def infilt_patt(img,bit_patt,width=32,height=32,ch ="R",debug=False):
    if debug: print("DEBUG infilt_patt",int(len(bit_patt)/(width-1)))
    for j in range(int(len(bit_patt)/(width-1))+1):
        for i in range(width):
            try:
                r, g, b, a = img.get_at((i, j))
                if bit_patt[i+j*width] == "1":
                    if ch=="R":
                        img.set_at((i, j),(r+1,g,b,a))
                    if ch=="G":
                        img.set_at((i, j),(r,g+1,b,a))
                    if ch=="B":
                        img.set_at((i, j),(r,g,b+1,a))
                
                if debug: print(f"[{i},{j},{i+j*width}]",bit_patt[i+j*width],r, end="")
            except:
                if debug: print(f"[{i},{j}]", end="!")
        if debug: print()
      
    return img


def parse_patt(img,len_bit_patt=255,width=32,height=32,ch="R"):
    # pattern = []
    pattern = ""
    for j in range(int(len_bit_patt/(width-1)+1)):
        for i in range(width):
            try:
                r, g, b, a = img.get_at((i, j))
                if ch=="R":
                    if r%2==0: 
                        #pattern.append(0)
                        pattern +="0"
                    else:
                        #pattern.append(1)
                        pattern +="1"
                if ch=="G":
                    pattern += "0" if g % 2 == 0 else "1"
                if ch=="B":
                    pattern += "0" if b % 2 == 0 else "1"
            except:
                print(f"[{i},{j}]", end="!")
    print()
    return pattern

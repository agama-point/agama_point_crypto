# Agama Point 2015-23
# $ pip install Pillow, numpy

from PIL import Image
import numpy as np


__version__ = "0.2.0"
# png - gray scale 
# bmp - "1bit"


def hexa_noise_to_png(hex_data, image_path):
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

    image = Image.fromarray(image_array)   
    image.save(image_path)


def noise_png_to_hexa(image_path):
    image = Image.open(image_path)
   
    image_array = np.array(image)    
    num_data = image_array.flatten()    
    byte_data = bytes(num_data)
    hex_data = byte_data.hex()

    return hex_data


def hexa_noise_to_bmpline(hex_data, image_path):
    byte_data = bytes.fromhex(hex_data) # hex2bytesArr
    num_data = np.frombuffer(byte_data, dtype=np.uint8) # 2nums

    image = Image.new('1', (len(num_data) * 8, 1))

    for i, value in enumerate(num_data):
        for j in range(8):
            bit = (value >> j) & 1
            image.putpixel((i * 8 + j, 0), int(bit))

    image.save(image_path, 'BMP')


def noise_bmpline_to_hexa(image_path):
    image = Image.open(image_path)
    image_array = np.array(image, dtype=np.uint8)

    bit_data = np.unpackbits(image_array).reshape(-1, 8)
    num_data = np.packbits(bit_data).tobytes()
    hex_data = num_data.hex()

    return hex_data


def hexa_arr_noise_to_bmp(hex_array_data, image_path):
    num_elements = len(hex_array_data)
    num_pixels = max(len(hex_data) * 4 for hex_data in hex_array_data)

    image = Image.new('1', (num_pixels, num_elements))

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
    image = Image.open(image_path)
    image_array = np.array(image, dtype=np.uint8)
    rows, width = image_array.shape
    hex_array_data = []

    for i in range(rows):
        binary_row = ''.join([str(bit) for bit in image_array[i]])
        hex_data = hex(int(binary_row, 2))[2:].zfill(width // 4)
        hex_array_data.append(hex_data)

    return hex_array_data

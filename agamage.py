import argparse
from crypto_agama.agama_image_tools import Image21

"""
python agamage.py crea ag100x100.png 100x100
python agamage.py noise ag100x100.png -c R -f 50

python agamage.py ibin ag100x100.png data/hex.txt -x 0 -y 0 -c R
python agamage.py pbin ag100x100.png -x 0 -y 0 -l 128 -c R
"""
DEBUG = True

def create_image(filename, size):
    width, height = map(int, size.split('x'))
    img = Image21(width, height)
    img.save(filename)

def copy_image(source, destination, zoom=1):
    img_src = Image21()
    img_src.load(source)
    img_dest = Image21()
    img_dest.copy(img_src, zoom)
    img_dest.save(destination)

def add_noise(filename, channel, fill):
    img = Image21()
    img.load(filename)
    img.add_noise(channel, fill)
    img.save(filename)

def add_border(filename, thickness, color):
    img = Image21()
    img.load(filename)
    img.border(thickness, color)
    img.save(filename)

def infilt_bin(filename, hex_file, x=0, y=0, channel="R"):
    img = Image21()
    img.load(filename)
    img.normalize(channel)
    
    with open(hex_file, "r") as file:
        hex_data = file.read().strip()    
    
    bin_data = bin(int(hex_data, 16))[2:].zfill(len(hex_data) * 4)
    if DEBUG:
        print("hex:", hex_data)
        print("bin:", bin_data)
    img.infilt_bin(bin_data, x, y, channel)
    img.save(filename)

def parse_bin_to_hex(filename, x=0, y=0, length=32, channel="R"):
    img = Image21()
    img.load(filename)
    
    bin_data = img.parse_bin(x, y, channel, length)
    hex_data = f"{int(bin_data, 2):X}".zfill(length // 4)
    print(hex_data)

def parse_args():
    parser = argparse.ArgumentParser(description="Agamage CLI tool for image manipulation using Image21 library")
    
    subparsers = parser.add_subparsers(dest="command")

    # Command: crea (create image)
    create_parser = subparsers.add_parser("crea", help="Create a new image")
    create_parser.add_argument("filename", help="Name of the image file to create (e.g., img1.png)")
    create_parser.add_argument("size", help="Size of the image in WIDTHxHEIGHT format (e.g., 100x100)")

    # Command: copy (copy image with optional zoom)
    copy_parser = subparsers.add_parser("copy", help="Copy an image with optional zoom")
    copy_parser.add_argument("source", help="Source image file")
    copy_parser.add_argument("destination", help="Destination image file")
    copy_parser.add_argument("-z", "--zoom", type=int, default=1, help="Zoom factor (default is 1)")

    # Command: noise (add noise to image)
    noise_parser = subparsers.add_parser("noise", help="Add noise to an image")
    noise_parser.add_argument("filename", help="Image file to add noise to")
    noise_parser.add_argument("-c", "--channel", default="R", help="Color channel to add noise to (R, G, B)")
    noise_parser.add_argument("-f", "--fill", type=int, default=10, help="Percentage of pixels to fill with noise (default is 10%)")

    # Command: bord (add border to image)
    border_parser = subparsers.add_parser("bord", help="Add a border to an image")
    border_parser.add_argument("filename", help="Image file to add border to")
    border_parser.add_argument("-t", "--thickness", type=int, default=2, help="Thickness of the border (default is 2)")
    border_parser.add_argument("-c", "--color", nargs=3, type=int, default=[128, 128, 128], help="Color of the border (R G B format, default is 128 128 128)")

    # Command: ibin (infiltrate binary data from hex file)
    ibin_parser = subparsers.add_parser("ibin", help="Infiltrate binary data from a hex file into an image")
    ibin_parser.add_argument("filename", help="Image file to infiltrate")
    ibin_parser.add_argument("hex_file", help="Hex file containing the data to infiltrate")
    ibin_parser.add_argument("-x", type=int, default=0, help="X coordinate to start infiltration (default is 0)")
    ibin_parser.add_argument("-y", type=int, default=0, help="Y coordinate to start infiltration (default is 0)")
    ibin_parser.add_argument("-c", "--channel", default="R", help="Color channel to infiltrate data into (R, G, B)")

    # Command: pbin (parse binary data and convert to hex)
    pbin_parser = subparsers.add_parser("pbin", help="Parse binary data from an image and convert to hex")
    pbin_parser.add_argument("filename", help="Image file to parse data from")
    pbin_parser.add_argument("-x", type=int, default=0, help="X coordinate to start parsing (default is 0)")
    pbin_parser.add_argument("-y", type=int, default=0, help="Y coordinate to start parsing (default is 0)")
    pbin_parser.add_argument("-l", "--length", type=int, default=32, help="Length of binary data to parse (default is 32 bits)")
    pbin_parser.add_argument("-c", "--channel", default="R", help="Color channel to parse data from (R, G, B)")

    # Help and version
    parser.add_argument("-v", "--version", action="version", version="Agamage 1.0")

    return parser.parse_args()

def main():
    args = parse_args()

    if args.command == "crea":
        create_image(args.filename, args.size)
    elif args.command == "copy":
        copy_image(args.source, args.destination, args.zoom)
    elif args.command == "noise":
        add_noise(args.filename, args.channel, args.fill)
    elif args.command == "bord":
        add_border(args.filename, args.thickness, tuple(args.color))
    elif args.command == "ibin":
        infilt_bin(args.filename, args.hex_file, args.x, args.y, args.channel)
    elif args.command == "pbin":
        parse_bin_to_hex(args.filename, args.x, args.y, args.length, args.channel)
    else:
        print("Unknown command. Use -h for help.")

if __name__ == "__main__":
    main()
#!/usr/bin/python3

import argparse
import sys

import base64
import requests

import imghdr
from PIL import Image
from io import BytesIO


def encode_image(img_path: str) -> str:
    try:
        with open(img_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception as e:
        sys.stderr.write('ERROR: %s\n\n' % str(e))
        sys.exit(2)

def send_request(url: str, data: dict) -> str:
    try:
        response = requests.get(url, json=data)
        response.raise_for_status()
        return response.json()['image']
    except Exception as e:
        sys.stderr.write('ERROR: %s\n\n' % str(e))
        sys.exit(2)

def save_image(encoded_img: str, img_path: str) -> None:
    try:
        decoded_file = base64.b64decode(encoded_img)
        file_format = imghdr.what(None, h=decoded_file)
        img = Image.open(BytesIO(decoded_file))
        img.save(img_path, file_format)
    except Exception as e:
        sys.stderr.write('ERROR: %s\n\n' % str(e))
        sys.exit(2)


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", metavar='PATH', help="input image", required=True)
parser.add_argument("-o", "--output", metavar='PATH', help="output image", required=True)
parser.add_argument("-u", "--url", metavar='URL', help="URL to REST API", required=True)
parser.add_argument("--resize", nargs=2, metavar=('WIDTH', 'HEIGHT'), type=int)
parser.add_argument("--interpolation", help="if resize is selected")
parser.add_argument("--crop", nargs=4, metavar=('X_BEGIN', 'X_END', 'Y_BEGIN', 'Y_END'), type=int)
parser.add_argument("--rotate", metavar='ANGLE_IN_DEGREES', type=int)
parser.add_argument("--scale", help="if rotate is selected", type=float)
parser.add_argument("--negative", action="store_true")
args = parser.parse_args()

if args.resize:
    url_augmentation = f"resize?width={args.resize[0]}&height={args.resize[1]}"
    if args.interpolation:
        url_augmentation += f"&interpolation={args.interpolation}"
elif args.crop:
    url_augmentation = f"crop?xBegin={args.crop[0]}&xEnd={args.crop[1]}&yBegin={args.crop[2]}&yEnd={args.crop[3]}"
elif args.rotate:
    url_augmentation = f"rotate?angle={args.rotate}"
    if args.scale:
        url_augmentation += f"&scale={args.scale}"
elif args.negative:
    url_augmentation = "negative"
else:
    message = 'You need to choose one of the following: --resize, --crop, --rotate, --negative'
    sys.stderr.write('ERROR: %s\n\n' % message)
    parser.print_help()
    sys.exit(2)

encoded_img = encode_image(args.input)

data = {'image': encoded_img}
url = f"{args.url}/augmentation/{url_augmentation}"

encoded_img = send_request(url, data)
save_image(encoded_img, args.output)

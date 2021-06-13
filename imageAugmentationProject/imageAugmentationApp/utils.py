import base64

import numpy as np
import cv2
import imghdr

from PIL import Image
from io import BytesIO

class WrongFormatException(Exception):
    '''
        Raised when the file format is invalid.
    '''
    
    def __init__(self, file_format: str, accepted_formats :tuple):
        self.message = f"'{file_format}' format is not accepted. Accepted file formats: {accepted_formats}"
        super().__init__(self.message)

def resize(encoded_img: str, width: int=None, height: int=None, interpolation: str=None) -> str:
    file_format = get_file_format(encoded_img)
    interpolation = get_interpolation_from_str(interpolation)
    
    img = decode_image(encoded_img)

    width = img.shape[1] if width is None else width
    height = img.shape[0] if height is None else height

    img = cv2.resize(img, (width, height), interpolation=interpolation)

    return encode_image(img, file_format)

def crop(encoded_img: str, xBegin: int=0, xEnd: int=None, yBegin: int=0, yEnd:int=None) -> str:

    file_format = get_file_format(encoded_img)

    img = decode_image(encoded_img)

    xEnd = img.shape[1] if xEnd is None else xEnd
    yEnd = img.shape[0] if yEnd is None else yEnd
    
    img = img[yBegin:yEnd, xBegin:xEnd]

    return encode_image(img, file_format)

def rotate(encoded_img: str, angle: int, scale: float=1.0) -> str:
    file_format = get_file_format(encoded_img)

    img = decode_image(encoded_img)

    height, width = img.shape[:2]
    center = (width // 2, height // 2)
    M = cv2.getRotationMatrix2D(center, angle, scale)
    img = cv2.warpAffine(img, M, (height, width))

    return encode_image(img, file_format)

def negative(encoded_img: str) -> str:
    file_format = get_file_format(encoded_img)

    img = Image.open(BytesIO(base64.b64decode(encoded_img)))

    for i in range(0, img.size[0]-1):
        for j in range(0, img.size[1]-1):
            pixels = img.getpixel((i,j))
            red = 255 - pixels[0]
            green = 255 - pixels[1]
            blue = 255 - pixels[2]

            img.putpixel((i,j),(red, green, blue))

    buffered = BytesIO()
    img.save(buffered, format=file_format)
    return base64.b64encode(buffered.getvalue())

def get_file_format(encoded_file: str, accepted_formats: tuple=('jpeg', 'png', 'bmp')) -> str:
    try:
        decoded_file = base64.b64decode(encoded_file)
        file_format = imghdr.what(None, h=decoded_file)
    except Exception:
        file_format = 'unknown'
    
    if file_format not in accepted_formats:
        raise WrongFormatException(file_format, accepted_formats)
    
    return file_format

def decode_image(encoded_image: str) -> np.ndarray:
    '''
        Decode image encoded in base64 to numpy.ndarray
    '''

    nparr = np.fromstring(base64.b64decode(encoded_image), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

def encode_image(decoded_image: np.ndarray, img_format: str) -> str:
    '''
        Encode image saved in numpy.ndarray to base64
    '''

    retval, buffer = cv2.imencode('.' + img_format, decoded_image)
    return base64.b64encode(buffer).decode()

def get_interpolation_from_str(val: str) -> int:
    if val == 'INTER_NEAREST':
        return cv2.INTER_NEAREST
    elif val == 'INTER_AREA':
        return cv2.INTER_AREA
    elif val == 'INTER_CUBIC':
        return cv2.INTER_CUBIC
    elif val == 'INTER_LANCZOS4':
        return cv2.INTER_LANCZOS4
    else:
        return cv2.INTER_LINEAR

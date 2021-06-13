from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .utils import (resize, crop, rotate, negative, WrongFormatException)

@api_view(['GET'])
def resizeView(request):
    '''
        Returns encoded (base64) resized image.

        Required:
        - encoded (base64) image (formats: ".jpg", ".png", ".bmp") in JSON body
        - at least one of the following parameters: 
            - width (integer) - default: width of an original image
            - height (integer) - default: height of an original image

        Optional:
        - inerpolation parameter:
            - "INTER_LINEAR" for bilinear interpolation (default)
            - "INTER_NEAREST" for nearest-neighbor interpolation
            - "INTER_AREA" for resampling using pixel area relation
            - "INTER_CUBIC" for bicubic interpolation over 4x4 pixel neighborhood
            - "INTER_LANCZOS4" for Lanczos interpolation over 8x8 pixel neighborhood
    '''

    encoded_img = request.data.get('image')
    width = request.query_params.get('width')
    height = request.query_params.get('height')
    interpolation = request.query_params.get('interpolation')
    
    width = int(width) if width and width.isdigit() else None
    height = int(height) if height and height.isdigit() else None

    if any([
        not encoded_img, 
        not width and not height
    ]):
        message = "You must provide an image file and at least one of the ".join((
            "following parameters: width or height."))
        data = {
            "error": message
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    try:
        img = resize(encoded_img, width, height, interpolation)
    except WrongFormatException as e:
        data = { "error": e.message }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    data = { "image" : img }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def cropView(request):
    '''
        Returns encoded (base64) cropped image.

        Required:
        - encoded (base64) image (formats: ".jpg", ".png", ".bmp") in JSON body

        Optional parameters:
        - xBegin    (integer) - default: 0
        - xEnd      (integer) - default: width of an original image
        - yBegin    (integer) - default: 0
        - yEnd      (integer) - default: height of an original image
    '''

    encoded_img = request.data.get('image')

    if not encoded_img:
        message = "You must provide an image file."
        data = { "error": message }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    xBegin = request.query_params.get('xBegin')
    xEnd = request.query_params.get('xEnd')
    yBegin = request.query_params.get('yBegin')
    yEnd = request.query_params.get('yEnd')
    
    xBegin = int(xBegin) if xBegin and xBegin.isdigit() else 0
    xEnd = int(xEnd) if xEnd and xEnd.isdigit() else None
    yBegin = int(yBegin) if yBegin and yBegin.isdigit() else 0
    yEnd = int(yEnd) if yEnd and yEnd.isdigit() else None
    
    try:
        img = crop(encoded_img, xBegin, xEnd, yBegin, yEnd)
    except WrongFormatException as e:
        data = { "error": e.message }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    data = { "image" : img }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def rotateView(request):
    '''
        Returns encoded (base64) rotated image.

        Required:
        - encoded (base64) image (formats: ".jpg", ".png", ".bmp") in JSON body
        - angle parameter (integer except zero)

        Optional:
        - scale parameter (float number) - default: 1.0
    '''

    encoded_img = request.data.get('image')
    angle = request.query_params.get('angle')
    scale = request.query_params.get('scale')

    try:
        angle = int(angle)
    except:
        angle = 0

    try:
        scale = float(scale)
    except:
        scale = 1.0

    if not encoded_img or angle == 0:
        data = {
            "error": "You must provide an image file and an angle"
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    try:
        img = rotate(encoded_img, angle, scale)
    except WrongFormatException as e:
        data = { "error": e.message }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    data = { "image" : img }
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def negativeView(request):
    '''
        Returns encoded (base64) image after negative transformation.

        Required:
        - encoded (base64) image (formats: ".jpg", ".png", ".bmp") in JSON body
    '''

    encoded_img = request.data.get('image')

    if not encoded_img:
        data = {
            "error": "You must provide an image file"
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    try:
        img = negative(encoded_img)
    except WrongFormatException as e:
        data = { "error": e.message }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    data = { "image" : img }
    return Response(data, status=status.HTTP_200_OK)

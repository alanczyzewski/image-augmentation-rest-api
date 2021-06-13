# Image augmentation REST API
## REST API with Django REST Framework
#### Run
To run this project go to imageAugmentationProject/ directory and run the following command:
> python manage.py runserver

This command would start the server at http://127.0.0.1:8000/

#### Endpoints
Each endpoint takes JSON Object as the request body. The object have to contain pair: "image" and plain text image encoded with base64 algorithm (allowable image formats: ".jpg", ".png", ".bmp"). In the response body, each endpoint returns JSON Object with an augmented image.

Example body (request or response):
```
{
	"image": "someimageencodedwithbase64"
}
```

###### GET /augmentation/resize
The endpoint returns encoded resized image.
Available parameters:
* "width" (integer) - The width of an output image. By default it's equal to the width of an original image.
* "height" (integer) - The height of an output image. By default it's equal to the height of an original image.
* "interpolation" (text) - Acceptable values:
	* "INTER_LINEAR" - Bilinear interpolation *(default)*.
	* "INTER_NEAREST" - Nearest-neighbor interpolation.
	* "INTER_AREA" - Resampling using pixel area relation.
	* "INTER_CUBIC" - Bicubic interpolation over 4x4 pixel neighborhood.
	* "INTER_LANCZOS4" - Lanczos interpolation over 8x8 pixel neighborhood.

Example request:

>GET localhost:8000/augmentation/resize?width=80&height=160&interpolation=INTER_CUBIC HTTP/1.1

###### GET /augmentation/crop
The endpoint returns encoded cropped image.
Available parameters:
* "xBegin" (integer) - The starting x-axis coordinate of the slice. By default it's equal to 0.
* "xEnd" (integer) - The ending x-axis coordinate of the slice. By default it's equal to the width of an original image.
* "yBegin" (integer) - The starting y-axis coordinate of the slice. By default it's equal to 0.
* "yEnd" (integer) - The ending y-axis coordinate of the slice. By default it's equal to the height of an original image.

Example request:

>GET localhost:8000/augmentation/crop?xBegin=0&xEnd=100&yBegin=40&yEnd=150 HTTP/1.1

###### GET /augmentation/rotate
The endpoint returns encoded rotated image. The rotation is performed around the center of an image.
Available parameters:
* "angle" (integer except 0) - The number of (counterclockwise) degrees by which you want to rotate the image. This is **required** parameter.
* "scale" (floating point number) - The scale of the rotating image. By default it's equal to 1.0 (the same dimensions as an input image).

Example request:

>GET localhost:8000/augmentation/rotate?angle=-90&scale=1.5 HTTP/1.1

###### GET /augmentation/negative
The endpoint returns encoded image after negative transformation. This endpoint doesn't take any parameters.

Example request:

>GET localhost:8000/augmentation/negative HTTP/1.1

## Testing script
The script sends a request with an encoded image file and saves received augmented image file. The script is located at testing_script/get_augmentation.py
#### Run
Usage of the script:
> ./get_augmentation.py [options]

Available options:
* -h, --help 
	* shows the help message
* -i PATH, --input PATH
	* takes an input image path relative to testing_script/ ***(required)***
* -o PATH, --output PATH
	* takes an output image path relative to testing_script/ ***(required)***
* -u URL, --url URL
	* takes a URL to REST API ***(required)***
* --resize WIDTH HEIGHT
* --interpolation INTERPOLATION
* --crop X_BEGIN X_END Y_BEGIN Y_END
* --rotate ANGLE_IN_DEGREES
* --scale SCALE
* --negative

Example:

> ./get_augmentation.py -i img_examples/white-king.jpg -o output.jpg --url http://localhost:8000 --resize 50 50

## Used
* python - 3.8.8
* django - 3.2.2
* djangorestframework - 3.12.4
* opencv - 4.5.2
* pillow - 8.0.0
* numpy - 1.19.2
* requests - 2.25.1

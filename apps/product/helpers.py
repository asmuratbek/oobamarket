from io import BytesIO
import os
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

__author__ = 'kolyakoikelov'


def create_thumbnail_image(main_image, thumb_image, thumbnail_size):
    if not main_image:
        return
    if not thumb_image:
        if main_image.name.endswith(".jpg") or main_image.name.endswith(".jpeg"):
            pil_type = 'jpeg'
            file_extension = 'jpg'
            image_type = 'image/jpeg'

        elif main_image.name.endswith(".png"):
            pil_type = 'png'
            file_extension = 'png'
            image_type = 'image/png'
        elif main_image.name.endswith(".gif"):
            pil_type = 'gif'
            file_extension = 'gif'
            image_type = 'image/gif'
        else:
            pil_type = 'jpeg'
            file_extension = 'jpg'
            image_type = 'image/jpeg'

        image = Image.open(BytesIO(main_image.read()))
        image.thumbnail(thumbnail_size, Image.ANTIALIAS)
        output = BytesIO()
        image.save(output, pil_type)
        output.seek(0)
        thumbnail_image = SimpleUploadedFile(os.path.split(main_image.name)[-1], output.read(), content_type=image_type)
        thumb_image.save('%s_thumbnail.%s' % (os.path.splitext(main_image.name)[0], file_extension),
                         thumbnail_image, save=False)

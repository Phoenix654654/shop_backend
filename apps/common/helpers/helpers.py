import os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


def process_and_resize_image(image_path, resize_dimensions, format='JPEG', quality=90):
    with Image.open(image_path) as pil_image:
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        pil_image = pil_image.resize(resize_dimensions)

        buffer = BytesIO()
        pil_image.save(fp=buffer, format=format, quality=quality)
        buffer.seek(0)

        image_file = ContentFile(buffer.read())
        filename = os.path.basename(image_path)

        return image_file, filename

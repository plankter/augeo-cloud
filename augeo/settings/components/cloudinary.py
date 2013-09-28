from os import environ

# See: http://cloudinary.com/documentation/django_integration#getting_started_guide
INSTALLED_APPS += (
    'cloudinary',
)

import cloudinary

cloudinary.config(
    cloud_name=environ['CLOUDINARY_CLOUD_NAME'],
    api_key=environ['CLOUDINARY_API_KEY'],
    api_secret=environ['CLOUDINARY_API_SECRET']
)
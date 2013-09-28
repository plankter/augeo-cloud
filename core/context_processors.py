import cloudinary

def consts(request):
    return dict(
        THUMBNAIL = {
            "crop": "fit", "width": 240,
        },
        CLOUDINARY_CLOUD_NAME = cloudinary.config().cloud_name
    )
from PIL import Image
from PIL.ExifTags import TAGS

def extract_exif(file_path):
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()

        if not exif_data:
            print("No EXIF metadata found.")
            return {}

        readable_exif = {}
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            readable_exif[tag] = value

        return readable_exif

    except Exception as e:
        print("Error extracting EXIF:", e)
        return {}

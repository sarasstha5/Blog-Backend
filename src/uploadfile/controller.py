from PIL import Image
from fastapi import HTTPException


def uploadfile(file):
    try:
        image = Image.open(file.file)
        image.verify()

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid image file"
        )

    return{
        "filename":file.filename,
        "content-type":file.content_type,
        "valid": "valid image"
    }
    

from PIL import Image
from pathlib import Path
from uuid import uuid4
from fastapi import HTTPException, UploadFile

UPLOAD_DIR = Path("media/post")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
#validate if it is image
def validate_image(image: UploadFile):
    allowed_types = {"image/jpeg", "image/png", "image/webp"}

    if image.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only JPEG, PNG and WEBP images are allowed",
        )

    try:
        opened_image = Image.open(image.file)
        opened_image.verify()
    
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid image file"
        )
    
    image.file.seek(0)

#store image to folder
def save_image(image:UploadFile):
    filename = f"{uuid4().hex}_{image.filename}"
    file_path = UPLOAD_DIR / filename
    #store to the media/posts
    # with open(file_path, "wb") as buffer:
    #     buffer.write(image.file.read())
    img = Image.open(image.file)
    #resize image
    img.thumbnail((1600, 1600))                 
    #compress and save to folder
    if img.format == "JPEG":
        img.save(file_path, quality=80, optimize=True)

    elif img.format == "PNG":
        img.save(file_path, optimize=True)

    return str(file_path)

#delete the image from the folder too
def delete_image(image_url:str):
    if not image_url:
        return

    file_path = Path(image_url)

    if file_path.exists():
        file_path.unlink()

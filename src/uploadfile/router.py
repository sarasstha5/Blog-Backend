from fastapi import APIRouter,UploadFile,File
from src.uploadfile import controller


router = APIRouter(prefix="/uploadfile", tags=["uploadFile"])

@router.post("/")
def uploadFile(file: UploadFile = File(...)):
    return controller.uploadfile(file)

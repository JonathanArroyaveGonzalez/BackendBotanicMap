from fastapi import APIRouter, File, UploadFile, Depends
from ..environment import serviceAccountKey
from ..services.storageService import FirebaseStorageService

# Create a router for image-related endpoints
router = APIRouter(prefix="/images", tags=["images"])

# Initialize Firebase Storage Service
"""
storage_service = FirebaseStorageService(
    cred=env.cred, 
    bucket_name='my-project-4848-1683442933444.firebasestorage.appspot.com'
)"""
storage_service = FirebaseStorageService()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Endpoint to upload an image to Firebase Storage
    
    :param file: Image file to upload
    :return: Dictionary with the public URL of the uploaded image
    """
    try:
        # Upload the image and get its public URL
        image_url = await storage_service.upload_image(file)
        
        return {
            "status": "success",
            "url": image_url
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


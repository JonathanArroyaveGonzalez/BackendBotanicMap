import os
import uuid
from io import BytesIO
from fastapi import UploadFile, HTTPException
import firebase_admin
from firebase_admin import credentials, storage
from google.cloud import storage as gcs
from ..environment import serviceAccountKey

class FirebaseStorageService:
    def __init__(self):
        """
        Initialize Firebase Storage service
        """
        # Check if Firebase app is already initialized to prevent duplicate initialization
        if not firebase_admin._apps:
            firebase_admin.initialize_app(
                credential=serviceAccountKey.cred, 
                options={
                    'storageBucket': 'my-project-4848-1683442933444.firebasestorage.appspot.com'
                }
            )
        self.bucket_name = 'my-project-4848-1683442933444.firebasestorage.app'
        # Get the default bucket correctly
        self.bucket = storage.bucket(self.bucket_name)
        self.configure_cors()

    def configure_cors(self):
        """
        Configure CORS for Firebase Storage bucket
        """
        cors_configuration = [{
            "origin": ["*"],
            "responseHeader": ["Content-Type"],
            "method": ["GET", "HEAD", "PUT", "POST", "DELETE"],
            "maxAgeSeconds": 3600
        }]
        
        # Set the CORS configuration on the bucket
        self.bucket.cors = cors_configuration
        self.bucket.patch()

    async def upload_image(self, file: UploadFile) -> str:
        """
        Upload an image to Firebase Storage
        
        :param file: UploadFile from FastAPI
        :return: Public URL of the uploaded image
        """
        try:
            # Validate file is an image
            if not file.content_type.startswith('image/'):
                raise HTTPException(status_code=400, detail="File must be an image")

            # Generate unique filename
            file_extension = file.content_type.split('/')[-1]
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            
            # Create a new blob and upload the file's content
            blob = self.bucket.blob(unique_filename)
            
            # Read the contents of the uploaded file
            contents = await file.read()
            
            # Upload file to Firebase Storage
            blob.upload_from_string(
                contents, 
                content_type=file.content_type
            )
            
            # Make the blob publicly accessible
            blob.make_public()
            
            # Return the public URL
            return blob.public_url

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
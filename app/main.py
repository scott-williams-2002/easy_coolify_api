from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Header
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
import shutil
import tempfile
import logging
#from .utils import images_to_video

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_KEY = os.environ.get('API_KEY', 'default-secret')

app = FastAPI()

# Set up CORS
# In production, you should restrict this to the specific domains that need access.
origins = [
    # Add the URL of your n8n instance here. For example:
    "https://n8n.scottbot.party/",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        logger.warning("Invalid API Key received.")
        raise HTTPException(status_code=403, detail="Invalid API KEY")

@app.get("/test")
async def test_endpoint():
    logger.info("Test endpoint called.")
    return {"message": "Test endpoint is working"}

@app.post("/make_video", dependencies=[Depends(verify_api_key)])
async def make_video(files: List[UploadFile] = File(...)):
    logger.info(f"make_video endpoint called with {len(files)} file(s).")
    # For now, this returns a generic video file.
    # In the future, you can implement the logic to process the uploaded files.
    video_path = "app/test.mp4"
    if not os.path.exists(video_path):
        logger.error(f"Video file not found at path: {video_path}")
        raise HTTPException(status_code=404, detail="Video not found")
    
    logger.info("Request successful, returning video file.")
    return FileResponse(video_path, media_type="video/mp4", filename="output.mp4") 
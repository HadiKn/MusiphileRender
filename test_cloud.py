import os
from decouple import config
import cloudinary
import cloudinary.uploader
from datetime import datetime, timezone

# Disable timestamp check
os.environ['CLOUDINARY_DISABLE_TIMESTAMPS'] = '1'

# Configure Cloudinary
cloudinary.config(
    cloud_name=config('CLOUDINARY_CLOUD_NAME'),
    api_key=config('CLOUDINARY_API_KEY'),
    api_secret=config('CLOUDINARY_API_SECRET'),
    secure=True
)

def test_upload():
    try:
        # Test with a simple image upload
        result = cloudinary.uploader.upload(
            "https://res.cloudinary.com/demo/image/upload/sample.jpg",
            public_id=f"test_upload_{datetime.now(timezone.utc).timestamp()}"
        )
        print("✅ Cloudinary is working!")
        print("Uploaded URL:", result['secure_url'])
        return True
    except Exception as e:
        print("❌ Error with Cloudinary:", str(e))
        return False

if __name__ == "__main__":
    test_upload()
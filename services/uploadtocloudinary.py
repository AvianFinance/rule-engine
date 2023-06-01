import cloudinary
from cloudinary.uploader import upload

def upload_txt_to_cloudinary(file_path, public_id):
    cloudinary.config(
        cloud_name='YOUR_CLOUD_NAME',
        api_key='YOUR_API_KEY',
        api_secret='YOUR_API_SECRET'
    )

    response = upload(
        file_path,
        resource_type='raw',
        public_id=public_id,
        overwrite=True
    )

    if 'url' in response:
        return response['url']

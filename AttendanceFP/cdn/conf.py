import os

import AttendanceFP.cdn.backend

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = os.getenv('AWS_S3_ENDPOINT_URL')

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl":"max-age=86400",
}

AWS_LOCATION = os.getenv('AWS_LOCATION')

DEFAULT_FILE_STORAGE = 'AttendanceFP.cdn.backend.MediaRootS3Boto3Storage'
STATICFILES_STORAGE = 'AttendanceFP.cdn.backend.StaticRootS3Boto3Storage'




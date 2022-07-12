import os

import AttendanceFP.cdn.backend

AWS_ACCESS_KEY_ID = 'VRYBATD7CLQXMEZKJRIZ'
AWS_SECRET_ACCESS_KEY = '3adNDfzk5ZsOtBU6YWxFxX1c80ffa3clDwXtn49OPdM'
AWS_STORAGE_BUCKET_NAME = 'appstaticfiles'
AWS_S3_ENDPOINT_URL = 'https://sfo3.digitaloceanspaces.com'

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl":"max-age=86400",
}

AWS_LOCATION = 'https://appstaticfiles.sfo3.digitaloceanspaces.com'

DEFAULT_FILE_STORAGE = 'AttendanceFP.cdn.backend.MediaRootS3Boto3Storage'
STATICFILES_STORAGE = 'AttendanceFP.cdn.backend.StaticRootS3Boto3Storage'




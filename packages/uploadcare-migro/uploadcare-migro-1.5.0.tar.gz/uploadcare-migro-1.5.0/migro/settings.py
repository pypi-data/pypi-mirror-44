"""

    migro.settings
    ~~~~~~~~~~~~~~

    Utility settings.

"""
# Upload base url.
UPLOAD_BASE = 'https://upload.uploadcare.com/'

# Project public key.
PUBLIC_KEY = None

# Timeout for status check of file uploaded by `from_url`.
# If you have big files - you can increase this option.
FROM_URL_TIMEOUT = 30

# Maximum number of concurrent upload requests
MAX_CONCURRENT_UPLOADS = 20

# Time to wait before next status check, seconds.
STATUS_CHECK_INTERVAL = 0.3

# Throttling timeout sleep interval
THROTTLING_TIMEOUT = 5.0

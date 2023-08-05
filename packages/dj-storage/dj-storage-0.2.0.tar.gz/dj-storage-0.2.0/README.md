# Nice file storage support for Django

This is a single, generic file storage backend for Django, for storing the files on any storage service with a HTTP/REST API.

Both **Google Storage** and **AWS S3** provide HTTP/REST API for file storage.

The only thing that differs between the services is the authentication method. Both Google and AWS use their own propertiary authentication methods, that have to be implemented. **Right now only Google Storage auth is implemented.**

## Requirements
* Django 2.0+

## Installation
```sh
pip install dj-storage
```

### settings.py
* Set `DEFAULT_FILE_STORAGE = 'dj_storage.HTTPStorage'`
* Set `MEDIA_URL = 'https://storage.googleapis.com/your-bucket-name/'`
* Provide [GCP Application Default Credentials](https://cloud.google.com/docs/authentication/production)

## Planned features
* Support for AWS S3 auth - requires fixing [aws-requests-auth #45](https://github.com/DavidMuller/aws-requests-auth/issues/45)
* Support for standard auth mechanisms (like HTTP Basic auth)


## Usage Info

The variables `client_id` and `client_secret` are how Google identify your application. These are specified in the initialization parameters or in the `client_secrets.json` file.
The variables `access_token` and `refresh_token` are how Google's APIs differentiate between different YouTube channels. These are specified in the authenticate method.

This module uploads a given video to a youtube channel, as such there are 2 things this module needs. 
- A video
- Video Options
  - Title
  - Description
  - Tags
  - Category
  - Status
  - DeclaredMadeForKids
  
- A channel to upload to(In the form of a authentication file)

- The authentication file should contain the following:
  - access_token: token_here
  - refresh_token: token_here
  - scope: scope_here
  - token_type: Bearer
  - expires_in: 3599

This file should be called client_secrets.json and exist in the directory this script is.

# Quick Start

## 0. Importing the package 
```python
# youtube upload api
from youtube_upload.client import YoutubeUploader
```

## 1. Instantiating an uploader
```python
uploader = YoutubeUploader(client_id,client_secret)
```
*or*
```python
uploader = YoutubeUploader()
```
If a client_secrets.json is present in the current working directory (downloaded from the [Credentials Control Panel](https://console.developers.google.com/apis/credentials) in the Google Cloud Console when you create the application). 
*or*
```python
uploader = YoutubeUploader(secrets_file_path=secrets_file_path_here)
```
You can specify the path to the file with the [`secrets_file_path`](https://pillargg.github.io/youtube-upload/YoutubeUploader/#youtube_upload.client.YoutubeUploader) parameter.

## 2. Authentication

If you run [`authenticate`](https://pillargg.github.io/youtube-upload/YoutubeUploader/#youtube_upload.client.YoutubeUploader.authenticate) with no parameters and no `oauth.json`, it opens a web page locally that you can use to sign into the YouTube Channel you want to upload the video to. 


```python
uploader.authenticate()
```
*or*
```python
uploader.authenticate(access_token=access_token_here, refresh_token=refresh_token_here)
```
*OR*
```python
uploader.authenticate(oauth_path='oauth.json')
```

## 3. Uploading the video
```python

# Video options
options = {
    "title" : "Example title", # The video title
    "description" : "Example description", # The video description
    "tags" : ["tag1", "tag2", "tag3"],
    "categoryId" : "22",
    "privacyStatus" : "private", # Video privacy. Can either be "public", "private", or "unlisted"
    "kids" : False # Specifies if the Video if for kids or not. Defaults to False.
    "thumbnailLink" : "https://cdn.havecamerawilltravel.com/photographer/files/2020/01/youtube-logo-new-1068x510.jpg" # Optional. Specifies video thumbnail.
}

# upload video
uploader.upload(file_path, options) 
```
Parameter `tags` should be list of strings only. The parameter `categoryId` refers to YouTube internal categories, more information can be found [here](https://stackoverflow.com/questions/17698040/youtube-api-v3-where-can-i-find-a-list-of-each-videocategoryid). 
## 4. Closing the uploader
```python
uploader.close()
```

This method deletes the OAuth JSON file. Omit this function if you do not desire that behavior.

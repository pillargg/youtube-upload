![Build Docs](https://github.com/pillargg/youtube-upload/workflows/Build%20Docs/badge.svg?branch=master) ![Upload Python Package](https://github.com/pillargg/youtube-upload/workflows/Upload%20Python%20Package/badge.svg)

# PillarGG YouTube Uploader
Upload Youtube Videos and more via Python.

# Getting Started

![](https://thumbs.gfycat.com/ConventionalSecondhandGemsbuck-size_restricted.gif)

`pip install pillar-youtube-upload`

You can read more [below](https://github.com/pillargg/youtube-upload#usage) and on the [docs](https://pillargg.github.io/youtube-upload/YoutubeUploader/).

This project uses the [Youtube Data API](https://developers.google.com/youtube/v3/docs/videos/insert).

All implementations of youtube upload needs some form of [authentication](https://developers.google.com/youtube/v3/guides/authentication).

## Client Side youtube upload
To upload youtube videos as a client, you need to follow [this guide](https://developers.google.com/youtube/v3/guides/auth/client-side-web-apps).


## Server Side youtube upload
To upload youtube videos as a server, you need to follow [this guide](https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps).


## Getting a youtube api key
1. First, you need to go to [this website](https://console.developers.google.com/apis/library).
2. If prompted, select a project, or create a new one.
3. Use the Library page to find and enable the YouTube Data API v3. 
4. Go to the [credentials page](https://console.developers.google.com/apis/credentials).
5. Click `Create Credentials > OAuth client ID`.
6. Select the Web application app type.
7. Fill in the form and click create. For testing redirect URIs that refer to the local machine with `http://localhost:8080`. 
8. Download the client_secret.json file from the API Console and securely store the file in a location that only your application can access. By default, the application gets this file from the directory your script is being ran in. The path can also be changed when the class `YoutubeUploader` is being initialized.
8. Get your `client_id` and `client_secret`.

We recommend that you [design your app's auth endpoints](https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps#protectauthcode) so that your application does not expose authorization codes to other resources on the page.

The key must have the scope 'https://www.googleapis.com/auth/youtube.upload'.


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

# Usage

### 0. Importing the package 
```python
# youtube upload api
from youtube_upload.client import YoutubeUploader
```

### 1. Instantiating an uploader
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

### 2. Authentication

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

### 3. Uploading the video
```python

# Video options
options = {
    "title" : "Example title", # The video title
    "description" : "Example description", # The video description
    "tags" : ["tag1", "tag2", "tag3"],
    "categoryId" : "22",
    "privacyStatus" : "private", # Video privacy. Can either be "public", "private", or "unlisted"
    "kids" : False, # Specifies if the Video if for kids or not. Defaults to False.
    "thumbnailLink" : "https://cdn.havecamerawilltravel.com/photographer/files/2020/01/youtube-logo-new-1068x510.jpg" # Optional. Specifies video thumbnail.
}

# upload video
uploader.upload(file_path, options) 
```
Parameter `tags` should be list of strings only. The parameter `categoryId` refers to YouTube internal categories, more information can be found [here](https://stackoverflow.com/questions/17698040/youtube-api-v3-where-can-i-find-a-list-of-each-videocategoryid). 
### 4. Closing the uploader
```python
uploader.close()
```

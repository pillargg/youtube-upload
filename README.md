# PillarGG YouTube Uploader
Upload Youtube Videos and more via Python.

# Getting Started

`pip install pillar-youtube-upload`

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
8. Download the client_secret.json file from the API Console and securely store the file in a location that only your application can access. By default, the application gets this file from the directory your script is being ran in. The path can also be changed when the class `YouTubeUploader` is being initialized.
8. Get your `client_id` and `client_secret`.

We recommend that you [design your app's auth endpoints](https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps#protectauthcode) so that your application does not expose authorization codes to other resources on the page.

The key must have the scope 'https://www.googleapis.com/auth/youtube.upload'.


## Usage Info

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

This file should be called client_secrets.sjon and exist in the directory this script is.

## Usage

```python
# youtube upload api
from youtube_upload.client import YouTubeUploader

uploader = YoutubeUploader(client_id,client_secret)
uploader.authenticate()

# Video options
options = {
    title : "Example title",
    description : "Example description",
    tags : ["tag1", "tag2", "tag3"],
    categoryId : "22",
    privacyStatus : "private",
    kids : False
    thumbnailLink : "https://cdn.havecamerawilltravel.com/photographer/files/2020/01/youtube-logo-new-1068x510.jpg"
}

# upload video
uploader.upload(file_path, options) 
```

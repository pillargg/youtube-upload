import json
import os
import time
import uuid

import httplib2
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

from youtube_upload import (MAX_RETRIES, MISSING_CLIENT_SECRETS_MESSAGE,
                            RETRYABLE_EXCEPTIONS, RETRYABLE_STATUS_CODES,
                            VALID_PRIVACY_STATUSES, YOUTUBE_API_SERVICE_NAME,
                            YOUTUBE_API_VERSION, YOUTUBE_UPLOAD_SCOPE)
from youtube_upload.oauth_template import oauth_template


class YoutubeUploader():
    '''
    The YouTube Uploader client.

    When using in a multithreaded environment, please create a new instance of the `YoutubeUploader` class per thread.
    '''

    def __init__(
        self,
        client_id="",
        client_secret="",
        secrets_file_path=os.path.join(
            '.',
            'client_secrets.json')):
        '''
        Initialization Function for the class. 

        The variables `client_id` and `client_secret` can be passed in when the class is initialized, this will have the function generate the `client_secrets.json` file. 

        If you do not pass the variables in, the class will look for a `client_secrets.json` file in the same direction in which the script is being initialized. You can instead
        pass in a directory to where the `client_secrets.json` is with the parameter `secrets_file_path` here is an example `client_secrets.json` file:
        ```json
        {
            "web": {
            "client_id": "",
            "client_secret": "",
            "redirect_uris": [],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://accounts.google.com/o/oauth2/token"
            }
        }
        ```
        '''

        self.client_secrets = {}
        if client_id == "" or client_secret == "":
            self.secrets_file = secrets_file_path
            try:
                with open(secrets_file_path) as f:
                    self.client_secrets = json.loads(f.read())
            except FileNotFoundError:
                raise
        else:
            self.client_secrets = {
                'web': {
                    'redirect_uris': [],
                    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                    'token_uri': 'https://accounts.google.com/o/oauth2/token',
                    'client_id': client_id,
                    'client_secret': client_secret
                }
            }
            with open(secrets_file_path, 'w') as f:
                f.write(json.dumps(self.client_secrets))
            self.secrets_file = secrets_file_path

        self.youtube = None
        self.options = None
        self.flow = None
        self.credentials = None
        self.oauth_path = 'oauth.json'

        self.max_retry = MAX_RETRIES

    def __del__(self):
        self.close()

    # This is if you have another OAuth file to use
    def authenticate(self, oauth_path='oauth.json', access_token=None, refresh_token=None):
        '''
        This method authenticates the user with Google's servers. If you give no path, the method will look for the `oauth.json` file in the current working directory.

        If a path is given, and the file does not exist at that path, the file will be created at that path. If the file does exist at the given path, it will be used.

        If in the case that you do not have an OAuth JSON file, you can specify an access and refresh token via the `access_token` and `refresh_token` parameters.

        '''

        self.oauth_path = oauth_path
        # If access_token and refresh_token is provided, create new oauth.json
        if access_token is not None and refresh_token is not None:
            if '.json' not in oauth_path and os.path.isdir(oauth_path):
                # https://stackoverflow.com/questions/2961509/python-how-to-create-a-unique-file-name
                self.oauth_path = os.path.join(
                    oauth_path, str(uuid.uuid4()) + '.json')
            else:
                self.oauth_path = str(uuid.uuid4()) + '.json'
            subs = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'client_id': self.client_secrets['web'].get('client_id'),
                'client_secret': self.client_secrets['web'].get('client_secret')
            }
            oauth_json_str = oauth_template.substitute(subs)
            with open(self.oauth_path, 'w') as f:
                f.write(oauth_json_str)

        self.flow = flow_from_clientsecrets(
            self.secrets_file,
            scope=YOUTUBE_UPLOAD_SCOPE,
            message=MISSING_CLIENT_SECRETS_MESSAGE)
        storage = Storage(self.oauth_path)
        self.credentials = storage.get()

        # Catches the edge case where no credentials were provided
        if self.credentials is None or self.credentials.invalid:
            # this wil only run if there is no callback function
            self.credentials = run_flow(self.flow, storage)

        self.youtube = build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            http=self.credentials.authorize(
                httplib2.Http()))

    def upload(self, file_path, options={}, chunksize=(-1)):
        '''
        This uploads the file to YouTube. The only required argument is the `file_path`, which is the path to the video to be uploaded. 

        The `options` parameter is a dictionary of options. The items are pretty self explanatory, here is an example options dictionary:
        ```Python
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
        ```

        The parameter, `chunk_size` is the max size of the HTTP request to send the video. This parameter is in bytes, and if set to `-1`, which is the default, it 
        will send the video in one large request. Set this to a different value if you are having issues with the upload failing. 

        You can also add a callback function for the case where the upload were to fail. This is mainly for custom error handling and prompting users to re-authenticate. 

        The callback function is the parameter `noauth_callback`. The function passed should be able to accept a tuple of arguments. The parameter `noauth_args` is the arguments for the function. Here 
        is an example of the callback function being used.

        ```Python
        from youtube_upload.client import YoutubeUploader

        def callback(*args):
            print(args[0], args[1])

        with YoutubeUploader() as youtube:
            youtube.authenticate()
            youtube.upload("test.mp4", noauth_callback=callback, noauth_args=("It failed."))
        ```

        And here is the example output in the case that the upload would fail.

        ```
        It failed. invalid_grant: Bad Request
        ```
        '''
        body = {
            'snippet': {
                'title': options.get('title', 'Test Title'),
                'description': options.get('description', 'Test Description'),
                'tags': options.get('tags'),
                'categoryId': options.get('category', '22')
            },
            'status': {
                'privacyStatus': options.get('privacyStatus', VALID_PRIVACY_STATUSES[0]),
                'selfDeclaredMadeForKids': options.get('kids', False)
            }
        }

        insert_request = self.youtube.videos().insert(
            part=",".join(
                list(
                    body.keys())), body=body, media_body=MediaFileUpload(
                file_path, chunksize=chunksize, resumable=True))

        self._resumable_upload(
            insert_request, bool(
                options.get('thumbnailLink')), options)

    def _resumable_upload(self, insert_request, uploadThumbnail, options):
        response = None
        error = None
        retry = 0

        while response is None:
            try:
                _, response = insert_request.next_chunk()
                if 'id' in response:
                    video_id = response.get('id')
                    if uploadThumbnail:
                        request = self.youtube.thumbnails().set(
                            videoId=video_id, media_body=MediaFileUpload(
                                options.get('thumbnailLink')))
                        response = request.execute()
                        print(response)
                else:
                    raise HttpError(f'Unexpected response: {response}')
            except HttpError as e:
                if e.resp.status in RETRYABLE_STATUS_CODES:
                    error = "A retryable HTTP error %d occurred:\n%s" % (
                        e.resp.status, e.content)
                else:
                    raise
            except RETRYABLE_EXCEPTIONS as e:
                error = "A retryable error occurred: %s" % e

            if error is not None:
                print(error)
                retry += 1
                if retry > self.max_retry:
                    exit("No longer attempting to retry.")

                print("Sleeping 5 seconds and then retrying...")
                time.sleep(5)

    def close(self):
        '''
        Tears down and closes the class cleanly.
        '''
        if os.path.exists(self.oauth_path):
            os.remove(self.oauth_path)

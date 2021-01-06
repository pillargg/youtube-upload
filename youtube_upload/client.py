import json
import os
import time

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


class YoutubeUploader():
    def __init__(
        self,
        client_id="",
        client_secret="",
        secrets_file_path=os.path.join(
            '.',
            'client_secrets.json')):

        if client_id == "" or client_secret == "":
            self.secrets_file = secrets_file_path
        else:
            client_secrets = {
                'redirect_uris': [],
                'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                'token_uri': 'https://accounts.google.com/o/oauth2/token',
                'client_id': client_id,
                'client_secret': client_secret
            }
            with open(secrets_file_path, 'w') as f:
                f.write(json.dumps(client_secrets))
            self.secrets_file = secrets_file_path

        self.youtube = None
        self.options = None
        self.flow = None
        self.credentials = None

        self.max_retry = MAX_RETRIES

    def authenticate(self):
        self.flow = flow_from_clientsecrets(
            self.secrets_file,
            scope=YOUTUBE_UPLOAD_SCOPE,
            message=MISSING_CLIENT_SECRETS_MESSAGE)
        storage = Storage('oauth.json')
        self.credentials = storage.get()

        if self.credentials is None or self.credentials.invalid:
            # this will have to be changed for auth purposes
            self.credentials = run_flow(self.flow, storage)

        self.youtube = build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            http=self.credentials.authorize(
                httplib2.Http()))

    def upload(self, file_path, options={}, chunksize=(-1)):
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

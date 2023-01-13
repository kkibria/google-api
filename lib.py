from http import client
import httplib2
import os
import random
# import sys
import time
import pickle

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

YOUTUBE_UPLOAD_SCOPE = "youtube.upload"
CLOUD_PLATFORM_SCOPE = "cloud-platform"

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application.

CLIENT_SECRETS_FILE = ".secrets/client_secret.json"


def get_tokens(fetch=False, client_secrets_file=CLIENT_SECRETS_FILE, scope=None):
    token_path = f'.secrets/{scope}_token.pickle'
    credentials = None

    # token.pickle stores the user's credentials from previously successful logins
    if os.path.exists(token_path):
        print('Loading Credentials From File...')
        with open(token_path, 'rb') as token:
            credentials = pickle.load(token)

    # If there are no valid credentials available, then either refresh the token or log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            if not fetch:
                return False

            print('Fetching New Tokens...')

            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file,
                scopes=[
                    f"https://www.googleapis.com/auth/{scope}"
                ]
            )
            flow.run_local_server(port=8080, prompt='consent',
                                  authorization_prompt_message='')
            credentials = flow.credentials

        # Save the credentials for the next run
        with open(token_path, 'wb') as f:
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, f)

    return credentials

    # Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, client.NotConnected,
                        client.IncompleteRead, client.ImproperConnectionState,
                        client.CannotSendRequest, client.CannotSendHeader,
                        client.ResponseNotReady, client.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def get_authenticated_service(scope=YOUTUBE_UPLOAD_SCOPE):
    credentials = get_tokens(scope=scope)
    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                 credentials=credentials)
    #  http=httplib2.Http())


def initialize_upload(youtube, options):
    tags = options.keywords.split(",") if options.keywords else None
    body = dict(
        snippet=dict(
            title=options.title,
            description=options.description,
            tags=tags,
            categoryId=options.category
        ),
        status=dict(
            privacyStatus=options.privacyStatus
        )
    )

    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
    )

    resumable_upload(insert_request)


def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print("Uploading file...")
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print(
                        f"Video id '{response['id']}' was successfully uploaded.")
                else:
                    exit(
                        f"The upload failed with an unexpected response: {response}")
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                     e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = f"A retriable error occurred: {e}"

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print("Sleeping %f seconds and then retrying..." % sleep_seconds)
            time.sleep(sleep_seconds)

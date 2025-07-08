import os.path
import time
import yt_dlp
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

DOCUMENT_ID = 'DOCUMENT ID GOES HERE'
SCOPES = ['https://www.googleapis.com/auth/documents','https://www.googleapis.com/auth/drive']
dlp_settings = {'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320',}], 'outtmpl': '%(title)s.%(ext)s', 'noplaylist': True, 'quiet': True,}

print(" @@-:  %@@  =@@ *@%## @                  @@ @                 @ @@ %            ")
print("@#*@@=:  %@+=*+ :-* @@                  =                      @@  +            ")
print("    @* @@.    .=--  @@  @@  @@ %@  =@@%=@@*@  @@   @+ =@@ @@@  @@+%: @@@ :@@ @@@")
print("   @@++#@.   @@#-@+ @@= *@@  @#@@:@ .-# @@  .* @@ -@. :@@.@@   @%  @* =*  @@.%@ ")
print(" +.     @#  @*   @@ @@   @%  @   #@ :    @     @: .@   #@ @@   @%  @:     +@ %@ ")
print("@@@@@+:--@@ -@@@#   @@= * = -@@. -@@%@   @    .@@ -@@  @@ @@#  @@*#@@@%=  @@ @@%")
print("    #+   .    :*@    * =    .*#:   -#    @     **. *#. =%  #    +    *:   =#  * ")
print("                       @@@@              @                                      ")
print("~*~_~*~*~_~*~*~_~*~*~_~*~*~_~*~*~_~*~*~_~*~*~_~*~*~_~*~*~_~*~*~_~*~*~_~*~*~_~*~*")
#                                                                           by rari_teh
print("Logging in...")

badge = None
if os.path.exists('token.json'):
    badge = Credentials.from_authorized_user_file('token.json', SCOPES)
if not badge or not badge.valid:
    if badge and badge.expired and badge.refresh_token:
        try:
            badge.refresh(Request())
        except:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            badge = flow.run_local_server(port=0)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
        badge = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(badge.to_json())
service_docs = build('docs', 'v1', credentials=badge)
service_drive = build("drive", "v3", credentials=badge)
state = "ready"
print("Online.")

while (True):
    try:
        document = service_docs.documents().get(documentId=DOCUMENT_ID).execute()
        query = document.get("title")
        if query.endswith('$'):
            print(f'Searching for {query[:-1]}...')
            query = f'ytsearch1:"{query[:-1]}"'
            with yt_dlp.YoutubeDL(dlp_settings) as dlp_sess:
                info_dict = dlp_sess.extract_info(query, download=True)
                filename = info_dict['entries'][0]['title'] + ".mp3"
                print(f'Saved {filename[:-4]} ({info_dict["entries"][0]["id"]}) successfully. Uploading...')
                try:
                    media = MediaFileUpload(info_dict['entries'][0]['requested_downloads'][0]['filepath'], resumable=True)
                    drive_item = service_drive.files().create(body={"name": filename}, media_body=media, fields="id").execute()
                    print(f'Uploaded file: {drive_item.get("id")}')
                    os.remove(filename)
                except:
                    state = "error"
                    print("Upload/file error")
                
            service_drive.files().update(fileId=DOCUMENT_ID, body={'name': f'!rf - {state}'}).execute()
            state = "ready"
            print("Ready.")
    except:
        if badge.expired and badge.refresh_token:
            try:
                badge.refresh(Request())
            except:
                flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
                badge = flow.run_local_server(port=0)
        print("Error! Retrying in 10s")
    time.sleep(10)
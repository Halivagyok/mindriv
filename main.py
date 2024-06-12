import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

from datetime import datetime

tim = datetime.now()
time = tim.strftime('%Y.%m.%d.%H:%M')

# Define the scopes required for accessing Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

#engedely vizsgalata
def authenticate():
    """Authenticate and authorize the user."""
    creds = None

    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def upload_file(file_path , folder_id):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id] if folder_id else None
        }
    # Upload the file
    media = MediaFileUpload(file_path)
    file = service.files().create(body=file_metadata, media_body=media).execute()
    #print(f'File uploaded: {file["name"]} ({file["id"]})')

def folder(folder_path, parent):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    parent_id = parent
    folder_name = time + " " + os.getenv("USERNAME")

    folder_metadata = {
        'name': folder_name,
        'parents': [parent_id],
        'mimeType': 'application/vnd.google-apps.folder'    
    }

    created_folder = service.files().create(body=folder_metadata).execute()
    print(f'Folder "{folder_name}" created with ID: {created_folder["id"]}')
    id = created_folder["id"]


    # Function to upload a folder recursively
    def upload_folder(folder_path, folder_id):
        def create_folder(folder_name, parent_id):
            folder_metadata = {
                'name': folder_name,
                'parents': [parent_id],
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = service.files().create(body=folder_metadata, fields='id').execute()
            return folder.get('id')

        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                upload_file(item_path, folder_id)
            elif os.path.isdir(item_path):
                subfolder_id = create_folder(item, folder_id)
                upload_folder(item_path, subfolder_id)

       
    # Function to create a folder on Google Drive
        def create_folder(folder_name, parent_id):
            folder_metadata = {
                'name': folder_name,
                'parents': [parent_id],
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = service.files().create(body=folder_metadata, fields='id').execute()
            return folder.get('id')
        
    upload_folder(folder_path, id)

def nofolder(folder_path, folder_id):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    def upload_folder(folder_path, folder_id):
        def create_folder(folder_name, parent_id):
            folder_metadata = {
                'name': folder_name,
                'parents': [parent_id],
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = service.files().create(body=folder_metadata, fields='id').execute()
            return folder.get('id')

        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                upload_file(item_path, folder_id)
            elif os.path.isdir(item_path):
                subfolder_id = create_folder(item, folder_id)
                upload_folder(item_path, subfolder_id)
    # Function to create a folder on Google Drive
        def create_folder(folder_name, parent_id):
            folder_metadata = {
                'name': folder_name,
                'parents': [parent_id],
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = service.files().create(body=folder_metadata, fields='id').execute()
            return folder.get('id')
        
    upload_folder(folder_path, folder_id)





def up():
    folder_path = folderh.get()
    parent = fold.get()
    folder(folder_path, parent)

def fix_up():
    folder_path = folderh.get()
    parent = "1Uq6cjx30i1wr7VijrKnnIIPos8cwcde7"
    folder(folder_path, parent)
    
def upnofold():
    folder_path = folderh.get()
    parent = fold.get()
    nofolder(folder_path, parent)

import tkinter as tk 
root = tk.Tk()

root.title("mindriv")
#root.geometry("800x450")
label = tk.Label(root, text="Mindiv", font=('Arial', 18))
label.grid(row=0)

tk.Label(root, text="mappa helye").grid(row=1)
tk.Label(root, text="drive folder id").grid(row=2)


folderh = tk.Entry(root)
fold = tk.Entry(root)
folderh.grid(row=1, column=1)
fold.grid(row=2, column=1)

gob1 = tk.Button(root, text="saját hely", command=up)
gob1.grid(row=3, column=0)

gob2 = tk.Button(root, text="fix hely", command=fix_up)
gob2.grid(row=3, column=1)

gob3 = tk.Button(root, text="új mappa nélkül", command=upnofold)
gob3.grid(row=4, column=0)


root.mainloop()
authenticate()
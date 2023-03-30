from django.http import HttpResponse,JsonResponse
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json

def data_get(request):
        # Service Account Credential file
        SERVICE_ACCOUNT_FILE = 'cred.json'
        # Google Api Scopes for entire function
        scopes = ['https://www.googleapis.com/auth/admin.directory.user.readonly',
                'https://www.googleapis.com/auth/cloud-platform']

        creds = None
        # Making Google service call
        creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=scopes)

        emailId = "ajay.singh@freecharge.com"

        # Making Domain wide delegation for the user/email id
        delegated_credentials = creds.with_subject(emailId)
       
        # Creating Drive service using Domain wide delegated credentials
        directory_service = build('admin', 'directory_v1', credentials=delegated_credentials)
        #sT = datetime.utcnow() # <-- get time in UTC
        #starttime = sT.isoformat("T") + "Z"  
        # startTime='2023-02-18T10:26:35.000Z'      
        # Making multiple Api call to re
        results = directory_service.users().list(domain= 'freecharge.com', maxResults=10
                                ,orderBy='email').execute()
        users = results.get('users', [])
        print(type(users))
        users = [{'id':data.get('id',False),'primaryEmail':data.get('primaryEmail',False),'suspended':data.get('suspended',False)} for data in users]
        return JsonResponse(users,safe=False)

from django.http import JsonResponse
from googleapiclient.discovery import build
from google.oauth2 import service_account
from .settings import EMAIL_ID

def data_get(request):
        code = request.GET.get('code') or ''
        # Service Account Credential file
        SERVICE_ACCOUNT_FILE = 'cred.json'
        # Google Api Scopes for entire function
        scopes = ['https://www.googleapis.com/auth/admin.directory.user.readonly',
                'https://www.googleapis.com/auth/cloud-platform']

        creds = None
        page_token = None
        # Making Google service call
        creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=scopes)

        emailId = EMAIL_ID

        # Making Domain wide delegation for the user/email id
        delegated_credentials = creds.with_subject(emailId)
       
        # Creating Drive service using Domain wide delegated credentials
        directory_service = build('admin', 'directory_v1', credentials=delegated_credentials)
        data = []
        flag = False
        while True:
                users = []
                results = directory_service.users().list(domain= 'freecharge.com', maxResults=500
                                        , pageToken=page_token,orderBy='email').execute()
                users = results.get('users', [])
                for user in users:
                        try:
                                if user['externalIds'][0]['value'] == code:
                                        matched_user_data = {'employeeCode':user['externalIds'][0]['value'],'primaryEmail':user.get('primaryEmail')
                                        ,'suspended':user.get('suspended')}
                                        data.append(matched_user_data)
                                        flag=True
                                        break
                        except:
                               pass
                if flag:
                        break
                page_token = results.get('nextPageToken')
                if not page_token:
                        break
       
        return JsonResponse(data,safe=False)

from django.http import JsonResponse
from googleapiclient.discovery import build
from google.oauth2 import service_account
from .settings import EMAIL_ID
import re
pattern = r'^[0-9]+$'

def data_get(request):
        code = request.GET.get('code')
        is_valid_code = code and re.match(pattern,code)
        

        # Service Account Credential file
        SERVICE_ACCOUNT_FILE = 'cred.json'
        # Google Api Scopes for entire function
        scopes = ['https://www.googleapis.com/auth/admin.directory.user.readonly',
                'https://www.googleapis.com/auth/cloud-platform']

        creds = None
        page_token = None
        creds = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=scopes)

        emailId = EMAIL_ID

        delegated_credentials = creds.with_subject(emailId)
       
        directory_service = build('admin', 'directory_v1', credentials=delegated_credentials)
        emp_data = []
        if is_valid_code :
                results = directory_service.users().list(
                domain='freecharge.com',
                query=f"externalId={code}",
                maxResults=1
                ).execute()
                if results and not results.get('users'):
                        emp_data.append({'message':'Invalid Employee Code'})
                if results.get('users'):
                        res_user = results.get('users')[0]
                        matched_user_data = {'employeeCode':res_user['externalIds'][0]['value'],'primaryEmail':res_user.get('primaryEmail')
                                                ,'suspended':res_user.get('suspended')}
                        emp_data.append(matched_user_data)

        else:
                emp_data.append({'message':'Invalid Employee Code'})
        return JsonResponse(emp_data,safe=False)

                # data = []
                # flag = False
                # while True:
                #         users = []
                #         results = directory_service.users().list(domain= 'freecharge.com', maxResults=500
                #                                 , pageToken=page_token,orderBy='email').execute()
                #         # print('result',results)
                #         users = results.get('users', [])
                #         for user in users:
                #                 try:
                #                         if user['externalIds'][0]['value'] == code:
                #                                 matched_user_data = {'employeeCode':user['externalIds'][0]['value'],'primaryEmail':user.get('primaryEmail')
                #                                 ,'suspended':user.get('suspended')}
                #                                 data.append(matched_user_data)
                #                                 flag=True
                #                                 break
                #                 except:
                #                        pass
                #         if flag:
                #                 break
                #         page_token = results.get('nextPageToken')
                #         if not page_token:
                #                 break
        
        # return JsonResponse(results,safe=False)

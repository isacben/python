from __future__ import print_function
import pickle
import os.path
import xmlrpc.client
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Amounts to correct the reveneu report
AMOUNTS = [0] # Fill this with amounts, for example: 150.00

START = "1/01/2020"
END = "1/31/2020"

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Dashboard 2020 Spreadsheet
DASHBOARD_SPREADSHEET_ID = 'xxxxxxxxxxxxxxxxx'
DASHBOARD_RANGE_NAME = 'JAN20!F16:F17'

# Odoo Reveneu Report 2020 Spreadsheet
ODOO_SPREADSHEET_ID = 'xxxxxxxxxxxxxxxxxxx'
ODOO_RANGE_NAME = 'CST_IBE!C3:D3'

# Odoo API
URL = ''
DB = ''
ODOO_USR = ''
ODOO_PWD = ''

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'sheets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Get reveneu amount from Odoo
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(URL))
    uid = common.authenticate(DB, ODOO_USR, ODOO_PWD, {})

    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(URL))
    res = models.execute_kw(DB, uid, ODOO_PWD, 'account.invoice', 'search_read', 
                            [[["user_id", "ilike", "xxx"], ["date_invoice", ">=", START], ["date_invoice", "<=", END]]],
                            {'fields': ['amount_total_signed']})

    reveneu = sum(map(lambda x: float(x['amount_total_signed']), res))

    # Fix amount for the reveneu report
    adjustments = '='
    total_reveneu = reveneu
    for amount in AMOUNTS:
        adjustments += '+' + str('%.2f'%amount)
        total_reveneu += amount
        
    dashboard_values  = [
        [str('%.2f'%reveneu)],
        [adjustments],
    ]
    odoo_values  = [
        [str('%.2f'%reveneu), adjustments],
    ]
    dashboard_body = {'values': dashboard_values}
    odoo_body = {'values': odoo_values}
    value_input_option = 'USER_ENTERED'
    
    # Call the Sheets API
    sheet = service.spreadsheets()
    
    # Update Dashboard
    result = sheet.values().update(spreadsheetId=DASHBOARD_SPREADSHEET_ID,
                                   range=DASHBOARD_RANGE_NAME,
                                   valueInputOption=value_input_option,
                                   body=dashboard_body).execute()
                                   
    # Update Odoo Reveneu Report
    odoo_result = sheet.values().update(spreadsheetId=ODOO_SPREADSHEET_ID,
                                   range=ODOO_RANGE_NAME,
                                   valueInputOption=value_input_option,
                                   body=odoo_body).execute()

    print('--------------------------------------------')
    print('Actuals Billing: $' + str(('%.2f'%reveneu)))
    print('Adjustments: ' + adjustments)
    print('Adjusted Actuals Billing: $' + str(('%.2f'%total_reveneu)))
    

if __name__ == '__main__':
    main()

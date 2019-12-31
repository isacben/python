# Isaac Benitez
# Customer Success Manager
# Odoo Inc.

# This scripts gets the reveneu invoiced by a user, within a period of time.

import xmlrpc.client

url = ''
db = ''
username = ''
password = ''

start = "12/01/2019"
end = "12/31/2019"

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
res = models.execute_kw(db, uid, password, 'account.invoice', 'search_read', 
    [[["user_id", "ilike", "ibe"], ["date_invoice", ">=", start], ["date_invoice", "<=", end]]],
    {'fields': ['amount_total_signed']})

total = sum(map(lambda x: float(x['amount_total_signed']), res))

print('%.2f'%total)

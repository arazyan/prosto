import requests

headers = {'Accept': 'application/json'}

qr_url = 'https://api.prostospb.team/api/form_participation.php?user_id=139627&event_id=9706'

request_url = f'http://api.qrserver.com/v1/read-qr-code/?fileurl={qr_url}'

r = requests.get(request_url, headers=headers)
print(request_url)
print(r.text)




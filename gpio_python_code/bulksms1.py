import http.client
import json
from base64 import b64encode


conn = http.client.HTTPSConnection('api.bulksms.com')

# /v1/messages
# myusername="davidcee"
# mypassword="XX!"
userAndPass = b64encode(b"davidcee:XX!").decode("ascii")
print(userAndPass)
# headers = {'Content-type': 'application/json' '%s' % authstr }
headers = {'Content-type': 'application/json', 'Authorization' : 'Basic %s' %  userAndPass }
print("headers:", headers)

mydata={ 'to': '7808247824', 'encoding': 'UNICODE', 'body': 'Test from Python'}
json_mydata = json.dumps(mydata)
print(json_mydata)

payload=authstr + "%20" + json_mydata


conn.request('POST', '/v1/messages', json_mydata, headers=headers )

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


 
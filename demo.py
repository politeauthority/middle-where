from fabric.connection import Connection

import requests

# with Connection('host') as c:
#     print(c.run('docker ps'))


data = {
    'host': 'host',
    'cmds': ['du /root/backups']
}
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
r = requests.post(
    'http://localhost:5000/run',
    json=data,
    headers=headers)

# r = requests.get('http://localhost:5000/')
print(r)
print(r.text)

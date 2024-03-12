import os
import requests
# definition of the API address
api_address = 'localhost'
# API port
api_port = 8000
# requête
r = requests.post(
    url='http://{localhost}:{8000}/login'.format(address=api_address, port=api_port),
    params= {
        'username': 'harriet',
        'password': 'munich2024'
    }
)
output = '''
============================
    Authentication test
============================
request done at "/login"
| username="harriet"
| password="munich2024"
expected result = 200
actual restult = {status_code}
==>  {test_status}
'''
# query status
status_code = r.status_code
# display the results
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output.format(status_code=status_code, test_status=test_status))
# printing in a file
if os.environ.get('LOG') == 1:
    with open('api_test.log', 'a') as file:
        file.write(output)
        
r = requests.post(
    url='http://{localhost}:{8000}/login'.format(address=api_address, port=api_port),
    params= {
        'username': 'mickey',
        'password': 'mouse2024'
    }
)
output = '''
============================
    Authentication test
============================
request done at "/login"
| username="mickey"
| password="mouse2024"
expected result = 422
actual restult = {status_code}
==>  {test_status}
'''
# query status
status_code = r.status_code
# display the results
if status_code == 422:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output.format(status_code=status_code, test_status=test_status))
# printing in a file
if os.environ.get('LOG') == 1:
    with open('api_test.log', 'a') as file:
        file.write(output)
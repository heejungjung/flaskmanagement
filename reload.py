from dotenv import load_dotenv
import os
import requests

username = os.environ.get('PAW_USER')
api_token = os.environ.get('PAW_API')
domain_name = os.environ.get('PAW_DOMAIN')

response = requests.post(
    'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain_name}/reload/'.format(
        username=username, domain_name=domain_name
    ),
    headers={'Authorization': 'Token {token}'.format(token=api_token)}
)
if response.status_code == 200:
    print('reloaded OK')
else:
    print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))
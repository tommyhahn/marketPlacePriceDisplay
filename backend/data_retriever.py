import requests


def retrieve_data():
    response = requests.get('https://mocki.io/v1/70f45519-0232-463b-bd4f-88e9d7213d26')
    data = response.json()
    return data

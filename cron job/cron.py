import requests
def generate_random_data():
    requests.get("http://192.168.59.102:31600/generate_random_data")
generate_random_data()
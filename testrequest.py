import requests

url = 'https://jsonplaceholder.typicode.com/posts'

x = requests.post(url)

print(x.json())

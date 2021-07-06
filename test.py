import requests
import urllib

word='hello world'
encode = requests.utils.quote(word)
encode2=urllib.parse.quote(word)
for i in range(0,9):
    print(i)
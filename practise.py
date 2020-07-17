import requests

payload = {
    "token": "Bbc-xRoXD0IsyJCrLynAyQ",
    "data": {
      "name": "nameFirst",
      "email": "internetEmail",
      "phone": "phoneHome",
      "Age":"10",
      "_repeat": 300
    }
};

r = requests.post("https://app.fakejson.com/q", json = payload)
print(r.content)
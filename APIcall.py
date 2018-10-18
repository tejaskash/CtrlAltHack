import requests
import matplotlib.pyplot as plt
import json
from PIL import Image
from io import BytesIO

KEY = "e10b537e12764747a3cc496d6c026ac4"
assert KEY
BASE_URL = "https://centralindia.api.cognitive.microsoft.com/vision/v2.0/"
analyse = BASE_URL+"analyze"
img = input("Enter Image URL: ")
headers = {'Ocp-Apim-Subscription-Key':KEY}
params = {'visualFeatures':'Categories,Description,Color'}
data = {'url':img}
response = requests.post(analyse,headers = headers,params = params,json = data)
response.raise_for_status()
analysis = response.json()
print(json.dumps(response.json()))
imgcaption = analysis["description"]["captions"][0]["text"].capitalize()
image = Image.open(BytesIO(requests.get(img).content))
plt.imshow(image)
plt.axis("off")
_ = plt.title(imgcaption,size="x-large",y=-0.1)
plt.show()

import requests
import base64
import json


class PlateCreater:

    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def get_plate(self, image: bytes) -> str:
        img_base64 = base64.b64encode(image)

        url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=eu&secret_key=%s' % self.secret_key
        r = requests.post(url, data=img_base64)

        data = json.dumps(r.json(), indent=2)
        data_dict = json.loads(data)

        try:
            return data_dict['results'][0]['plate']
        except IndexError:
            return ''

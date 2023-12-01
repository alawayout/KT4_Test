import json

import pytest
import requests
import pprint


class BaseRequest:
    def __init__(self, base_url):
        self.base_url = base_url
        # set headers, authorisation etc

    def _request(self, url, request_type, data=None, expected_error=False):
        stop_flag = False
        while not stop_flag:
            if request_type == 'GET':
                response = requests.get(url)
            elif request_type == 'POST':
                response = requests.post(url, json=data)
            elif request_type == 'PUT':
                response = requests.put(url, json=data)
            else:
                response = requests.delete(url)

            if not expected_error and response.status_code == 200:
                stop_flag = True
            elif expected_error:
                stop_flag = True
        return response

    def get(self, endpoint, endpoint_id, expected_error=True):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'GET', expected_error=expected_error)
        return response

    def post(self, endpoint, endpoint_id='', body=None):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'POST', data=body, expected_error=True)
        return response.json()

    def delete(self, endpoint, endpoint_id=''):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'DELETE')
        return response.json()['message']

    def put(self, endpoint, endpoint_id, body):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'PUT', data=body)
        return response.json()['message']


BASE_URL = 'https://dog.ceo/api/breeds'
BASE_URL2 = 'https://dog.ceo/api/breed'
Base_request = BaseRequest(BASE_URL)
Base_request2 = BaseRequest(BASE_URL2)

dogs_list = Base_request.get('list', 'all')
pprint.pprint(dogs_list.json()['message'])


@pytest.mark.parametrize('name', [key for key in dogs_list.json()['message']])
def test_type(name):
    assert type(dogs_list.json()['message'][name]) == list


img = Base_request.get('image', 'random')
pprint.pprint(img.json()['message'])


@pytest.mark.parametrize('image', [img.json()['message']])
def test_img(image: str):
    assert image.endswith('.jpg')


count = 3
arr_img = Base_request.get('image', f'random/{count}')


@pytest.mark.parametrize('image_arr', [arr_img.json()['message']])
def test_arr_img(image_arr: list):
    assert len(image_arr) == count


breed = 'hound'
breed_images = Base_request2.get(breed, 'images')


@pytest.mark.parametrize('breed_img', [img for img in breed_images.json()['message']])
def test_breed_img(breed_img):
    assert breed in breed_img


hound_list = ["afghan", "basset", "blood", "english", "ibizan", "plott", "walker"]
sub_breed_list = Base_request2.get('hound', 'list')
print(sub_breed_list.json()['message'])


@pytest.mark.parametrize('name, expected', [(sub_breed_list.json()['message'][i], hound_list[i]) for i in range(0, 7)])
def test_name(name, expected):
    assert name == expected
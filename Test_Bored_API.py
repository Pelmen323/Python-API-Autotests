import json
import requests
import logging
import random
import string
from timeit import default_timer as timer
import pytest

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
url = "https://www.boredapi.com/api"
key = "7096020"
activities = ('social', 'education', 'recreational', 'busywork', 'charity', 'relaxation', 'diy', 'music', 'cooking')
test_response = {
    "activity": "Practice coding in your favorite lanaguage",
    "type": "recreational",
    "participants": 1,
    "price": 0,
    "link": "",
    "key": "7096020",
    "accessibility": 0.1
}


@pytest.mark.smoke
class TestBoredApi:

    def check_response_code(response):
        assert response.status_code == 200, f"Should be OK - 200, actual - {response.status_code}"

    def check_response_keys(response):
        for i in test_response.keys():
            assert i in response.json().keys(), f"The response should contain the key that is missing - {i}"

    def test_get_random_activity(self):
        response = requests.get(f"{url}/activity")
        TestBoredApi.check_response_code(response)
        TestBoredApi.check_response_keys(response)

    def test_get_activity_by_key(self):
        response = requests.get(f"{url}/activity?key={key}")
        TestBoredApi.check_response_code(response)
        for i in test_response.items():
            assert i in response.json().items(), f"The response should contain the item that is missing - {i}"

    def test_get_activity_by_type(self):
        type_activity = random.choice(activities)
        response = requests.get(f"{url}/activity?type={type_activity}")
        TestBoredApi.check_response_code(response)
        TestBoredApi.check_response_keys(response)
        assert response.json()["type"] == type_activity, f"Expected activity '{type_activity}', actual type of activity - {response.json()['type']}"

    def test_get_activity_by_participants(self):
        participants = random.randint(1, 5)
        response = requests.get(f"{url}/activity?participants={participants}")
        TestBoredApi.check_response_code(response)
        TestBoredApi.check_response_keys(response)
        assert response.json()["participants"] == participants, f"Expected participants '{participants}', actual participants - {response.json()['participants']}"

    def test_get_activity_by_price(self):
        price = (random.randint(1, 6)) / 10
        response = requests.get(f"{url}/activity?price={price}")
        TestBoredApi.check_response_code(response)
        TestBoredApi.check_response_keys(response)
        assert response.json()["price"] == price, f"Expected price '{price}', actual price - {response.json()['price']}"  

    def test_get_activity_by_accessibility(self):
        accessibility = (random.randint(0, 10)) / 10
        response = requests.get(f"{url}/activity?accessibility={accessibility}")
        TestBoredApi.check_response_code(response)
        TestBoredApi.check_response_keys(response)
        assert response.json()["accessibility"] == accessibility, f"Expected accessibility '{accessibility}', actual accessibility - {response.json()['accessibility']}"

    def test_get_activity_by_price_range(self):
        minprice = (random.randint(1, 6)) / 10
        maxprice = (random.randint(int(minprice*10), 6)) / 10
        response = requests.get(f"{url}/activity?minprice={minprice}&maxprice={maxprice}")
        TestBoredApi.check_response_code(response)
        TestBoredApi.check_response_keys(response)
        assert maxprice >= response.json()["price"] >= minprice, f"The price should be more >= {minprice} and <= {maxprice}, actual - {response.json()['price']}"

    def test_get_activity_by_accessibility_range(self):
        minaccess = (random.randint(0, 10)) / 10
        maxaccess = (random.randint(int(minaccess*10), 10)) / 10
        response = requests.get(f"{url}/activity?minaccessibility={minaccess}&maxaccessibility={maxaccess}")
        TestBoredApi.check_response_code(response)
        TestBoredApi.check_response_keys(response)
        assert maxaccess >= response.json()["accessibility"] >= minaccess, f"The price should be more >= {minaccess} and <= {maxaccess}, actual - {response.json()['accessibility']}"

    def test_get_activity_by_participants_range(self):
        minparticipants = random.randint(1, 5)
        maxparticipants = random.randint(minparticipants, 5)
        response = requests.get(f"{url}/activity?minparticipants={minparticipants}&maxparticipants={maxparticipants}")
        TestBoredApi.check_response_code(response)
        TestBoredApi.check_response_keys(response)
        assert maxparticipants >= response.json()["participants"] >= minparticipants, f"The price should be more >= {minparticipants} and <= {maxparticipants}, actual - {response.json()['participants']}"

    def test_get_activity_by_participants_and_type(self):
        participants = random.randint(1, 5)
        type_activity = "social"
        response = requests.get(f"{url}/activity?type={type_activity}&participants={participants}")
        TestBoredApi.check_response_code(response)
        TestBoredApi.check_response_keys(response)
        assert response.json()["participants"] == participants, f"Expected participants '{participants}', actual participants - {response.json()['participants']}"
        assert response.json()["type"] == type_activity, f"Expected activity '{type_activity}', actual type of activity - {response.json()['type']}"

    def test_error_non_existing_activity(self):
        type_activity = ''.join([random.choice(string.ascii_letters) for i in range(random.randint(2, 15))])
        response = requests.get(f"{url}/activity?type={type_activity}")
        TestBoredApi.check_response_code(response)
        assert response.json() == {"error": "No activity found with the specified parameters"}, f"Expected error message, got {response,json()}"

    def test_error_invalid_arg_type(self):
        participants = ''.join([random.choice(string.ascii_letters) for i in range(random.randint(2, 15))])
        response = requests.get(f"{url}/activity?participants={participants}")
        TestBoredApi.check_response_code(response)
        assert response.json() == {"error": "Failed to query due to error in arguments"}, f"Expected error message, got {response,json()}"

    def test_error_POST_request(self):
        request_body = test_response.copy()
        request_body["participants"] = random.randint(10, 1000)
        response = requests.post(f"{url}/activity?key={key}", data=request_body)
        TestBoredApi.check_response_code(response)
        assert response.json() == {"error": "Endpoint not found"}, f"Expected error message, got {response,json()}"
        response = requests.get(f"{url}/activity?key={key}")
        TestBoredApi.check_response_code(response)
        for i in test_response.items():
            assert i in response.json().items(), f"The response should contain the item that is missing - {i}"

    def test_error_PUT_request(self):
        request_body = test_response.copy()
        request_body["participants"] = random.randint(10, 1000)
        response = requests.put(f"{url}/activity?key={key}", data=request_body)
        TestBoredApi.check_response_code(response)
        assert response.json() == {"error": "Endpoint not found"}, f"Expected error message, got {response,json()}"
        response = requests.get(f"{url}/activity?key={key}")
        TestBoredApi.check_response_code(response)
        for i in test_response.items():
            assert i in response.json().items(), f"The response should contain the item that is missing - {i}"

    def test_error_PATCH_request(self):
        request_body = test_response.copy()
        request_body["participants"] = random.randint(10, 1000)
        response = requests.patch(f"{url}/activity?key={key}", data=request_body)
        TestBoredApi.check_response_code(response)
        response = requests.get(f"{url}/activity?key={key}")
        TestBoredApi.check_response_code(response)
        for i in test_response.items():
            assert i in response.json().items(), f"The response should contain the item that is missing - {i}"

    def test_error_DELETE_request(self):
        response = requests.delete(f"{url}/activity?key={key}")
        TestBoredApi.check_response_code(response)
        assert response.json() == {"error": "Endpoint not found"}, f"Expected error message, got {response,json()}"
        response = requests.get(f"{url}/activity?key={key}")
        TestBoredApi.check_response_code(response)
        for i in test_response.items():
            assert i in response.json().items(), f"The response should contain the item that is missing - {i}"

if __name__ == '__main__':
    start = timer()
    TestBoredApi.test_get_activity_by_type(TestBoredApi)
    TestBoredApi.test_get_random_activity(TestBoredApi)
    TestBoredApi.test_get_activity_by_key(TestBoredApi)
    TestBoredApi.test_get_activity_by_participants(TestBoredApi)
    TestBoredApi.test_get_activity_by_price(TestBoredApi)
    TestBoredApi.test_get_activity_by_accessibility(TestBoredApi)
    TestBoredApi.test_get_activity_by_price_range(TestBoredApi)
    TestBoredApi.test_get_activity_by_accessibility_range(TestBoredApi)
    TestBoredApi.test_get_activity_by_participants_range(TestBoredApi)
    TestBoredApi.test_get_activity_by_participants_and_type(TestBoredApi)
    TestBoredApi.test_error_non_existing_activity(TestBoredApi)
    TestBoredApi.test_error_invalid_arg_type(TestBoredApi)
    TestBoredApi.test_error_POST_request(TestBoredApi)
    TestBoredApi.test_error_PUT_request(TestBoredApi)
    TestBoredApi.test_error_PATCH_request(TestBoredApi)
    TestBoredApi.test_error_DELETE_request(TestBoredApi)
    end = timer()
    print(f"Tests finished! It took {end-start} to finish the run")

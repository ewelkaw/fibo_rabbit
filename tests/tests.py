import unittest
import requests
import time
import os


class TestUnitTest(unittest.TestCase):
    def setUp(self):
        self.base_url = os.getenv("BASE_TEST_URL", "http://localhost:5000/api/fibo")
        counter = 0
        connected = False
        while counter < 30 and not connected:
            try:
                requests.request("GET", self.base_url)
                connected = True
            except requests.exceptions.ConnectionError:
                counter = counter + 1
                time.sleep(1)
        if not connected:
            raise Exception("Unable to connect to docker-compose stack")

    def test_get_not_calculated(self):
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        response = requests.request("GET", f"{self.base_url}/1234321", headers=headers)

        self.assertEqual(
            response.json(),
            {
                "error": "Calculation have been not requested or have not been finished yet."
            },
        )
        self.assertEqual(response.status_code, 404)

    def test_post_new_number(self):
        payload = '{"number": 666}'
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        response = requests.request(
            "POST", self.base_url, headers=headers, data=payload
        )

        self.assertEqual(
            response.json(), {"success": "Request will be processed"},
        )
        self.assertEqual(response.status_code, 202)

    def test_repost_number(self):
        payload = '{"number": 3}'
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        requests.request("POST", self.base_url, headers=headers, data=payload)

        time.sleep(1)

        response = requests.request(
            "POST", self.base_url, headers=headers, data=payload, allow_redirects=False,
        )

        self.assertEqual(
            response.text, "",
        )
        self.assertEqual(response.status_code, 303)

    def test_post_and_retrieve_number(self):
        payload = '{"number": 12}'
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        requests.request("POST", self.base_url, headers=headers, data=payload)

        time.sleep(1)

        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        response = requests.request("GET", f"{self.base_url}/12", headers=headers)

        self.assertEqual(
            response.json(),
            {"number": 12, "sequence": [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]},
        )
        self.assertEqual(response.status_code, 200)

    def test_post_invalid_number(self):
        payload = '{"number": "hellothere"}'
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        response = requests.request(
            "POST", self.base_url, headers=headers, data=payload
        )

        self.assertEqual(
            response.json(), {"error": "Invalid number - you need to provide int"},
        )
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    if os.getenv("CI") != "true":
        print("This script is supposed to be running only on the CI env")
    else:
        unittest.main()

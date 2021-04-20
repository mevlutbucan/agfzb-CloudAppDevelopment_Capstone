import requests
import json
# import related models here
from .models import CarDealer
from requests.auth import HTTPBasicAuth

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {}".format(url))
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {}".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
# def post_request():

# Create a get_dealers_from_cf method to get dealers from a cloud function
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealerships_from_cloudant(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        dealerships = json_result["entries"]
        for dealer in dealerships:
            car_dealer = CarDealer(id=dealer["id"],
                                   city=dealer["city"],
                                   state=dealer["state"],
                                   st=dealer["st"],
                                   address=dealer["address"],
                                   zip=dealer["zip"],
                                   lat=dealer["lat"],
                                   long=dealer["long"],
                                   short_name=dealer["short_name"] if 'short_name' in dealer else None,
                                   full_name=dealer["full_name"] if 'full_name' in dealer else None)
            results.append(car_dealer)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative




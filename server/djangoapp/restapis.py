import requests
import json
from .models import CarDealer, DealerReview

# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        print("Network exception occurred")
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
# def post_request():

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealerships_from_cloudant(**kwargs):
    API_URL = "https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/949f20dc522c93ee49c129709667f19bb65ab6298b4763844d288912d7226ca2/capstone-project-fn/dealership"
    results = []
    json_result = get_request(API_URL)
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
                                   short_name=dealer["short_name"],
                                   full_name=dealer["full_name"])
            results.append(car_dealer)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cloudant(dealerId):
    API_URL = "https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/949f20dc522c93ee49c129709667f19bb65ab6298b4763844d288912d7226ca2/capstone-project-fn/review"
    results = []
    json_result = get_request(API_URL, dealerId=dealerId)
    if json_result:
        reviews = json_result["entries"]
        for review in reviews:
            sentiment = analyze_review_sentiments(review["review"])
            dealer_review = DealerReview(id=review["id"],
                                         name=review["name"],
                                         dealership=review["dealership"],
                                         review=review["review"],
                                         purchase=review["purchase"],
                                         purchase_date=review["purchase_date"],
                                         car_make=review["car_make"],
                                         car_model=review["car_model"],
                                         car_year=review["car_year"],
                                         sentiment=sentiment)
            results.append(dealer_review)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    API_URL = "https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/949f20dc522c93ee49c129709667f19bb65ab6298b4763844d288912d7226ca2/capstone-project-fn/analyze/sentiment"
    results = []
    json_result = get_request(API_URL, text=text)
    if json_result:
        return json_result["label"]

# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative




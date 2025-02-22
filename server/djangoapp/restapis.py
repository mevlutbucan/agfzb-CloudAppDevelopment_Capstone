import os
import requests
import json
from .models import CarDealer, DealerReview

API_URL = os.environ.get('COURSERA_CF_API_URL')
API_URL_DEALERSHIP = API_URL + '/api/dealership'
API_URL_REVIEW = API_URL + '/api/review'
API_URL_SENTIMENT = API_URL + '/api/sentiment'

# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        print("Network exception occurred")
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, json=json_payload, params=kwargs)
    except:
        print("Network exception occurred")
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealerships_from_cloudant(**kwargs):
    results = []
    json_result = get_request(API_URL_DEALERSHIP)
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
    results = []
    json_result = get_request(API_URL_REVIEW, dealerId=dealerId)
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

def add_dealer_review_to_cloudant(review_post):
    review = {
        "id": review_post['review_id'],
        "name": review_post['reviewer_name'],
        "dealership": review_post['dealership'],
        "review": review_post['review'],
        "purchase": review_post.get('purchase', False),
        "purchase_date": review_post.get('purchase_date'),
        "car_make": review_post.get('car_make'),
        "car_model": review_post.get('car_model'),
        "car_year": review_post.get('car_year')
    }
    return post_request(API_URL_REVIEW, review)

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    results = []
    json_result = get_request(API_URL_SENTIMENT, text=text)
    if json_result:
        return json_result.get('label', 'neutral')

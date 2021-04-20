#
# Insert a new document into Cloudant database:
# https://docs.couchdb.org/en/stable/api/database/bulk-api.html#db-all-docs
#
import sys
from cloudant.client import Cloudant

def main(params):
    cloudant_or_error = get_cloudant_account(params)
    if type(cloudant_or_error) == str:
        return { "error": cloudant_or_error }
    cloudant_db = cloudant_or_error['dealership-reviews']
    new_document = set_document(params)
    inserted_document = cloudant_db.create_document(new_document)
    if inserted_document.exists():
        return { "response": "New document has been inserted." }
    else:
        return { "error": "Something went wrong." }

def get_cloudant_account(params):
    if not 'api_username' in params:
        return "api_username parameter is required."
    if not 'api_key' in params:
        return "api_key parameter is required."
    from cloudant.client import Cloudant
    return Cloudant.iam(params['api_username'], params['api_key'], connect=True)

def set_document(params):
    return {
        "id": params['id'],
        "name": params['name'],
        "dealership": params['dealership'],
        "review": params['review'],
        "purchase": params['purchase'],
        "purchase_date": params['purchase_date'],
        "car_make": params['car_make'],
        "car_model": params['car_model'],
        "car_year": params['car_year']
    }

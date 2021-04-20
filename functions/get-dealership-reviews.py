#
# Get all documents in Cloudant database:
# https://docs.couchdb.org/en/stable/api/database/bulk-api.html#db-all-docs
#
import sys
from cloudant.client import Cloudant

def main(params):
    cloudant = get_cloudant_account(params)
    cloudant_db = cloudant['dealership-reviews']
    filtered_list = get_filtered_list(cloudant_db, params)
    formatted_list = get_formatted_list(filtered_list)
    return { "entries": formatted_list }

def get_cloudant_account(params):
    return Cloudant.iam(params['api_username'], params['api_key'], connect=True)

def get_filtered_list(db, params):
    filtered_list = []
    if 'dealerId' in params:
        for document in db:
            if str(document['id']) == params['dealerId']:
                filtered_list.append(document)
    else:
        for document in db:
            filtered_list.append(document)
    return filtered_list

def get_formatted_list(filtered_list):
    formatted_list = []
    for document in filtered_list:
        formatted_list.append({
            "id": document['id'],
            "name": document['name'],
            "dealership": document['dealership'],
            "review": document['review'],
            "purchase": document['purchase'],
            "purchase_date": document['purchase_date'] if 'purchase_date' in document else None,
            "car_make": document['car_make'] if 'car_make' in document else None,
            "car_model": document['car_model'] if 'car_model' in document else None,
            "car_year": document['car_year'] if 'car_year' in document else None
        })
    return formatted_list

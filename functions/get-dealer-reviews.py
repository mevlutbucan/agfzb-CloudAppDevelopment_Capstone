#
# Get all documents in Cloudant database:
# https://docs.couchdb.org/en/stable/api/database/bulk-api.html#db-all-docs
#
import sys

def main(params):
    cloudant_or_error = get_cloudant_account(params)
    if type(cloudant_or_error) == str:
        return { "error": cloudant_or_error }
    cloudant_db = cloudant_or_error['dealership-reviews']
    filtered_list = get_filtered_list(cloudant_db, params)
    formatted_list = get_formatted_list(filtered_list)
    return { "entries": formatted_list }

def get_cloudant_account(params):
    if not 'api_username' in params:
        return "api_username parameter is required."
    if not 'api_key' in params:
        return "api_key parameter is required."
    from cloudant.client import Cloudant
    return Cloudant.iam(params['api_username'], params['api_key'], connect=True)

def get_filtered_list(db, params):
    filtered_list = []
    if 'dealerId' in params:
        for document in db:
            if str(document['dealership']) == params['dealerId']:
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
            "purchase_date": document.get('purchase_date'),
            "car_make": document.get('car_make'),
            "car_model": document.get('car_model'),
            "car_year": document.get('car_year')
        })
    return formatted_list

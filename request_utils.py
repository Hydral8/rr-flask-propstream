import ast
import requests
from airtable import Airtable
import re


# utility function to get the first valid record and return it as a dict
def first_valid_record(records):
    for i in reversed(range(len(records))):
        try:
            record = ast.literal_eval(records[i]["fields"]["json"])
        except:
            raise Exception(
                "One or all of the records did not have a parsable json data")

        if "JSESSIONID" in record["cookie"]:
            return record

    raise Exception("There was no record with a JSESSIONID")


def get_records():
    airtable = Airtable('appP8OJaz4knlavqC', "api_headers",
                        api_key='keyJEDY3Mkf5qjQAP')

    try:
        # get all records
        records = airtable.get_all()
        return records
    except requests.HTTPError as e:
        raise Exception(e)
    except:
        raise Exception("Some other error")


def get_cookies():
    records = get_records()
    valid_rec = first_valid_record(records)
    cookie = valid_rec["cookie"]
    return cookie


def propstream_req(city, stateco, zipcode, strtadd):
    strtadd = re.sub(" ", "%20", strtadd)
    cookies = get_cookies()
    # testing with manually fetched data. Airtable rn is semifunctional
    # cookies = "JSESSIONID=AcR1ez1QgaKI4GlOP3SJxVKrpZGrsNe89qe8GFGo.localhost-propstream-server"			
    print(cookies)
    url = 'https://app.propstream.com/eqbackend/resource/auth/ps4/property?cityName=' + \
        city+'&stateCode='+stateco+'&zip='+zipcode+'&streetAddress='+strtadd
    print("The url for the property information is -> ", url)
    headers = {
        'authority': 'app.propstream.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://app.propstream.com/search',
        'accept-language': 'en-US,en;q=0.9',
        'Cookie': cookies
    }

    response = requests.request("GET", url, headers=headers)
    
    if response.ok:
        return response.json()
        # return jsonval
    else:
        raise Exception(
            "Invalid authentication cookie. This is an issue with the cookie stored in the airtable")
        
 
# FOR TESTING (Prob move to a pytest file)       
# airtable = Airtable('appP8OJaz4knlavqC', "api_headers",
#                         api_key='jedi4432')
# try:
#     # get all records
#     records = airtable.get_all()
# except requests.HTTPError as e:
#     try:
#         raise Exception(e)
#     except Exception as e2:
#         print(e2)
# except:
#     print("SOME OTHER ERROR")
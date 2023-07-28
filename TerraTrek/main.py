from dotenv import dotenv_values
import requests

def extract_lat_long_via_address(api_key, address_or_zipcode):
    lat, lng = None, None
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address_or_zipcode}&key={api_key}"
    # see how our endpoint includes our API key? Yes this is yet another reason to restrict the key
    r = requests.get(endpoint)
    if r.status_code not in range(200, 299):
        return None, None
    try:
        '''
        This try block incase any of our inputs are invalid. This is done instead
        of actually writing out handlers for all kinds of responses.
        '''
        results = r.json()['results'][0]
        lat = results['geometry']['location']['lat']
        lng = results['geometry']['location']['lng']
    except:
        pass
    return lat, lng


def main():
    env_dict = dotenv_values(".env")
    
    api_key = env_dict["GC_KEY"]
    
    print(extract_lat_long_via_address(api_key, "40 St George St, Toronto, ON M5S 2E4"))
    

if __name__ == '__main__':
    main()
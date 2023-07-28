import requests, serial
API_KEY = "AIzaSyDZ09Q_Kbdwg3kgHH3Quh4SoLf4W1Dgcdc"

def extract_lat_long(location):
    # Code directly from john link: https://www.codingforentrepreneurs.com/blog/python-tutorial-google-$
    lat, lng = None, None
    api_key = API_KEY
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = "{}?address={}&key={}".format(base_url, location, api_key)

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

'''
serial_dir = "fill this in later (we used a value that worked for makeuoft)"

s = serial.Serial("", 9600, timeout = 1)

while True:
    #if waiting_for_voice:
    if s.in_waiting > 0:
        line = s.readline().decode("utf-8").rstrip() # make serial outputs comma separated and end char$
        end_delim_ind = line.index(";")
        line = line[:end_delim_ind].split(",") # line format: 
        
        # do stuff with info sent from arduino
        
   ///     
        
# def get_address
'''


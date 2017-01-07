import json
import urllib2


apikey   = "AIzaSyBJAj1Ap9-MM7BQyauuSNRBFCG_YOombv8"
#latlon   = "40.191989,-85.386546"
#latlon   = "40.188873,-85.443129"
#latlon   = "40.175847,-85.498022"
latlon   = "40.056941,-86.886668"
radius   = "10000"
badTypes = ["local_government_office","locality","political"]



def parseNearbyResults(nearbyResults):
   for nearbyResult in nearbyResults:
      detailsSearch = "https://maps.googleapis.com/maps/api/place/details/json?key=" + apikey + "&placeid=" + nearbyResult['place_id']

      detailsJson   = json.load(urllib2.urlopen(detailsSearch))

      if "result" not in detailsJson:
         continue

      detailsResult = detailsJson['result']

      ignore = False
      for type in detailsResult['types']:
         if str(type) in badTypes:
            ignore = True

      ignore |= "permanently_closed" in detailsResult

      if ('formatted_phone_number' not in detailsResult or 'opening_hours' not in detailsResult or 'website' not in detailsResult) and not ignore:
         print(detailsResult['name'])
         print(detailsResult['url'])
         print(detailsResult['types'])

         print("Address Missing" if 'formatted_address' not in detailsResult else detailsResult['formatted_address'])
         print("Phone # Missing" if 'formatted_phone_number' not in detailsResult else detailsResult['formatted_phone_number'])
         print("Website Missing" if 'website' not in detailsResult else detailsResult['website'])
         if 'opening_hours' not in detailsResult: print("Hours Missing")

         print("--------------\n")

      #else:
      #   print("Skipping: " + detailsResult['name'])




# Start Here #

nextPageToken = None

nearbySearch  = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=" + apikey + "&location=" + latlon + "&radius=" + radius

for i in range(1,20):

   nearbyJson    = json.load(urllib2.urlopen(nearbySearch))
   nextPageToken = nearbyJson['next_page_token'] if "next_page_token" in nearbyJson else None

   parseNearbyResults(nearbyJson['results'])
   
   if nextPageToken:
      nearbySearch  = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=" + apikey + "&pagetoken=" + nextPageToken
   else:
      break


#googleapi
import requests
import json
from PIL import Image
import os
class GoogleDriveAPI:
	def __init__(self):
		print ("Calling parent constructor")

class Files(GoogleDriveAPI):
	def __init__(self):
		print ("Calling face constructor")

	def upload( self ):

		im = Image.open('capture.jpg')
		number_of_bytes_in_file = os.stat('capture.jpg').st_size
		print(number_of_bytes_in_file)

		# print(im.size)
		# print('heee')
		# url_persongroup = self.get_basic_url()+'/'+person_group_id
		headers = {
			'Content-Type':'image/jpeg',
			'Content-Length':number_of_bytes_in_file,
			'Authorization':Bearer ya29.GlttBWrs1k7HlT1EDK8Ybkcz8gOOOZBviMXZZflTHxtuHwXlNY_ZB_bOc8qwi1Beh9auVI4ohbWIp4tAUZGcUpYR-6s4wc4meuOhn-2uZod-i7z5Ggh9m3pWNSbg
		}
		payload = {
			'name':
		}
		#TODO: add userdata if exists
		response = requests.put(url_persongroup,data=json.dumps(payload),headers=headers)

		print( 'hi' )
		return
test = Files()
test.upload()

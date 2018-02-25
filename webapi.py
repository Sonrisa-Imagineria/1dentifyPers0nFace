#!/usr/bin/python3
# import urllib.request
# import urllib.parse
import requests
import json
class MSFaceAPI:
	location = 'southeastasia'
	apiType = ''
	apiKey = '90d24310967b4ace86c56317988c7e72'
	url = 'https://' + str(location) + '.api.cognitive.microsoft.com/face/v1.0'
	def __init__(self):
		print ("Calling parent constructor")

	def get_basic_url( self ):
		print('get basic '+str(self.apiType))
		return str(self.url) + '/' + str(self.apiType)

class Face(MSFaceAPI):
	def __init__(self):
		print ("Calling face constructor")

	def detect( self ):
		print( str(self.get_basic_url()) )
		return

	def identify( self ):
		print( str(self.get_basic_url()) )
		return

class PersonGroup(MSFaceAPI):
	def __init__(self):
		self.apiType = 'persongroups'
		print ("Calling person group constructor")

	def create( self, person_group_id, person_group_name ):
		url_persongroup = self.get_basic_url()+'/'+person_group_id
		headers = {
			'Content-Type':'application/json',
			'Ocp-Apim-Subscription-Key':self.apiKey
		}
		payload = {
			'name':person_group_name
		}
		#TODO: add userdata if exists
		response = requests.put(url_persongroup,data=json.dumps(payload),headers=headers)
		print ( url_persongroup )
		print ( response )
		print( str(self.get_basic_url()) )
		return

	def train_person_group( self, person_group_id ):
		url_persongroup = self.get_basic_url() + '/' + person_group_id + '/train'
		print( url_persongroup )
		headers = {
			'Ocp-Apim-Subscription-Key':self.apiKey
		}
		response = requests.post(url_persongroup,headers=headers)
		print( response.content )
		print( str(self.get_basic_url()) )
		return
	def get_group( self, person_group_id ):
		url_persongroup = self.get_basic_url()+'/'+person_group_id
		headers = {
			'Ocp-Apim-Subscription-Key':self.apiKey
		}
		response = requests.get(url_persongroup,headers=headers)

		print( response )
		return
class Person(MSFaceAPI):
	def __init__(self):
		self.apiType = 'persongroups'
		print ("Calling person constructor")

	def	create( self, person_group_id, person_name, person_alias):
		url_person = self.get_basic_url() + '/' + person_group_id + '/persons'
		print( url_person )
		headers = {
			'Ocp-Apim-Subscription-Key':self.apiKey
		}
		payload = {
			'name': person_name,
			'userData': person_alias
		}
		response = requests.post(url_person,data=json.dumps(payload),headers=headers)
		print('create person')
		print( response )
		return
	def	add_a_face( self, person_group_id, person_id, person_url ):
		print('add_a_face')
		url_person = self.get_basic_url() + '/' + person_group_id + '/persons/' + person_id + '/persistedFaces'
		headers = {
			'Ocp-Apim-Subscription-Key':self.apiKey
		}
		payload = {
			'url': person_url
		}
		response = requests.post(url_person,data=json.dumps(payload),headers=headers)
		print(response.content)
		return
	def get_person_list( self, person_group_id ):
		print('get person list')
		url_person = self.get_basic_url() + '/' + person_group_id + '/persons'
		headers = {
			'Ocp-Apim-Subscription-Key':self.apiKey
		}
		response = requests.get(url_person,headers=headers)
		print(response.content)
		return
	def get_person_info( self, person_group_id, person_id):
		print( 'get a person')
		url_person = self.get_basic_url() + '/' + person_group_id + '/persons/' + person_id
		headers = {
			'Ocp-Apim-Subscription-Key':self.apiKey
		}
		response = requests.get(url_person,headers=headers)
		print(response.content)
		return
pgroup = PersonGroup()
pgroup.train_person_group('yuhsiang')
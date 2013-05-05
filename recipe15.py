def get_info(api, ids):
  infos = {}
	for id in ids:
		user = api.get_user(id)
		infos.update({user.id:user})
	return infos

if __name__ == '__main__':
	import myauth #get your authentication for the value, api
	api = myauth.get_api()
	infos = {}
	infos.update( get_info(api, ['ladofa9', 'corea919']) )
	infos.update( get_info(api, ['72169826', '169290610']) )
	infos.update( get_info(api, 362977517, 362980557) )
	
	import json
	#print json.dumps(infos, indent=1) #is not working

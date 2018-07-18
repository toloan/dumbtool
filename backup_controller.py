import db_controller,os
def delete(config, *argv):
	connection = db_controller.connection(config)['data']
	state = db_controller.connection(config)['state']
	if state == 'success':
		if len(argv) == 1:
			table_list = db_controller.get_all_table(connection)
		elif len(argv) == 2:
			table_list = argv[1].split(',')
		true_count = sum(db_controller.get(connection,argv[0],table_list).values())
		deleted_value = db_controller.delete(connection,argv[0],table_list)
		error = true_count - deleted_value['data']
		count_all = sum(db_controller.get(connection,"1",db_controller.get_all_table(connection)).values())
		connection.close()
		return {'data': {'all': count_all,'deleted': deleted_value['data'],'error': error},'state': deleted_value['state']}

	else:
		return {'data':None,'state':state}


def backup(config,backup_config,clause,table_list):
	backup= db_controller.backup(config,clause,table_list)
	state = backup['state']
	filename = backup['data']
	if state == 'success':
		state = db_controller.load(backup_config,filename)['state']
		print(state)
		if state != 'success':
			return False
		os.remove(filename)
		return True
	else:
		return False



def delete_backup(config,backup_config,*argv):
	print('start')
	connection = db_controller.connection(config)['data']
	state = db_controller.connection(config)['state']
	print('backup')
	if state == 'success':
		if len(argv) == 1:
			table_list = db_controller.get_all_table(connection)
		elif len(argv) == 2:
			table_list = argv[1].split(',')
		if backup(config,backup_config,argv[0],table_list) == False:
			connection.close()
			return {'data': None,'state':'false to backup'}
		else:

			true_count = sum(db_controller.get(connection,argv[0],table_list).values())
			delete = db_controller.delete(connection,argv[0],table_list)
			state2 = delete['state']
			deleted = delete['data']
			error = true_count - deleted
			count_all = sum(db_controller.get(connection,"1",db_controller.get_all_table(connection)).values())
			connection.close()
			return {'data': {'all': count_all,'deleted': deleted,'error': error},'state': state2}

	else:
		return {'data':None,'state':state}	
	
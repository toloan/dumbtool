import configparser
import sys
def get_config(config_dict):
	# read  config 
	keys = [config_dict[i] for i in range(len(config_dict)) if i%2 == 0 ]
	values = [config_dict[i] for i in range(len(config_dict)) if i%2 == 1 ]
	file_name = None
	mode = None
	clause = None
	tables = None
	for i in range(len(keys)):
		if keys[i] =='-t-connection_info'or keys[i] == '-f':
			file_name = values[i]
			continue
		if keys[i] == '-m' or keys[i] == '-mode':
			mode = values[i]
		if  keys[i] =='-w' or keys[i] == '-where_clause':
			clause = values[i]
			continue
		if keys[i] == '-table' or keys[i] =='-tb':
			tables = values[i]
			continue
	if file_name == None or mode == None or clause == None or (mode != 'delete' and mode !='backup-delete'):
		return {'data': None, 'state': 'python DBBackupCleaner.py --help をチェック見てください'}

	# read file config
	config_file = configparser.ConfigParser()
	try:
		config_file.read(file_name)
		list_key=['client','port','host','name','user','password']
		db_list = [option for option in config_file['RemoteDB']]
		check_db=[option for option in list_key if option not in db_list]
		if len(check_db)>0:
			return{'data':None,'state':"RemoteDBの"+ ','.join(check_db) +"のキーワードがありません.python DBBackupCleaner.py --help をチェック見てください"}
		check_db=[option for option in db_list if option not in list_key]
		if len(check_db)>0:
			return{'data':None,'state':"RemoteDBに"+','.join(check_db)+"のキーワードがありません.python DBBackupCleaner.py --help をチェック見てください"}
		if mode == 'backup-delete':	
			db_list = [option for option in config_file['BackupDB']]
			check_db=[option for option in list_key if option not in db_list]
			if len(check_db)>0:
				return{'data':None,'state':"BackupDBの"+','.join(check_db)+"のキーワードがありません.python DBBackupCleaner.py --help をチェック見てください"}
			check_db=[option for option in db_list if option not in list_key]
			if len(check_db)>0:
				return{'data':None,'state':"BackupDBに"+','.join(check_db)+"のキーワードがありません.python DBBackupCleaner.py --help をチェック見てください"}	
	except:
		return{'data':None,'state':"ォーマットが間違いました"}
	config_file = dict(config_file._sections)
	config_file['mode'] = mode
	config_file['clause'] = clause
	config_file['tables'] = tables
	return {'data': config_file,'state': 'success'}

def output(config,message):
	print(message)
	print("done")
	sys.exit(0)



def help():
	print("使い方:\t python DBBackupNCleaner.py [-option 'value']")
	print("options:")
	print("\t -h\t--help\t\t使い方 ")
	print("\t -f\t-connection_info\t○\t使い方")
	print("\t -m\t-mode\t○\tbackup_delte/delete")
	print("\t -w\t-where_clause\t○\tレコーどを選ぶ")
	print("\t -tb\t-table\t○\tテーブル名")


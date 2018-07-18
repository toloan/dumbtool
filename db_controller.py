import MySQLdb
def connection(config):
	try:
		db = MySQLdb.connect(
    		host = config['host'], 
    		user = config['user'], 
    		passwd = config['password'], 
    		db = config['name'], 
    		port = int(config['port']))
	except:
		return {'data': None, 'state': 'unable to run'} 

	return {'data': db,'state':'success'}

def delete(connection,clause,tables_list):
	cursor = connection.cursor()
	rowcount = 0
	state ="success"
	for table in tables_list:
		query = "DELETE from "+table +" WHERE "+clause
		try:
			cursor.execute(query)
			rowcount = rowcount + cursor.rowcount
			connection.commit()
		except:
			state = "some records are not deleted"
			connection.rollback()
	return {"data": rowcount,'state': state}
	
def get_all_table(connection):
	content = "show tables;"
	cursor = connection.cursor()
	cursor.execute(content)
	result = cursor.fetchall()
	if len(result)>=1:
		return list(result[0])
	else:
		return ()

def get(connection,clause,tables_list):
	cursor = connection.cursor()
	list_data = {}
	rowcount = 0
	state ="success"

	for table in tables_list:
		query = "SELECT * from " + table+" WHERE "+clause
		try:

			cursor.execute(	query)
			rows = cursor.fetchall()
			list_data[table] = len(rows)
		except:
			state = "aug"
			connection.rollback()
	return list_data
def save(connection, data):
	cursor = connection.cursor()
	rowcount = 0
	for table,record in data:
		column = ','.join(record.keys())
		value = ','.join(record.values())
		query = "insert into " + table + "( "+ column+ ")values("+value+")"
		try:
			cursor.execute(query)
			rowcount = rowcount + cursor.rowcount
			connection.commit()
		except:
			connection.rollback()
	return rowcount
def backup(config,clause,tables_list):
	import time, subprocess
	timestamp = str(int(time.time()))
	file_name = timestamp+'_dump.sql'
	if config['password'] != '':
		command = 'mysqldump --host '+ config['host'] +' --port '+config['port'] + ' -u '+ config['user']+ ' -p '+config['password']+' '+config['name']+''+' '.join(tables_list)+' --where="'+clause+'" > '+file_name
	else:
		command = 'mysqldump --host '+ config['host'] +' --port '+config['port'] + ' -u '+ config['user']+ ' '+config['name']+' '+' '.join(tables_list)+' --where="'+clause+'" > '+file_name
	try: 
		p = subprocess.Popen(command,shell=True)
		p.communicate()
		if(p.returncode != 0):
			raise
		return {'data':file_name,'state':'success','command':command}
	except Exception as e:
		print(e)
		return{'data':None,'state':'wrong config','command':command}

def load(config,file_name):
	import time, subprocess
	try: 
		if config['password'] != '':
			command = 'mysql --host '+ config['host'] +' --port '+config['port'] + ' -u '+ config['user']+ ' -p '+config['password']+' --database '+config['name']+' < '+file_name
		else:
			command = 'mysql --host '+ config['host'] +' --port '+config['port'] + ' -u '+ config['user']+' --database '+config['name']+' < '+file_name
		p = subprocess.Popen(command,shell = True)
		p.communicate()
		if(p.returncode != 0):
			raise
		return {'data':file_name,'state':'success'}
	except:
		return{'data':None,'state':'unable to load file'}

# def get_all(connection):
# 	cursor = connection.cursor()
# 	rowcount = 0
# 	state ="success"
# 	tables_list = get_all_table(connection)
# 	for table in tables_list:
# 		query = "SELECT * from "+table
# 		try:
# 			cursor.execute(query)
# 			rows = cursor.fetchall()
# 			rowcount = rowcount + len(rows)
# 			connection.commit()
# 		except:
# 			state = "bug"
# 			db.rollback()
# 	return {"data": rowcount,'state': state}

# config = {'host':'127.0.0.1','port':'3306','user':'root','password':'','name':'BackupDB'}
# tables = ['data']
# clause = "updated_date <= '2018-02-02'"
# print(backup(config,clause,tables)['command'])
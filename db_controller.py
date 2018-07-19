import MySQLdb
import psycopg2
def connection(config):
	if config['client'] == 'mysql':
		try:
			db = MySQLdb.connect(
	    		host = config['host'], 
	    		user = config['user'], 
	    		passwd = config['password'], 
	    		db = config['name'], 
	    		port = int(config['port']))
		except:
			return {'data': None, 'state': 'unable to run'} 
	elif config['client'] == 'postgreSQL':
		try:
			db = psycopg2.connect(
	    		host = config['host'], 
	    		user = config['user'], 
	    		passwd = config['password'], 
	    		db = config['name'], 
	    		port = int(config['port']))
		except:
			return {'data': None, 'state': 'unable to run'} 

	else:
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
	if config['client'] == 'mysql':
		if config['password'] != '':
			command = 'mysqldump --host '+ config['host'] +' --port '+config['port'] + ' -u '+ config['user']+ ' -p '+config['password']+' '+config['name']+''+' '.join(tables_list)+' --where="'+clause+'" --skip-add-drop-table --skip-comments | sed \'s/^CREATE TABLE /CREATE TABLE IF NOT EXISTS /\' > '+file_name
		else:
			command = 'mysqldump --host '+ config['host'] +' --port '+config['port'] + ' -u '+ config['user']+ ' '+config['name']+' '+' '.join(tables_list)+' --where="'+clause+'" --skip-add-drop-table --skip-comments | sed \'s/^CREATE TABLE /CREATE TABLE IF NOT EXISTS /\'> '+file_name
	elif config['client'] == 'postgreSQL':
		if config['password'] != '':
			command = 'pg_dump -h '+ config['host']+' --port '+config['port'] +' --user '+config['user']+' --password '+config['password']+' -d '+config['name']+ '-t '+''.join(tables_list)+' -w="'+clause+'" | sed \'s/^CREATE TABLE /CREATE TABLE IF NOT EXISTS /\' > '+file_name

		else:
			command = 'pg_dump -h '+ config['host']+' --port '+config['port'] +' --user '+config['user']+' -d '+config['name']+ '-t '+''.join(tables_list)+ ' -w="'+clause+'" | sed \'s/^CREATE TABLE /CREATE TABLE IF NOT EXISTS /\' > '+file_name 

	else:
		return {'data':None,'state':'wrong config','command':command}
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
	if config['client'] == 'mysql':
		if config['password'] != '':
			command = 'mysql --host '+ config['host'] +' --port '+config['port'] + ' -u '+ config['user']+ ' -p '+config['password']+' --database '+config['name']+' < '+file_name
		else:
			command = 'mysql --host '+ config['host'] +' --port '+config['port'] + ' -u '+ config['user']+' --database '+config['name']+' < '+file_name
	elif config['client'] == 'postgreSQL':
		if config['password'] != '':
			command = 'psql --host '+ config['host'] +' --port '+config['port'] + ' -u '+ config['user']+ ' --password '+config['password']+' -d '+config['name']+' < '+file_name
		else:
			command = 'psql --host '+ config['host'] +' --port '+config['port'] + ' -u '+ config['user']+' -d '+config['name']+' < '+file_name
	try: 
		p = subprocess.Popen(command,shell = True)
		p.communicate()
		if(p.returncode != 0):
			raise
		return {'data':file_name,'state':'success'}
	except:
		return{'data':None,'state':'unable to load file'}

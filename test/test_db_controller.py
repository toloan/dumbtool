import unittest
import sys
sys.path.append("../")
import db_controller
class TestDBController(unittest.TestCase):
	def test_connection(self):
		#true
		config = {'client':'mysql','host':'127.0.0.1','port':3306,'user':'root','password':'','name':'DB'}
		expected_message = 'success'
		return_value = db_controller.connection(config)
		self.assertIsNotNone(return_value['data'])
		self.assertEqual(return_value['state'],expected_message)
		return_value['data'].close()
		#mysql
		#postgre
		#false
		config = {'client':'mysql','host':'127.0.0.1','port':3306,'user':'root','password':'a','name':'DB'}
		expected_message = 'unable to run'
		return_value = db_controller.connection(config)
		self.assertIsNone(return_value['data'])
		self.assertEqual(return_value['state'],expected_message)
	#def test_get(self):
		#true
		# table not exist
		#no record found
	def test_get_all_table(self):
		#true
		config = {'client':'mysql','host':'127.0.0.1','port':3306,'user':'root','password':'','name':'DB'}
		connection = db_controller.connection(config)['data']
		self.assertEqual(db_controller.get_all_table(connection),['data'])
		self.assertEqual(len(db_controller.get_all_table(connection)),1)
		connection.close()
		# there's no table
		# config = {'client':'mysql','host':'127.0.0.1','port':3306,'user':'root','password':'','name':'BackupDB'}
		# connection = db_controller.connection(config)['data']
		# self.assertEqual(db_controller.get_all_table(connection),())
		# connection.close()
	def test_delete(self):
		#there's no table
		print('test_delete:')
		config = {'client':'mysql','host':'127.0.0.1','port':3306,'user':'root','password':'','name':'BackupDB'}
		connection = db_controller.connection(config)['data']
		tables = db_controller.get_all_table(connection)
		clause = "updated_date <= '2018-01-01'"
		expected_data = 0
		expected_mess = 'success'
		return_value = db_controller.delete(connection,clause,tables)
		self.assertEqual(return_value['data'],expected_data)
		self.assertEqual(return_value['state'],expected_mess)
		connection.close()

		#success
		config = {'client':'mysql','host':'127.0.0.1','port':3306,'user':'root','password':'','name':'DB'}
		connection = db_controller.connection(config)['data']
		tables = db_controller.get_all_table(connection)
		clause = "updated_date <= '2018-01-01'"
		expected_data = db_controller.get(connection,clause,tables)['data']
		expected_mess = 'success'
		return_value = db_controller.delete(connection,clause,tables)
		self.assertEqual(return_value['data'],expected_data)
		self.assertEqual(return_value['state'],expected_mess)
		connection.close()
		#there's no record found
		config = {'client':'mysql','host':'127.0.0.1','port':3306,'user':'root','password':'','name':'DB'}
		connection = db_controller.connection(config)['data']
		tables = db_controller.get_all_table(connection)
		clause = "updated_date >= '2018-11-01'"
		expected_data = 0
		expected_mess = 'success'
		return_value = db_controller.delete(connection,clause,tables)
		self.assertEqual(return_value['data'],expected_data)
		self.assertEqual(return_value['state'],expected_mess)
		connection.close()
		#no such data table
		config = {'client':'mysql','host':'127.0.0.1','port':3306,'user':'root','password':'','name':'BackupDB'}
		connection = db_controller.connection(config)['data']
		tables = ['data']
		clause = "updated_date <= '2018-01-01'"
		expected_data = 0
		expected_mess = 'bug'
		return_value = db_controller.delete(connection,clause,tables)
		self.assertEqual(return_value['data'],expected_data)
		self.assertEqual(return_value['state'],expected_mess)
		connection.close()

	def test_backup(self):
		# backup success
		config = {'client':'mysql','host':'127.0.0.1','port':'3306','user':'root','password':'','name':'DB'}
		connection = db_controller.connection(config)['data']
		tables = db_controller.get_all_table(connection)
		clause = 'updated_date <= \'2018-02-02\''
		expected_mess = 'success'
		return_value = db_controller.backup(config,clause,tables)
		self.assertIsNotNone(return_value['data'])
		self.assertEqual(return_value['state'],expected_mess)
		connection.close()
		# no such table
		config = {'client':'mysql','host':'127.0.0.1','port':'3306','user':'root','password':'','name':'BackupDB'}
		tables = ['datab']
		clause1 = "updated_date <= '2018-02-02'"
		expected_mess = 'success'
		return_value = db_controller.backup(config,clause1,tables)
		self.assertIsNone(return_value['data'])
		self.assertNotEqual(return_value['state'],expected_mess)
	def test_load(self):
		#success
		config = {'client':'mysql','host':'127.0.0.1','port':'3306','user':'root','password':'','name':'DB'}
		tables = ['data']
		clause = 'updated_date <= \'2018-02-02\''
		file = db_controller.backup(config,clause,tables)['data']
		backup_config = {'client':'mysql','host':'127.0.0.1','port':'3306','user':'root','password':'','name':'BackupDB'}
		return_value = db_controller.load(backup_config,file)
		self.assertEqual(return_value['data'],file)
		self.assertEqual(return_value['state'],'success')
		connection = db_controller.connection(backup_config)['data']
		number = db_controller.get(connection,clause,tables)['data']
		self.assertNotEqual(number,0)
		connection.close()

			# already have such table
		# config = {'client':'mysql','host':'127.0.0.1','port':3306,'user':'root','password':'','name':'DB'}
		# tables = ['data']
		# clause = "updated_date <= '2018-02-02'"
		# file = db_controller.backup(config,clause,tables)
		# backup_config = {'client':'mysql','host':'127.0.0.1','port':3306,'user':'root','password':'','name':'BackupDB'}
		# return_value = db_controller.load(backup_config,file)
		# self.assertEqual(return_value['data'],file)
		# self.assertEqual(return_value['state'],'success')
		# connection = db_controller.connection(backup_config)
		# number = get(connection,clause,tables)['data']
		# self.assertEqual(number,6)
		# connection.close()
			# record exist
		# config = {'client':'mysql','host':'127.0.0.1','port':3306,'user':'root','password':'','name':'DB'}
		# tables = ['data']
		# clause = "updated_date <= '2018-02-02'"
		# file = db_controller.backup(config,clause,tables)
		# backup_config = {'client':'mysql','host':'127.0.0.1','port':3306,'user':'root','password':'','name':'BackupDB'}
		# return_value = db_controller.load(backup_config,file)
		# self.assertEqual(return_value['data'],file)
		# self.assertEqual(return_value['state'],'success')
		# connection = db_controller.connection(backup_config)
		# number = get(connection,clause,tables)['data']
		# self.assertEqual(number,6)
		# connection.close()
		# no file
		file = "abc"
		backup_config = {'client':'mysql','host':'127.0.0.1','port':'3306','user':'root','password':'','name':'BackupDB'}
		return_value = db_controller.load(backup_config,file)
		self.assertIsNone(return_value['data'])
		self.assertEqual(return_value['state'],'unable to load file')


if __name__ == '__main__':
	unittest.main()
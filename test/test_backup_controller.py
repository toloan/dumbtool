import unittest
import sys
sys.path.append("../")
import backup_controller, db_controller
class TestIOController(unittest.TestCase):
	def test_delete(self):
		# true, no table list
		config = {'client':'mysql','host':'127.0.0.1','port':'3306','user':'root','password':'','name':'DB'}
		clause = "updated_date <= '2017-12-20'"
		connection = db_controller.connection(config)['data']
		deleted = sum(db_controller.get(connection,clause,db_controller.get_all_table(connection)).values())
		connection.close()
		result = backup_controller.delete(config,clause)
		connection = db_controller.connection(config)['data']
		count_all = sum(db_controller.get(connection,"1",db_controller.get_all_table(connection)).values())
		expected_data = {'all':count_all,'deleted':deleted,'error':0}
		expected_mes = 'success'
		connection.close()
		self.assertEqual(result['data'],expected_data)
		self.assertEqual(result['state'],expected_mes)


		# true, table list exist
		config = {'client':'mysql','host':'127.0.0.1','port':'3306','user':'root','password':'','name':'DB'}
		clause = "updated_date <= '2018-01-01'"
		tables = 'data'
		tb = tables.split(",")
		connection = db_controller.connection(config)['data']
		x = db_controller.get(connection,clause,tb)
		deleted = sum(x.values())
		connection.close()
		result = backup_controller.delete(config,clause,tables)
		connection = db_controller.connection(config)['data']
		count_all = sum(db_controller.get(connection,"1",db_controller.get_all_table(connection)).values())
		expected_data = {'all':count_all,'deleted':deleted,'error':0}
		expected_mes = 'success'
		connection.close()
		self.assertEqual(result['data'],expected_data)
		self.assertEqual(result['state'],expected_mes)

		# tablelist with one wrong one
		config = {'client':'mysql','host':'127.0.0.1','port':'3306','user':'root','password':'','name':'DB'}
		clause = "updated_date <= '2018-01-03'"
		tables = 'data,beta'
		tb = tables.split(",")
		connection = db_controller.connection(config)['data']
		deleted = sum(db_controller.get(connection,clause,tb).values())
		connection.close()
		result = backup_controller.delete(config,clause,tables)
		connection = db_controller.connection(config)['data']
		count_all = sum(db_controller.get(connection,"1",db_controller.get_all_table(connection)).values())
		expected_data = {'all':count_all,'deleted':deleted,'error':0}
		expected_mes = 'some records are not deleted'
		connection.close()
		self.assertEqual(result['data'],expected_data)
		self.assertEqual(result['state'],expected_mes)

		# not existed table list
		config = {'client':'mysql','host':'127.0.0.1','port':'3306','user':'root','password':'','name':'DB'}
		clause = "updated_date <= '2018-02-01'"
		tables = 'theta,beta'
		tb = tables.split(",")
		result = backup_controller.delete(config,clause,tables)
		connection = db_controller.connection(config)['data']
		count_all = sum(db_controller.get(connection,"1",db_controller.get_all_table(connection)).values())
		expected_data = {'all':count_all,'deleted':0,'error':0}
		expected_mes = 'some records are not deleted'
		connection.close()
		self.assertEqual(result['data'],expected_data)
		self.assertEqual(result['state'],expected_mes) 
#3def test_backup():
		# true, no table list
		# true, table list exist
		# backup failed
		# load failed

	def test_delete_backup(self):
		# true, no table list
		config = {'client':'mysql','host':'127.0.0.1','port':'3306','user':'root','password':'','name':'DB'}
		backup_config = {'client':'mysql','host':'127.0.0.1','port':'3306','user':'root','password':'','name':'BackupDB'}
		clause = "updated_date <= '2018-02-01'"
		connection = db_controller.connection(config)['data']
		deleted = sum(db_controller.get(connection,clause,db_controller.get_all_table(connection)).values())
		connection.close()
		result = backup_controller.delete_backup(config,backup_config,clause)
		connection = db_controller.connection(config)['data']
		count_all = sum(db_controller.get(connection,"1",db_controller.get_all_table(connection)).values())
		expected_data = {'all':count_all,'deleted':deleted,'error':0}
		expected_mes = 'success'
		connection.close()
		self.assertEqual(result['data'],expected_data)
		self.assertEqual(result['state'],expected_mes)
		# true, table list exist
		config = {'client':'mysql','host':'127.0.0.1','port':'3306','user':'root','password':'','name':'DB'}
		backup_config = {'client':'mysql','host':'127.0.0.1','port':'3306','user':'root','password':'','name':'BackupDB'}
		clause = "updated_date <= '2018-02-02'"
		tables = 'data'
		tb = tables.split(",")
		connection = db_controller.connection(config)['data']
		deleted = sum(db_controller.get(connection,clause,tb).values())
		connection.close()
		result = backup_controller.delete_backup(config,backup_config,clause,tables)
		connection = db_controller.connection(config)['data']
		count_all = sum(db_controller.get(connection,"1",db_controller.get_all_table(connection)).values())
		expected_data = {'all':count_all,'deleted':deleted,'error':0}
		expected_mes = 'success'
		connection.close()
		self.assertEqual(result['data'],expected_data)
		self.assertEqual(result['state'],expected_mes)
		# no such table)
		config = {'client':'mysql','host':'127.0.0.1','port':'3306','user':'root','password':'','name':'DB'}
		backup_config = {'client':'mysql','host':'127.0.0.1','port':'3306','user':'root','password':'','name':'BackupDB'}
		clause = "updated_date <= '2018-03-03'"
		tables = 'theta,beta'
		result = backup_controller.delete_backup(config,backup_config,clause,tables)
		expected_mes = 'false to backup'
		self.assertIsNone(result['data'])
		self.assertEqual(result['state'],expected_mes) 
		# no backup config:
		config = {'client':'mysql','host':'127.0.0.1','port':'3306','user':'root','password':'','name':'DB'}
		backup_config = {'client':'mysql','host':'127.0.0.1','port':'3306','user':'root','password':'','name':'XSackupDB'}
		clause = "updated_date <= '2018-04-04'"
		tables = 'theta,beta'
		result = backup_controller.delete_backup(config,backup_config,clause,tables)
		expected_mes = 'false to backup'
		self.assertIsNone(result['data'])
		self.assertEqual(result['state'],expected_mes)

if __name__ == '__main__':
	unittest.main()
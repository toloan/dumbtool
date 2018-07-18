import unittest
import sys
from collections import OrderedDict
sys.path.append("../")
import io_controller
class TestIOController(unittest.TestCase):
	def test_get_config(self):
		self.maxDiff = None
		# true, k table
		test_list = ['-f','config_test/test_config1','-m','backup-delete','-w',"updated_date <= '2018-01-01'"]
		return_value = io_controller.get_config(test_list)
		print(return_value['data'])
		expected_data = {'RemoteDB':OrderedDict([
							('client','sql'),
							('port','3306'),
							('host','127.0.0.1'),
							('name','DB'),
							('user','root'),
							('password','')]),
						'BackupDB':OrderedDict([
							('client','sql'),
							('port','3306'),
							('host','127.0.0.1'),
							('name','BackupDB'),
							('user','root'),
							('password','')]),
						'mode': 'backup-delete',
						'clause':"updated_date <= '2018-01-01'",
						'tables':None
						}
		expected_message = 'success'
		self.assertEqual(return_value['data'],expected_data)
		self.assertEqual(return_value['state'],expected_message)

		# true, co table
		test_list = ['-f','config_test/test_config1','-m','backup-delete','-tb','data','-w',"updated_date <= '2018-01-01'"]
		return_value = io_controller.get_config(test_list)
		expected_data = {'RemoteDB':OrderedDict([
							('client','sql'),
							('port','3306'),
							('host','127.0.0.1'),
							('name','DB'),
							('user','root'),
							('password','')]),
						'BackupDB':OrderedDict([
							('client','sql'),
							('port','3306'),
							('host','127.0.0.1'),
							('name','BackupDB'),
							('user','root'),
							('password','')]),
						'mode': 'backup-delete',
						'clause':"updated_date <= '2018-01-01'",
						'tables':'data'
						}
		expected_message = 'success'
		self.assertEqual(return_value['data'],expected_data)
		self.assertEqual(return_value['state'],expected_message)
		# sai ten truong
		test_list = ['-f','config_test/test_config1','-mn','backup-delete','-w',"updated_date <= '2018-01-01'"]
		return_value = io_controller.get_config(test_list)
		expected_message = 'python DBBackupCleaner.py --help をチェック見てください'
		self.assertEqual(return_value['data'],None)
		self.assertEqual(return_value['state'],expected_message)
		# config chi co db delete and backup-delete
		test_list = ['-f','config_test/test_config2','-m','delete','-w',"updated_date <= '2018-01-01'"]
		return_value = io_controller.get_config(test_list)

		expected_data = {'RemoteDB':OrderedDict([
							('client','sql'),
							('port','3306'),
							('host','127.0.0.1'),
							('name','DB'),
							('user','root'),
							('password','')]),
						'mode': 'delete',
						'clause':"updated_date <= '2018-01-01'",
						'tables':None
						}
		expected_message = 'success'
		self.assertEqual(return_value['data'],expected_data)
		self.assertEqual(return_value['state'],expected_message)
		# wrong format: have abc key in db
		test_list = ['-f','config_test/test_config3','-m','delete','-w',"updated_date <= '2018-01-01'"]

		return_value = io_controller.get_config(test_list)
		expected_message = 'RemoteDBにabcのキーワードがありません.python DBBackupCleaner.py --help をチェック見てください'
		self.assertEqual(return_value['data'],None)
		self.assertEqual(return_value['state'],expected_message)
		# wrong format: dont have password key in db
		test_list = ['-f','config_test/test_config4','-m','delete','-w',"updated_date <= '2018-01-01'"]

		return_value = io_controller.get_config(test_list)
		expected_message = 'RemoteDBのpasswordのキーワードがありません.python DBBackupCleaner.py --help をチェック見てください'
		self.assertEqual(return_value['data'],None)
		self.assertEqual(return_value['state'],expected_message)
		# wrong format: have abc key in backup db
		test_list = ['-f','config_test/test_config5','-m','backup-delete','-w',"updated_date <= '2018-01-01'"]
		return_value = io_controller.get_config(test_list)
		expected_message = 'BackupDBにabcのキーワードがありません.python DBBackupCleaner.py --help をチェック見てください'
		self.assertEqual(return_value['data'],None)
		self.assertEqual(return_value['state'],expected_message)
		# wrong format: dont have password, client in backup db
		test_list = ['-f','config_test/test_config6','-m','backup-delete','-w',"updated_date <= '2018-01-01'"]

		return_value = io_controller.get_config(test_list)
		expected_message = 'BackupDBのclient,passwordのキーワードがありません.python DBBackupCleaner.py --help をチェック見てください'
		self.assertEqual(return_value['data'],None)
		self.assertEqual(return_value['state'],expected_message)

if __name__ == '__main__':
	unittest.main()
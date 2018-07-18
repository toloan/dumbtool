import sys
import json
import io_controller
import db_controller
import backup_controller
def main(argv):
	if len(argv)==2:
		if(argv[1]=='--help'or  argv[1]=='-h'):
			io_controller.help()
		else:
			io_controller.output(None,json.dumps({"状態:":"フォーマットが間違いました。python DBBackupCleaner.py --help をチェック見てください"}) )
	elif len(argv) == 9 or len(argv) == 7:
		# get config- return a dictionary // state
		return_dict = io_controller.get_config(argv[1:])
		config = return_dict['data']
		state = return_dict['state']
		if state == 'success':
			if config['mode'] == 'delete':
				if config['table'] !=None:
					output = backup_controller.delete(config['RemoteDB'],config['clause'],config['tables'])
					io_controller.output(output['data'],output['state'])

				else:
					output = backup_controller.delete(config['RemoteDB'],config['clause'])
					io_controller.output(output['data'],output['state'])
			else:
				if config['tables'] !=None:
					output = backup_controller.delete_backup(config['RemoteDB'],config['BackupDB'],config['clause'],config['tables'])
					io_controller.output(output['data'],output['state'])

				else:
					output = backup_controller.delete_backup(config['RemoteDB'],config['BackupDB'],config['clause'])
					io_controller.output(output['data'],output['state'])
		else:
			io_controller.output(config,state)
	else:
		# wrong number of argument
		io_controller.output(None,"format error。python DBBackupCleaner.py --help check")
#main(sys.argv)

test_list = ['DBBackupCleaner','-f','config_info','-m','backup-delete','-w',"updated_date <= '2018-01-01'"]
main(test_list)


import os

try:
	import paramiko
except ModuleNotFoundError as err:
	os.system("pip install paramiko")
	print("ALL DONE!!\nRestart the terminal and rerun the program")

ssh_client = None

class MIKROTIK_DEVICE():
	"""
	--> `USAGE:`
			  (*)device = MIKROTIK_DEVICE(ip_addr,user,passwd)

			  (*)device.connect()

			  (-)device.execute(command)
						. . .
			  (-)device.clear_logs()
						
			  (*)device.close_handle()

	--> `NOTE:`
				(*) -> required

				(-) -> optional

	"""

	def __init__(self,ipaddr:str = "192.168.88.1",user:str = "admin",passwd:str = "admin",quiet:bool = True) -> None:
		if not quiet:
			self.banner()
		self.ipaddr = ipaddr
		self.user = user
		self.passwd = passwd

	def banner(self) -> None:
		print("""
  MMM      MMM       KKK                          TTTTTTTTTTT      KKK
  MMMM    MMMM       KKK                          TTTTTTTTTTT      KKK
  MMM MMMM MMM  III  KKK  KKK  RRRRRR     OOOOOO      TTT     III  KKK  KKK
  MMM  MM  MMM  III  KKKKK     RRR  RRR  OOO  OOO     TTT     III  KKKKK
  MMM      MMM  III  KKK KKK   RRRRRR    OOO  OOO     TTT     III  KKK KKK
  MMM      MMM  III  KKK  KKK  RRR  RRR   OOOOOO      TTT     III  KKK  KKK
""")
		
	def connect(self) -> None:
		"""-->`Connect` to ssh client with supplied host"""
		global ssh_client
		try:
			ssh_client = paramiko.SSHClient()
			ssh_client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy)
			ssh_client.connect(hostname=self.ipaddr,username=self.user,password=self.passwd)
		except Exception as err:
			print(err)

	def execute(self, command:str) -> str:
		"""-->`Execute` command in mikrotik device and return the output"""
		global ssh_client
		try:
			stdin,stdout,stderr = ssh_client.exec_command(command)
			if stdout.channel.recv_exit_status() == 1 : print('Command failed!')
			if stderr:
				for line in stderr: print(line)
			reply =""
			for line in stdout:
				reply+=line
			stdin.close()
			stdout.close()
			stderr.close()
			return reply
		except Exception as err:
			print(err)

	def clear_logs(self) -> None:
		"""-->`Clear` the logs"""
		global ssh_client
		try:
			self.execute("/system logging action set memory memory-lines=1")
			self.execute("/system logging action set memory memory-lines=100")
		except Exception as err:
			print(err)
	
	def close_handle(self) -> None:
			"""-->`Close` ssh client handle"""
			global ssh_client
			try:
				ssh_client.close()
			except Exception as err:
				print(err)
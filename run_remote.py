# +========================================================================+
# |                   		      Kalyan VS                  	 	       |
# |                           kalyanvsc@gmail.com                          |
# +========================================================================+
# |                                                                        |
# |                                                                        |
# |Description      : Generate Health Check Report for SSH Enabled Devices |
# |                                                                        |
# |                                                                        |
# |Change History:                                                         |
# |---------------                                                         |
# |Version  Date       Author                 Remarks                      |
# |-------  ---------- ------------------ ---------------------------------|
# |Ver 1.0  05-06-2020 V.Srinivas Kalyan    Initial Version                |
# +========================================================================+

from cryptography.fernet import Fernet
from genencryptpasswdvalue import get_key
import pexpect
import sys
import os
import datetime
import logging
import configparser


def usage():
	"""Show command usage."""
	msg = ('\n\tUsage:  '+sys.argv[0]+' config_file_name \n\n'
		'\tExample: '+sys.argv[0]+' devices.cfg\n\n'
                '\tOPTIONAL Values:\n'
                '\t\tconfig_file_name ---> Name of the file that has remote devices access and command details, case sensitive\n'
		'\t\t                      If no file name is specified, uses default devices.cfg\n')
	print(msg)
	sys.exit()

def echomsg(msg):
	print ("\t\t"+msg)
	logger.info(msg)

def check_file_folder(file_folder):
	root_folder = os.getcwd()
	
	if not os.path.isdir(os.path.join(root_folder,file_folder)):
		try:
			print ("\t\tCreating Log Directory as it doesn't exist")
			os.makedirs(os.path.join(root_folder,file_folder))
		except OSError as oserr:
			print(oserr)
			sys.exit(1)
	return os.path.join(root_folder,file_folder)

def startlog(filename,level):
	global logger
	log_loc = check_file_folder('logs')
	mylogfile=log_loc+"/"+os.path.basename(filename)
	formatter = logging.Formatter('%(asctime)s  %(name)s  %(levelname)s  %(funcName)s:%(lineno)d  %(message)s')
	logger = logging.getLogger(sys.argv[0])
	hdlr = logging.FileHandler(mylogfile)
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr)

	if level.upper().strip() == "INFO":
		logger.setLevel(logging.INFO)
	elif level.upper().strip() == "DEBUG":
		logger.setLevel(logging.DEBUG)
	elif level.upper().strip() == "WARNING":
		logger.setLevel(logging.WARNING)
	elif level.upper().strip() == "ERROR":
		logger.setLevel(logging.ERROR)
	elif level.upper().strip() == "CRITICAL":
		logger.setLevel(logging.CRITICAL)

	print("\n")
	echomsg ("Recording Log Information in "+mylogfile)
	echomsg ("Author: Kalyan VS (kalyanvsc@gmail) \n")
	return (logger, mylogfile)

def errors(msg,err):
	print ("\n\tERROR ***** "+msg+" *****\n")
	logger.error("\n\tERROR ***** "+msg+" *****\n")
	print ("\t"+str(err)+"\n")
	logger.error("\t\t"+str(err))
	sys.exit(1)

def check_conn(username, passwd, srvrip, port, cmdstr, cmdtimeo):
	rtn = 0

	rusure = "Are you sure you want to continue connecting"
	hosterr = "Could not resolve hostname"
	timeerr = "Connection timed out"
	chngdid = "Add correct host key"
	
	cmd = 'ssh %s@%s -p %s "%s"' % (username, srvrip, port, cmdstr)
	child = pexpect.spawn(cmd, timeout=cmdtimeo)
	chk = child.expect([rusure,
                            'Password: ',
                            'password: ',
                            pexpect.EOF,
                            'Permission denied',
                            hosterr,
                            timeerr,
                            pexpect.TIMEOUT,
                            chngdid])

	while chk is not None:
		errmsg = ""
		output = ""
		if chk == 0 or chk == 1:
			child.sendline('yes')
			chk = child.expect([rusure,
                                    'Password: ',
                                    'password: ',
                                    pexpect.EOF,
                                    'Permission denied',
                                    hosterr,
                                    timeerr,
                                    pexpect.TIMEOUT,
                                    chngdid])
		elif chk == 2:
			child.sendline(passwd)
			chk = child.expect([rusure,
                                    'Password: ',
                                    'password: ',
                                    pexpect.EOF,
                                    'Permission denied',
                                    hosterr,
                                    timeerr,
                                    pexpect.TIMEOUT,
                                    chngdid])
		elif chk == 3:
			output = child.before.splitlines()
			rtn = 0
			chk = None
			child.close()	
			pass
		elif chk == 4:
			echomsg("incorrect password for %s on %s" % (username, srvrip))
			errmsg = "incorrect password for %s on %s" % (username, srvrip)
			chk = None
		elif chk == 5:
			echomsg("incorrect hostname or IP %s" % srvrip)
			errmsg = "incorrect hostname or IP %s" % srvrip
			chk = None
		elif chk == 6:
			echomsg("ssh connection timeout trying to execute ssh: %s" % cmdstr)
			errmsg = "ssh connection timeout trying to execute ssh: %s" % cmdstr
			chk = None
		elif chk == 7:
			echomsg("pexpect timeout while waiting for ssh: %s" % cmdstr)
			errmsg = "pexpect timeout while waiting for ssh: %s" % cmdstr
			chk = None
		elif chk == 8:
			echomsg("ssh host key verification failed for: %s" % srvrip)
			echomsg("Run the following on %s to understand the problem: %s" % (srvrip, cmd))
			errmsg = "ssh host key verification failed for: %s" % srvrip
			chk = None
	return rtn,output,errmsg

def send_email(smtp_server,smtp_port,sender_email,password,receiver_emai,filename,logfile):
	import email, smtplib, ssl
	from email import encoders
	from email.mime.base import MIMEBase
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText

	body = "Dear All, \n\n\t\tPlease check attachements for Devices Health Check Reports\n\nThanks & Regards\nKalyan"

	message = MIMEMultipart()
	message["From"] = sender_email
	message["To"] = receiver_email
	message["Subject"] = "Devices Health Check - RAW Data"
	message.attach(MIMEText(body, "plain"))
	for attachfile in [filename, logfile]:
		with open(attachfile, "rb") as attachment:
    			part = MIMEBase("application", "octet-stream")
    			part.set_payload(attachment.read())
		encoders.encode_base64(part)
		part.add_header(
    			"Content-Disposition",
    			f"attachment; filename= {attachfile}",
		)
		message.attach(part)
	text = message.as_string()
	context = ssl.create_default_context()
	try:
		with smtplib.SMTP_SSL(smtp_server,smtp_port, context=context) as server:
    			server.login(sender_email, password)
    			server.sendmail(sender_email, receiver_email.split(','), text)
	except Exception as e:
		errors("Unable to Send the Mail, Please check the configuration details",e)


if __name__ == "__main__":

	### print the command syntax ###
	if len(sys.argv) > 1:
		if sys.argv[1].upper() == "--HELP":
			usage()

	if len(sys.argv) > 1:
		input_file = sys.argv[1]
	else:
		input_file = 'devices.cfg'

	parser = configparser.RawConfigParser()
	### Validate the input file existence ###
	if not os.path.isfile(input_file):
		print("\n\t\t***** ERROR: File '"+input_file+"' Doesn't Exist *****")
		usage()
	else:
		parser.read(input_file)

	root_folder = os.getcwd()
	logger,logfile=startlog(sys.argv[0]+"_"+datetime.datetime.now().strftime("%d-%m-%Y_%H_%M_%S")+".log","INFO")
	data_loc = check_file_folder('data')
	data_file = data_loc+"/"+sys.argv[0]+"_"+datetime.datetime.now().strftime("%d-%m-%Y_%H_%M_%S"+".data")

	cipher_suite = Fernet(get_key())
	write_data = open(data_file, "w")
	for section_name in parser.sections():
		for eachkey,eachvalue in parser.items(section_name):
			locals()[eachkey]=eachvalue
		if section_name.lower() == "general":
			##### Checking and Removing Log and Data files based on retention value #####
			try:
				os.system("find ./data -type f -mtime +"+reports_retention+" -exec rm -f {} \;")
				os.system("find ./logs -type f -mtime +"+reports_retention+" -exec rm -f {} \;")
				echomsg("Cleared Log and Data Files as per Retention Period : "+str(reports_retention))
			except:
				echomsg("\t**** WARNING **** No Retention Period mentioned for Log and Data files hence not clearing the files from disk ")

		if not (section_name.lower() == "general" or section_name.lower() == "mail"):
			try:
				password = cipher_suite.decrypt(bytes(userpasswd,'utf-8')).decode('utf-8')
			except:
				errors("Invalid Encrypted Password Value",userpasswd)

			write_data.write(section_name+" : \n\n")

			exec_commands = commands.replace('"','').split(",")

			echomsg("Connecting Device : "+str(device_ip)+"->"+section_name)

			for eachcommand in exec_commands:
				write_data.write("\tExecuting Command : "+eachcommand.strip()+"\n")
				rtn,output,error = check_conn(username, password, device_ip,ssh_port, eachcommand.strip(), 60)
				if len(error) == 0:
					for eachitem in output:
						if not ("exit" in str(eachitem) or "skalyan" in str(eachitem)):
							write_data.write("\t\t"+eachitem.decode('utf-8')+"\n")
				else:
					echomsg("\t**** ERROR **** Unable to Access Device Due to "+error)
					write_data.write("\t**** ERROR **** Unable to Access Device Due to "+error+"\n\n")
					break
				write_data.write("\n")
	write_data.close()
	echomsg('\n\t\tData File Created Successfully at : '+data_file)

	##### Below Section for Sending Email #####
	echomsg('\n\t\tSending Email to the Recipients')
	try:
		smtp_server
		smtp_port 
		sender_email
		sender_email_password
		receiver_email 
	except NameError:
		echomsg("\n\t**** Required Parameters 'smtp_server', 'smtp_port', 'sender_email', 'sender_email_password' and 'receiver_email' not specified to send email notification ****\n")

	send_email(smtp_server,smtp_port,sender_email,cipher_suite.decrypt(bytes(sender_email_password,'utf-8')).decode('utf-8'),receiver_email,data_file,logfile)
	echomsg('\n\t\tEmail Sent Successfully to the Recipients')



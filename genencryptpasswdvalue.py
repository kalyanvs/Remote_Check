# +========================================================================+
# |                   		Kalyan VS                    	 	   |
# |                           kalyanvsc@mdcbms.ae                          |
# +========================================================================+
# |                                                                        |
# |                                                                        |
# |Description      : Generate Encrypyed Password for the value 	   |
# |                                                                        |
# |                                                                        |
# |Change History:                                                         |
# |---------------                                                         |
# |Version  Date       Author                 Remarks                      |
# |-------  ---------- ------------------ ---------------------------------|
# |Ver 1.0  05-06-2020 V.Srinivas Kalyan    Initial Version                |
# +========================================================================+

from cryptography.fernet import Fernet
import getpass

def get_key():
	key = b'Abcdefghijklmnopqrstuvwxyz_1234567890_09876='
	return (key)

if __name__ == "__main__":
	cipher_suite = Fernet(get_key())
	password = ""
	while password.strip() == "":
		password = getpass.getpass("Enter the value to generate envrypted password : ")

	print("Encrypted Value for the given Password is below ")
	print(cipher_suite.encrypt(bytes(password,'utf-8')).decode('utf8').replace("'", '"'))

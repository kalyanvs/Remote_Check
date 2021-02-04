## About The Project

This Python script allows you to captures the output of remotely executed commands and sends an email. You can pass any command that is supported on the target. The target is not only limited to servers, you can use against storages, switches etc., while SSH connection is supported.  

### Built With

The project is developed in Python 3.7.

## Features

- User/email passwords are encrypted
- Configurable retention period for reports and log files 

## Getting Started

### Prerequisites

A Linux machine with Python3.x or above with following modules 

- [ ] cryptography : For license and other details check https://pypi.org/project/cryptography/

  pip install cryptography

- [ ] pexpect : For license and other details check https://pypi.org/project/pexpect/

  pip install pexpect

### Installation & Configuration

Clone the repo from

​	https://github.com/kalyanvs/Remote_Check.git

The project contains the following files

1. genencryptpasswdvalue.py - This program will be used to provide encrypted values of a password

2. run_remote.py - This program executes the commands 

3. devices.cfg - The configuration file


#### Configuring device information

The configuration file (devices.cfg) contains three different sections i.e. **general, mail** and **device information**. Following is the format that you need to provide for devices. Please note for each device you have to create a dedicated block/section. 

```
[Name of The Device]
username = <account that is already exists on the target device to run the specified commands>
userpasswd = <the encrypted value of the password>** 
device_ip = <host name or IP address of the device>
ssh_port = <ssh port information>
commands = <command that you would like to execute on this device. The command should be mentioned within double quotes and comma seperated>
```

Below is the example:

```
[Primary_Storage]
username = kalyan
userpasswd = gAAAAABgFAT9Xla7a386Gixgvw0KfDirD3jYLDxSxKowgbxsZsF1zhPHQzPJn6b4ivlmRDHK7YlylDV2NN6xgDob8owmv
device_ip = 12.1.80.1
ssh_port = 22
commands = "puredrive list ", "purearray list --controller ", "purearray list --space ", "puremessage list --open"
```

#### Configuring Email Notification

In order to receive the report and log outputs (.txt file) through email you need to provide following details. 

Note:- The project is tested with gmail smtp server. 

```
[mail]
smtp_server=smtp.gmail.com
smtp_port=465
sender_email = test@gmail.com
sender_email_password = gAAAAABgFAT9Xla7a386Gixgvw0KfDirD3jYLDxSxKowgbxsZsF1zhPHQzPJn6b4i
receiver_email=test@gmail.com, test@yahoo.com
```

#### Configuring Log and Reports Retention

By default the output and log files will be retained for 7 days on the system where the code is running. Under general configuration you can adjust this based on your requirement

```
[general]
reports_retention=7
```

#### Generate Encrypted Password Value

It's highly recommended to store the passwords in encrypted mode instead of clear text. For this project you can run below command to generate encrypted value for "userpasswd" and "sender_email_password" fields in devices.cfg file.

```
python genencryptpasswdvalue.py 
Enter the value to generate envrypted password : 
```

Once you enter the password the encrypted value will be returned by the program, similar to below

```
gAAAAABgFAT9Xla7a386Gixgvw0KfDirD3jYLDxSxKowgbxsZsF1zhPHQzPJn6b4ivlmRDHK7YlylDV2NN6xgDob8owmv==
```

Copy and paste the encrypted value in devices.cfg for respective device

### Execution

After creating the configuration information you can run the below command to execute and generate report.

```
python run_remote.py
```

By default the code will read the configuration from from "devices.cfg" file. In case you want to use another configuration files you can run the command as below

```
python run_remote.py custom_file.txt
```

To get the command help:

```
python run_remote.py --help
```

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Kalyan VS - kalyanvsc@gmail.com

Project Link: https://github.com/kalyanvs/Remote_Check.git






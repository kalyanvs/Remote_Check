## About The Project

In any enterprise environment customers do implement monitoring tools, which requires additional configuration and plug-ins for some devices in order to get the required information. The target of this project is provide a tool that can fetch required information for daily administration from any SSH enabled devices like Linux/Unix, storage, network devices etc. Though there are monitoring tools, the administrator will have to access the devices on daily basis to check the health of the devices using various commands. This project majorly helps to avoid the manual intervention. 

### Built With

The project is developed in Python 3.7.

If you need binaries please check https://kalyanvsc.blogspot.com/2020/11/run-remote-checks_7.html

## Getting Started

Make sure that you have installed Python on the server where you want to deploy this code

### Prerequisites

Install following modules 

- [ ] cryptography

  pip install cryptography

- [ ] pexpect

  ​	pip install pexpect

### Installation

Clone the repo from

​	https://github.com/kalyanvs/Remote_Check.git

## Usage

The project contains the following files

1. genencryptpasswdvalue.py - This program will be used to provide encrypted values of a password

2. run_remote.py - This program executes the commands 

3. devices.cfg - The configuration file


### Configuring device information

The configuration file (devices.cfg) contains three different sections i.e. **general, mail** and **device information**. Following is the format that you need to provide device information. Please note for each device you have to create a dedicated block/section. 

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
[Primary_PureStorage]
username = kalyan
userpasswd = gAAAAABgFAT9Xla7a386Gixgvw0KfDirD3jYLDxSxKowgbxsZsF1zhPHQzPJn6b4ivlmRDHK7YlylDV2NN6xgDob8owmv
device_ip = 12.1.80.1
ssh_port = 22
commands = "puredrive list ", "purearray list --controller ", "purearray list --space ", "puremessage list --open"
```

### Configuring Email Notification

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

### Configuring Log and Reports Retention

By default the output and log files will be retained for 7 days on the system where you are running this code. Under general configuration you can adjust this based on your requirement

```
[general]
reports_retention=7
```

### Generate Encrypted Password Value

it's always recommended to store the passwords in encrypted mode instead of clear text. For this project you can run below command to generate encrypted value for "userpasswd" and "sender_email_password" fields in devices.cfg file.

```
python genencryptpasswdvalue.py 
Enter the value to generate envrypted password : 
```

Once you enter the password the encrypted value similar to below will be returned by the program

```
gAAAAABgFAT9Xla7a386Gixgvw0KfDirD3jYLDxSxKowgbxsZsF1zhPHQzPJn6b4ivlmRDHK7YlylDV2NN6xgDob8owmv==
```

Copy and paste the encrypted value in devices.cfg for respective device

### Generate Encrypted Password Value

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

Project Binary Files: https://kalyanvsc.blogspot.com/2020/11/run-remote-checks_7.html 

## Acknowledgements

https://pypi.org/project/cryptography/

https://pypi.org/project/pexpect/
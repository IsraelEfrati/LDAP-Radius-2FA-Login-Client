# LDAP-Radius-2FA-Login-Client
Instructions on how to install and configure LDAP and Radius servers to incorporate Google Authenticator

# LDAP 
## Installations

Run the following:

mkdir LDAP              
cd ./LDAP                                                       
Git clone https://github.com/osixia/docker-openldap.git                         
Git clone https://github.com/osixia/docker-phpLDAPadmin.git

Download and run this script:
https://github.com/IsraelEfrati/LDAP-Radius-2FA-Login-Client/blob/main/start_ldap_and_gui.sh

## Adding new users
In your browser go to:
https://localhost:6443
                    
Select login and enter the following credentials:

Login DN: cn=admin,dc=example,dc=org        
Password: admin

 ![Alt text](https://github.com/IsraelEfrati/screenshoots/blob/main/1.png?raw=true "Optional Title")
 
Create group: my_users              
Select dc=example,dc=org -> 'Create new entry here' 

In the 'group' field write 'my_users'

Click on 'create object' and 'commit' in the next page
 
Select 'cn=my_users' and select 'create a child entry'      
Enter first and last name, create a password and select 
'my_users' in the  'GID Number' dropdown.       

Select 'create object' 

Select  'Add new attribute' 

Select 'Email' in the 'Add Attribute' dropdown.     
The value of the email should be <User ID>@example.org      
The user Id was created in previous stage when the user was added.
      
Click on 'update object' 

  # Google Authenticator
## Installations        
apt-get install libpam-google-authenticator

## Create New Linux User
Run the command:        
sudo adduser <ldap User Id>     
set password and leave the other fields empty       

## Set up Google Authenticator
run the commands:       
su <ldap user id>       
cd ~        
google-authenticator        

enter 'y' for the first question        
scan the QR code in your google authenticator app       
enter 'y'       
enter y/n for the remaining questions       
run the command 'exit'


# FreeRADIUS
## Installations   
apt-get update      
apt-get upgrade     
apt-get install freeradius freeradius-common freeradius-utils freeradius-ldap
 

## Configuring FreeRADIUS

#### /etc/freeradius/3.0/radiusd.conf        

Under the 'security' section change the user and group to root:
```
user = root         
group = root
```
 
#### /etc/freeradius/3.0/users
Add the following lines to the file:
```
DEFAULT 	Ldap-Group == "cn=my_users,dc=example,dc=org" 
            Reply-Message = "You are Accepted"
```

#### /etc/freeradius/3.0/sites-enabled/default
Add the following lines in the 'authorize' section:
```
filter_uuid
filter_google_otp
```

Under the line: '#  The ldap module reads passwords from the LDAP database.':        
Remove the '-' before ldap
```
'ldap'
```

Add the following  lines in the 'authenticate' section:     
```
Auth-Type PAP {
		pap 
		if (&Google-Password) {
			 update request { 
			 	&User-Name := "%{&User-UUID}" 
			 	&User-Password := "%{&Google-Password}" 		 	
			 	} 
			 pam 
		} 
		else { 
			update reply { 
				Reply-Message := "Login incorrect: TOTP Fail" 
				} 
			reject 
		} 

	}
```

#### /etc/freeradius/3.0/policy.d/filter
Add the following:
```
filter_uuid {  
	if (&User-Name =~ /^(.*)@(.*)$/) { 
		update request { 
			&User-UUID := "%{1}" 
		} 
	} 
}

filter_google_otp { 
	if (&User-Password =~ /^(.*)([0-9]{6})$/) {
		update request { 
			&Google-Password := "%{2}"
			&User-Password := "%{1}" 
			
		} 
		
	} 
}
```

#### /etc/freeradius/3.0/dictionary
Add the following:
```
ATTRIBUTE 	Google-Password 		3000 	string 
ATTRIBUTE 	User-UUID 			    3001    string
```
#### /etc/freeradius/3.0/clients.conf

Add the following:
```
client MyComputer { 
	ipaddr = *
	secret = testing123 }
```

It is best to change the 'secret' for security reasons

#### /etc/freeradius/3.0/mods-available/ldap
In the 'ldap' section:      
Change the server to the ip where the ldap server is running:
```
server = 'localhost'
```

change the following values to the ldap server admin identity and password with which the radius will query the ldap server.
```
identity = 'cn=admin,dc=example,dc=org'
password = admin
```
change the following value:
```
base_dn = 'cn=my_users,dc=example,dc=org'
```
under the 'user' section change the filter to:
```
filter = "(mail=%{%{Stripped-User-Name}:-%{User-Name}})"
```

under the 'group' section change the filter to:
```
filter = '(objectClass=GroupOfNames)'
```

under the 'membership filter' section change the filter to:
```
membership_filter = "(|(&(objectClass=GroupOfNames)(member=%{control:Ldap-UserDn}))(&(objectClass=GroupOfNames)(member=%{control:Ldap-UserDn})))"
```

Run the following command:      
sudo ln -s  /etc/freeradius/3.0/mods-available/ldap  /etc/freeradius/3.0/mods-enabled/ldap


#### /etc/pam.d/radiusd 
Add the following line:
```
auth required pam_google_authenticator.so forward_pass
```
comment out the rest of the lines:
```
#@include common-auth
#@include common-account
#@include common-password
#@include common-session
```

Run the following command:      
sudo ln -s /etc/freeradius/3.0/mods-available/pam /etc/freeradius/3.0/mods-enabled

## Run freeRADIUS

#### To restart the freeRADIUS service:     
systemctl restart freeradius.service

#### To run freeRADIUS with logging run the following :
systemctl stop freeradius.service       
sudo freeradius -XXX > ./debug.txt


## Test configuration:
Run the following:
radtest <ldap user email>  <ldap user password + google authenticator code> localhost 1812 testing123
 
# Login Client
Download the python login client by running following:      
Git clone https://github.com/IsraelEfrati/LDAP-Radius-2FA-Login-Client.git

Run the project and browse to the URL in the output.

Provide user email, password and google passcode from the app.


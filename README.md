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
 

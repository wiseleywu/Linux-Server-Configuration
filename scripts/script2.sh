#!/bin/bash

# move git directory to where the app will be hosted
sudo mv /root/FlaskApp/ /var/www/

# Enable wsgi, restart apache
sudo a2enmod wsgi
sudo service apache2 restart

cd /var/www
# copy FlaskApp.conf to the approriate location
sudo cp FlaskApp/FlaskApp.conf /etc/apache2/sites-available/FlaskApp.conf

# using postgres account to create database called biologics-catalog
sudo -u postgres createdb biologics-catalog
# setup user catalog with password catalog
sudo -u postgres psql postgres <<EOF
create user catalog PASSWORD 'catalog';
EOF
# populate database with pre-defined entries (optional)
sudo python FlaskApp/FlaskApp/populator.py
# enable write access to /static/images in order for user to upload images
sudo chmod -R 777 FlaskApp/FlaskApp/static/images/
# enable virtual host of FlaskApp, then restart apache
sudo a2ensite FlaskApp
sudo service apache2 restart
# at this point, the web app should be functional

# create .ssh directory in grader's home
cd
mkdir .ssh

# run ssh-keygen in local environment, create ssh key pair
# copy the public key generated and paste it to .ssh/authorized_keys
echo "Run 'ssh-keygen' in your local environment, then paste the public key you have generated below:"
read varname
echo -e $varname >> .ssh/authorized_keys

# reconfigure file permission
chmod 700 .ssh
chmod 644 .ssh/authorized_keys

# change the SSH password authentication back to no
word="PasswordAuthentication yes"
rep="PasswordAuthentication no"
sudo sed -i "s/${word}/${rep}/" /etc/ssh/sshd_config
# restart ssh again
sudo service ssh restart

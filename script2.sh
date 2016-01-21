#!/bin/bash

# logout, relogin as grader, used password set earlier
exit
ssh -p 2200 grader@52.32.26.12

# git clone catalog app to /var/www/FlaskApp
cd /var/www
sudo git clone https://github.com/wiseleywu/Linux-Server-Configuration.git FlaskApp
# copy FlaskApp.conf to the approriate location
sudo cp /FlaskApp/FlaskApp.conf /etc/apache2/sites-available/FlaskApp.conf

# create and login PostgreSQL as user postgres
sudo -u postgres psql postgres


sudo -u grader createdb biologics-catalog

# populate database with pre-defined entries (optional)
sudo python FlaskApp/FlaskApp/populator.py


# create .ssh directory in grader's home
mkdir .ssh
# create .ssh/authorized_keys for ssh with public key
touch .ssh/authorized_keys
# run the follow in local environment, create ssh key pair
ssh-keygen # create a key-pair called secured_key.rsa either with or without passphrase
# copy the content within secured_key.pub file created earlier and paste into authorized_keys
nano .ssh/authorized_keys # make sure the key is only one line with no line follow
# reconfigure file permission
chmod 700 .ssh
chmod 644 .ssh/authorized_keys
# loggout, relogin with keyphrase
ssh -p 2200 -i ~/.ssh/secured_key.rsa grader@52.32.26.12
# if it works, change the SSH password authentication back to no
word='PasswordAuthentication[[:space]]yes'
rep='PasswordAuthentication no'
sudo sed -i "s/${word}/${rep}/" /etc/ssh/sshd_config
# restart ssh again
sudo service ssh restart
# retry loginning in with key
ssh -p 2200 -i ~/.ssh/secured_key.rsa grader@52.35.43.61

#!/bin/bash

# remove old file and create symbolic link of UTC timezone to /etc/localtime
ln -sf /usr/share/zoneinfo/UTC /etc/localtime
# update the package list of all installed packages
apt-get update
# install updates for all installed packages
apt-get upgrade
# install unattended-upgrades to automatically install updated packages
apt-get install -y unattended-upgrades
# install other necessary programs
apt-get install -y postgresql python-psycopg2
apt-get install -y python-flask python-sqlalchemy
apt-get install -y python-pip
apt-get install -y libapache2-mod-wsgi python-dev
apt-get install -y apache2
apt-get install -y libmagickwand-dev
pip install werkzeug==0.8.3
pip install Flask-Login==0.1.3
pip install SQLAlchemy-ImageAttach
pip install oauth2client
pip install requests
pip install httplib2
pip install redis
pip install passlib
pip install flask-httpauth
pip install flask-seasurf

# install system monitoring tool
# curl -L http://bit.ly/glances | /bin/bash # <--do i actually need this
pip install glances
# install fail2ban to monitor malicious attack
apt-get install -y fail2ban
# install sendmail to send e-mail with fail2ban status
apt-get install -y sendmail
# allow the server to automatically set up our firewall rules at boot
# apt-get install -y iptables-persistent

# create a copy of jail.conf for fail2ban
cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# obtain user input for fail2ban destemail
echo "Type in the recipient e-mail address for fail2ban messages:"
read varname
word="destemail = root@localhost"
rep="destemail = "
rep+=$varname
sed -i "s/${word}/${rep}/" /etc/fail2ban/jail.local

# obtain user input for fail2ban sendername
echo "Type in the sender e-mail address for fail2ban messages:"
read varname
word="sendername = Fail2Ban"
rep="sendername = "
rep+=$varname
sed -i "s/${word}/${rep}/" /etc/fail2ban/jail.local

# change default action to include e-mail (+ relevant log) on top of ban
sed -i "s/(action_)/(action_mwl)/" /etc/fail2ban/jail.local
# change SSH port to monitor to 2200, tell fail2ban to look for ufw-ssh for actions
sed -i"" '/\[ssh\]/,/\[dropbear\]/ s/port     = ssh/port     = 2200/' /etc/fail2ban/jail.local
sed -i '/port     = 2200/a banaction = ufw-ssh' /etc/fail2ban/jail.local
# enable apache JAIL, tell fail2ban to look for ufw-apache for actions
sed -i"" '/\[apache\]/,/\[apache-multiport\]/ s/enabled  = false/enabled  = true/' /etc/fail2ban/jail.local
sed -i '/\[apache\]/a \banaction = ufw-apache' /etc/fail2ban/jail.local

# create ufw-ssh.conf for fail2ban to use on SSH-related traffic
echo -e "[Definition]\nactionstart = \nactionstop = \nactioncheck = \nactionban = ufw insert 1 deny from <ip> to any app OpenSSH\nactionunban = ufw delete deny from <ip> to any app OpenSSH" >> /etc/fail2ban/action.d/ufw-ssh.conf
# create ufw-apache.conf for fail2ban to use on SSH-related traffic
echo -e '[Definition]\nactionstart = \nactionstop = \nactioncheck = \nactionban = ufw insert 2 deny from <ip> to any app "Apache Full"\nactionunban = ufw delete deny from <ip> to any app "Apache Full"' >> /etc/fail2ban/action.d/ufw-apache.conf

# remove and create new file "10periodic" to configure auto-install interval
rm /etc/apt/apt.conf.d/10periodic
echo -e 'APT::Periodic::Update-Package-Lists "1";\nAPT::Periodic::Download-Upgradeable-Packages "1";\nAPT::Periodic::AutocleanInterval "7";\nAPT::Periodic::Unattended-Upgrade "1";' >> /etc/apt/apt.conf.d/10periodic
# add a new user named grader, input password when prompted
adduser --gecos "Udacity_Grader" grader
# change grader's group from "group" to "sudo"
usermod -a -G sudo grader
# create a grader profile under sudoers.d to remove password prompt when using
# sudo command
echo "grader ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/grader


# create a copy of sshd_config
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup
# check sshd_config to make sure PasswordAuthentication has been set to "yes"
if grep -q "PasswordAuthentication no" /etc/ssh/sshd_config; then
    word="PasswordAuthentication no"
    rep="PasswordAuthentication yes"
    sed -i "s/${word}/${rep}/" /etc/ssh/sshd_config
else
    echo "PasswordAuthentication has already been set to yes"
fi
# change default ssh port from 22 to 2200
sed -i -e 's/22/2200/g' /etc/ssh/sshd_config
# disable remote login for root
word="PermitRootLogin without-password"
rep="PermitRootLogin no"
sed -i "s/${word}/${rep}/" /etc/ssh/sshd_config
# restart ssh
service ssh restart


# configure firewall to deny all incoming traffic by default
ufw default deny incoming
# configure firewall to allow all outgoing traffic by default
ufw default allow outgoing
# configure firewall to only allow traffic in ssh (2200), HTTP, and NTP port
ufw allow 2200
ufw allow www
ufw allow ntp
# enable firewall
ufw enable
# copy the next script to grader's directory
cp FlaskApp/scripts/script2.sh /home/grader/script2.sh
# logout
exit

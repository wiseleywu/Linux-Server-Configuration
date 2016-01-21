# Linux Server Configuration

## Information for Udacity grader
- IP address: `ip-address`
- SSH port: `2200`
- Web application URL: `http://ip-address`

## Requirements
- git
- unattended-upgrades
- postgresql
- python-dev
- python-psycopg2
- python-flask
- python-sqlalchemy
- python-pip
- libapache2-mod-wsgi
- apache2
- libmagickwand-dev
- glances
- fail2ban
- sendmail

Other web application specific requirement could be referred here https://github.com/wiseleywu/Biologics-Catalog/blob/master/README.md

## Instructions
- Obtain RSA key of the server, save it to ~/.ssh (if applicable)
- Use `chmod 600 ~/.ssh/udacity_key.rsa` to configure file permission locally
- Use `ssh -i ~/.ssh/udacity_key.rsa root@ip-address` to login to remote server as root using RSA key
- git clone the current repository to a folder called 'FlaskApp' in current directory `https://github.com/wiseleywu/Linux-Server-Configuration.git FlaskApp`
- Run `bash FlaskApp/scripts/script1.sh`
  - At this point, you will get several prompt from the console for update/install, answer 'yes' to all questions
  - You will then get a prompt to setup recipient/sender e-mail address for fail2ban. Input your desired e-mail addresses
  - Finally, you will get a prompt to create password for new user 'grader'. Input a password of your choosing
  - After the script has completed running, you will be back to your local environment
- Re-login back to the server using `ssh -p 2200 grader@ip-address`
- Run `bash script2.sh` (this script has been copied to grader's home directory in previous script)
  - Toward the end, you will get a prompt to create a public key in your local environment. Open a new console and type `ssh-keygen`
  - Choose the current udacity_key.rsa, or create a new key. Choose a passphrase of your choosing
  - Copy the public key within udacity_key.rsa.pub and paste it at the server's prompt
  - After the script completed, exit back to the local environment (log out)
- Re-login back to the server using `ssh -p 2200 -i ~/.ssh/udacity_key.rsa grader@ip-address` to confirm the new secured key works
- At this point, the web app should be up and running and grader is the only user that could SSH into the remote server with the newly generated udacity_key.rsa

## Software Configuration
### System
- Change timezone to UTC
- Configure unattended-upgrades to update the package list, downloads, and installs available upgrades every day. The local download archive is cleaned every week.
- Add new user `grader` with root privilege and remove password prompt when using sudo command
### Security
- Disable password authentication in `sshd_config`
- Disable remote login for root
- Change default SSH port from 22 to 2200
- Configure firewall to deny all incoming traffic by default
- Configure firewall to allow all outgoing traffic by default
- Configure firewall to allow SSH, HTTP, and NTP traffic
### Monitoring

## Third-party Resources
- https://blog.vigilcode.com/2011/05/ufw-with-fail2ban-quick-secure-setup-part-ii/

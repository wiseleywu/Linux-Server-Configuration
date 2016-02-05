# Linux Server Configuration
This project involved deploying a previously developed web application to Amazon's Elastic Compute Cloud. The web app will be hosted in a Ubuntu virtual machine, and this repo included all the necessary information and scripts to deploy a functional version of [Biologics-Catalog][1] to the public web with Oauth login and CRUD operations while being protected against a variety of common attacks.

## Web App Location
- Currently, the web app could be reached by going to `ec2-54-149-58-225.us-west-2.compute.amazonaws.com`. I have also registered a domain name at `biologics-catalog.com`, but I had a brain fart and registered it at Google Domains instead of Amazon Route 53 - so I can't properly route traffic from the new domain name to my current web app location until I can transfer the domain name to Amazon (in 60 days). I have forwarded the domain name to the Amazon EC2 instance for now.

## ~~Information for Udacity grader~~
- ~~IP address: `52.27.179.148`~~
- ~~SSH port: `2200`~~
- ~~Web application URL: `http://ec2-52-27-179-148.us-west-2.compute.amazonaws.com/`~~

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

Other application-specific requirement could be referred [here][2].

## Instructions
- Obtain RSA key of the server, save it to ~/.ssh (if applicable)
- Use `chmod 600 ~/.ssh/udacity_key.rsa` to configure file permission locally
- Use `ssh -i ~/.ssh/udacity_key.rsa root@ip-address` to login to remote server as root using the RSA key
- Git clone this repo to a folder called 'FlaskApp' in the server's current directory `git clone https://github.com/wiseleywu/Linux-Server-Configuration.git FlaskApp`
- Run `bash FlaskApp/scripts/script1.sh`
  - At this point, you will get several prompt from the console for update/install, answer 'yes' to all questions
  - You will then get a prompt to setup recipient/sender e-mail address for fail2ban. Input your desired e-mail addresses
  - Finally, you will get a prompt to create password for new user 'grader'. Input a password of your choosing
  - Logout after the script has completed running
- Re-login back to the server using `ssh -p 2200 grader@ip-address`
- Run `bash script2.sh` (this script has been copied to grader's home directory in previous script)
  - You will get a prompt to create a public key in your local environment. Open a new console and type `ssh-keygen`
  - Choose the current udacity_key.rsa, or create a new key. Choose a passphrase of your choosing
  - Copy the public key within udacity_key.rsa.pub and paste it at the server's prompt
  - Logout after the script has completed running
- Re-login back to the server using `ssh -p 2200 -i ~/.ssh/udacity_key.rsa grader@ip-address` to confirm the new secured key works
- At this point, the web app should be up and running and grader is the only user that could SSH into the remote server with the newly generated udacity_key.rsa

## Software Configuration

### System
- Change time zone to UTC
- Configure unattended-upgrades to update the package list, downloads, and installs available upgrades every day. The local download archive is cleaned every week.
- Add new user `grader` with root privilege and remove password prompt when using sudo command

### Firewall
- Configure firewall to deny all incoming traffic by default
- Configure firewall to allow all outgoing traffic by default
- Configure firewall to allow SSH, HTTP, and NTP traffic

### SSH
- Disable password authentication in `sshd_config`
- Disable remote login for root
- Change default SSH port from 22 to 2200
- Enforced key-based authentication with public key located in `/home/grader/.ssh/authorized_keys`

### Fail2Ban
- Change default action to e-mail notification with relevant log
- Change SSH monitoring to port 2200, action defined in `ufw-ssh`
- Enable apache JAIL, action defined in `ufw-apache`
- Change recipient and sender e-mail addresses based on user's input

### PostgreSQL
- Create database with account `postgres`
- Create user `catalog` with no outstanding permissions
- Do not allow remote connections (default)

### System Monitoring
- Install **glances**

## Third-party Resources
- https://help.ubuntu.com/community/PostgreSQL
- https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps
- https://blog.vigilcode.com/2011/05/ufw-with-fail2ban-quick-secure-setup-part-ii/

[1]: https://github.com/wiseleywu/Biologics-Catalog
[2]: https://github.com/wiseleywu/Biologics-Catalog/blob/master/README.md

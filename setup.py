#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
DHT22
sudo apt-get update
sudo apt-get install build-essential python-dev python-openssl git

git clone https://github.com/adafruit/Adafruit_Python_DHT.git && cd Adafruit_Python_DHT
sudo python setup.py install


DISPLAY


FINGERPRINT
wget -O - http://apt.pm-codeworks.de/pm-codeworks.de.gpg | apt-key add -
wget http://apt.pm-codeworks.de/pm-codeworks.list -P /etc/apt/sources.list.d/

apt-get update
apt-get install python-fingerprint --yes


Dynamic DNS client with NoIP.com
(https://www.noip.com/support/knowledgebase/installing-the-linux-dynamic-update-client-on-ubuntu/)

cd /usr/local/src/
wget http://www.no-ip.com/client/linux/noip-duc-linux.tar.gz
tar xf noip-duc-linux.tar.gz
cd noip-2.1.9-1/
make install

Autostart noip2 on boot

sudo nano /etc/systemd/system/noip2.service

script from https://gist.github.com/NathanGiesbrecht/da6560f21e55178bcea7fdd9ca2e39b5
####################################################
[Unit]
Description=No-ip.com dynamic IP address updater
After=network.target
After=syslog.target

[Install]
WantedBy=multi-user.target
Alias=noip.service

[Service]
# Start main service
ExecStart=/usr/local/bin/noip2
Restart=always
Type=forking
####################################################

sudo systemctl enable noip2
sudo systemctl start noip2


APACHE

sudo a2enmod cgi

/etc/apache2/sites-available/mypidrei.com.conf
####################################
<VirtualHost 127.0.0.2:80>

        <Directory /var/www/my_pi_drei/www/>
                Options +ExecCGI
                DirectoryIndex index.py
        </Directory>
        AddHandler cgi-script .py

        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/my_pi_drei/www/
        ServerName www.mypidrei.com
        ServerAlias mypidrei.com

</VirtualHost>
####################################
sudo a2ensite mypidrei.com.conf
sudo service apache2 restart


add in /etc/hosts
####################################
127.0.0.2       mypidrei.com
####################################


CONFIG
copy config_example and rename the copy to config.py
    - replace all placeholder in the file


"""
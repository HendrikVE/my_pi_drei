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


"""
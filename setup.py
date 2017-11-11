#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
DHT22
sudo apt-get update
sudo apt-get install build-essential python-dev python-openssl git

git clone https://github.com/adafruit/Adafruit_Python_DHT.git && cd Adafruit_Python_DHT
sudo python setup.py install


DISPLAY


APACHE

sudo a2enmod userdir

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
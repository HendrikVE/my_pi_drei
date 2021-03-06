#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2017 Hendrik van Essen
 *
 * This file is subject to the terms and conditions of the MIT License
 * See the file LICENSE in the top level directory for more details.
"""

"""setup script"""

"""
BASIC SYSTEM PRIVATE COMPUTER
sudo apt-get install python3-pip
sudo apt-get install python-pip
sudo apt-get install python-zmq

ARDUINO
sudo apt-get install minicom python3-serial

Kookye FM-70
http://kookye.com/2016/07/24/use-arduino-drive-fingerprint-sensor/
unzip and copy to  <arduinosketchfolder>/libraries/

cd <arduinosketchfolder>/libraries/ 
git clone https://github.com/adafruit/DHT-sensor-library
git clone https://github.com/adafruit/Adafruit_Sensor

install ArduinoJson within Arduino IDE from Library Manager (Sketch -> Include Library -> Manage Libraries)
"""


"""
BASIC SYSTEM RASPBERRY PI
enable SSH
change lines in /etc/ssh/sshd_config
####################################################
PermitRootLogin no
PasswordAuthentication no
####################################################

banning ips trying to login with wrong credentials
sudo apt-get install fail2ban

DISPLAY
https://learn.adafruit.com/adafruit-2-2-pitft-hat-320-240-primary-display-for-raspberry-pi/detailed-installation

SOUND
sudo apt-get install python3-pygame
sudo apt-get install python-pygame


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

/etc/apache2/sites-available/mypidrei.ddns.net.conf
####################################
<VirtualHost *:80>

        <Directory /var/www/my_pi_drei/webserver/www/>
                Options +ExecCGI
                DirectoryIndex index.py
        </Directory>
        AddHandler cgi-script .py

        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/my_pi_drei/webserver/www/
        ServerName mypidrei.ddns.net

</VirtualHost>
####################################
sudo a2ensite mypidrei.ddns.net.conf

disable indexing in /etc/apache2/apache2.conf
####################################
<Directory /var/www/>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
</Directory>
####################################
to
####################################
<Directory /var/www/>
        Options -Indexes +FollowSymLinks
        AllowOverride None
        Require all granted
</Directory>
####################################

sudo service apache2 restart


add in /etc/hosts
####################################
127.0.0.2       mypidrei.com
####################################

You will need to forward port 80 (Webserver) and 22 (SSH, optional) in your router settings


SSL For Apache using Certbot
You will need to forward port 443 (HTTPS) in your router settings

sudo apt-get install python-certbot-apache
sudo certbot --apache -d mypidrei.ddns.net (needs user input. Recommended option "Secure"(redirection of http to https))


CONFIG
copy from webserver/config config_example and rename the copy to config.py
    -> replace all placeholder in the file


"""
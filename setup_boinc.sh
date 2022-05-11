#!/bin/bash

################# Setup Boinc server (Ubuntu 20.04)

# 1) Install deps
sudo add-apt-repository 'deb http://archive.ubuntu.com/ubuntu bionic main'
sudo add-apt-repository ppa:ondrej/php-5
sudo apt update
sudo apt-get install git build-essential apache2 libapache2-mod-php5.6 php5.6 \
    mariadb-server php5.6-gd php5.6-cli php5.6-mysql php5.6-xml php5.6-curl python-mysqldb \
    libtool automake autoconf pkg-config libmysql++-dev libssl-dev \
    libcurl4-openssl-dev


# 2) Add user boincadm for a separate project
sudo adduser boincadm
sudo usermod -a -G boincadm www-data
sudo chmod -R 711 /home/boincadm

# 3) Configure MySQL server
sudo mysql -h localhost -u root -p
CREATE USER 'boincadm'@'localhost' IDENTIFIED BY '';
GRANT ALL ON *.* TO 'boincadm'@'localhost';
FLUSH PRIVILEGES;
sudo systemctl enable mariadb.service

# 4) Configure Apache2 TODO: configure later
sudo systemctl enable apache2
sudo a2enmod cgi
sudo systemctl restart apache2
# echo "DefaultType application/octet-stream" >> /etc/apache2/apache2.conf # FOR PROBLEMS WITH SIGNATURES
# echo "LimitXMLRequestBody 134217728" >> /etc/apache2/apache2.conf # FOR LARGE FILES

# 5) Build from sources
su boincadm
cd ~
git clone https://github.com/BOINC/boinc.git boinc-src
cd ~/boinc-src
./_autosetup
./configure --disable-client --disable-manager \
--with-jpeg-dir --with-png-dir --with-mysqli --with-curl --with-gd --with-zlib
make

# 6) Make and configure a project
cd ~/boinc-src/tools/
./make_project  --delete_prev_inst --drop_db_first --url_base http://<SERVER_EXTERNAL_IP> \
--db_passwd <DB_PASSWORD> --test_app cplan

cd ~/projects/cplan/
chmod 02770 upload
chmod 02770 html/cache
chmod 02770 html/inc
chmod 02770 html/languages
chmod 02770 html/languages/compiled
chmod 02770 html/user_profile

sudo ln -s /home/boincadm/projects/cplan/cplan.httpd.conf /etc/apache2/sites-enabled
# generate a username/password file for your administrative web interface using http://178.154.210.253/cplan_ops
htpasswd -cb ~/projects/cplan/html/ops/.htpasswd boincadm <PASSWORD>

# run crontab -e, and add an entry to run the project's cron script
crontab -e
0,5,10,15,20,25,30,35,40,45,50,55 * * * * /home/boincadm/cplan/bin/start --cron
/home/boincadm/projects/cplan/bin/start --cron

cd ~/boinc-src/tools/
./check_project -p ~/projects/cplan

# 7) Run project
cd ~/projects/cplan/bin
./xadd
./update_versions
./start

sudo apt-get install -y mysql
sudo apt-get install -y memcached 
sudo apt-get install -y python-mysqldb
sudo apt-get install -y python-pip
sudo apt-get install -y libxml2-dev libxslt1-dev
sudo pip-2.7 install -y Scrapy
sudo apt-get install -y nginx nmap
sudo pip install python-memcached
sudo pip install tornado
sudo apt-get -y update && sudo apt-get -y upgrade
sudo pip install supervisor
#sudo pip install torndb

memcached -d -m 1024 -p 11211 -l 192.168.0.110

sudo mkdir -p /srv/www/kinomania.gr
cd /srv/www/kinomania.gr

cd
sudo cp -R * /srv/www/kinomania.gr/

sudo nginx -s stop

sudo rm /etc/nginx/nginx.conf
sudo ln -s /srv/www/kinomania.gr/conf/nginx.conf /etc/nginx/nginx.conf nginx.conf
sudo ln -s /srv/www/kinomania.gr/conf/supervisord.conf ~/.

sudo adduser --system --no-create-home --disabled-login --disabled-password --group nginx

#alias scp2ec='scp -i ~/Downloads/MicroMania.pem -r * ubuntu@54.246.81.102:/home/ubuntu'
#alias ssh2ec='ssh -i ~/Downloads/MicroMania.pem ubuntu@54.246.81.102'
#mysqldump -u root -p Kino > kinodb.out
#mysql -u root -p Kino < kino.backup
#supervisorctl stop all
#sudo crontab -e 
## * * * * * /srv/www/kinomania.gr/crawler.py

sudo mkdir /var/log/supervisord
sudo supervisord -c /srv/www/kinomania.gr/conf/supervisord.conf
sudo /etc/init.d/nginx start

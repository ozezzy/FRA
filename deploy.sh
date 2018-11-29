#!/bin/sh
WWWPATH=/var/www
SITE_CONF_PATH=/etc/apache2/sites-available/FRA.conf

#content of WSGI file
WSGI_FILE=$(cat <<-EndOfMessage
import os,sys

sys.path.insert(0,"/var/www/FRA/")

from FRA import app as application
if __name__ == "__main__":
    application.secret_key = os.urandom(12)
EndOfMessage
)

#content of apache site-available/FRA
SITE_CONF=$(cat <<-EndOfMessage
<VirtualHost *:80>
        WSGIDaemonProcess FRA python-home=/var/www/FRA/venv/
        WSGIProcessGroup FRA
        WSGIScriptAlias / /var/www/FRA/app.wsgi
        <Directory /var/www/FRA/FRA/>
            Order allow,deny
            Allow from all
        </Directory>
        Alias /static /var/www/FRA/FRA/static
        <Directory /var/www/FRA/FRA/static/>
            Order allow,deny
            Allow from all
        </Directory>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        LogLevel warn
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
EndOfMessage
)

# script that runs as root
if [ ! "`whoami`" = "root" ]
then
    echo "\nPlease run script as root."
    exit 1
fi

echo "starting deployment ..."
echo "checking python ..."

if [ !`which python3` ]; then
    echo "...installing python ..."
    { 

        sudo apt-get update -y
        sudo apt-get install python3 -y


    } || {
        echo "python3.6 installation failed pease install manually"
        exit 1
    }
else
        echo "python3.6 found."
fi


if [ !`which pip` ]; then
    {
        echo "installing pip ..."
        sudo apt install python-pip -y
    }||{
        echo "pip installation failed "
        exit 1
    }
else
    echo "pip installation found"
fi

if [ !`which virtualenv` ]; then
    echo "installing virtualenv ..."
    { 
    	sudo apt install virtualenv -y
    } || {
        echo "virtual env installation failed"
        exit 1
    }
else
        echo "virtualenv found"
fi

#create /var/www
sudo mkdir -p $WWWPATH

if [ ! -d "./FRA" ]; then
   echo "main project file FRA missing"
   exit 1
fi

if [ -d "/var/www/FRA" ]; then
    sudo rm -r /var/www/FRA
fi

sudo cp -r ../FRA $WWWPATH"/FRA"

virtualenv -p python3 $WWWPATH"/FRA/venv"
source $WWWPATH"/FRA/venv/bin/activate"
{
    echo "installing requirements ..."
  sudo  $WWWPATH"/FRA/venv/bin/pip" install -r $WWWPATH"/FRA/requirements.txt" 
}||{
    echo "wrong package in requirements.tet"
    exit 0
}
#run seed user
$WWWPATH"/FRA/venv/bin/python" $WWWPATH"/FRA/seed.py"
sudo echo  "$WSGI_FILE" > $WWWPATH"/FRA/app.wsgi"

##apache2
if [ !`which apache2` ]; then
    {
        echo "installing apache2 ..."
        sudo apt install apache2 -y
    }||{
        echo "apache installation failed"
    }
fi

 #insatll python3 wsgi module
{
   sudo apt-get install libapache2-mod-wsgi-py3 -y
}||{
    echo "python3 wsgi installation failed"
    exit 1
}

#enable wsgi module
sudo a2enmod wsgi

sudo echo  "$SITE_CONF" > $SITE_CONF_PATH
#desable deafult 
sudo a2dissite 000-default.conf

#enable siteconf
sudo a2ensite FRA.conf

#reload apache
sudo systemctl reload apache2

#restart apache
sudo service apache2 restart 

echo "Deployment COMPLETE"
echo "    thank you"
exit 0

#!/bin/sh
WWWPATH=/var/www/FRA
SITE_CONF_PATH=/etc/apache2/sites-available/FRA.conf

WSGI_FILE=$(cat <<-EndOfMessage
import os,sys

sys.path.insert(0,"/var/www/FRA/")

from FRA import app as application
if __name__ == "__main__":
    application.secret_key = os.urandom(12)
EndOfMessage
)

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
echo "...checking python"

python=`which python3.6`
if [ "$python" == "" ]; then
    echo "...installing python ..."
    { 

        sudo apt-get update
        sudo apt-get install python3.6


    } || {
        echo "python3.6 installation failed pease install manually"
        exit 1
    }
else
        echo "python3.6 found."
fi

pip=`which pip`
if [ "$pip" == "" ]; then
    {
        echo "installing pip ..."
    sudo apt install python-pip
    }||{
    echo "pip installation failed "
    exit 1
    }
else
    echo "pip installation found"
fi

venv=`which virtualenv`
if [ "$venv" == "" ]; then
    echo "installing virtualenv ..."
    { 
    pip install virtualenv
    } || {
        echo "virtual env installation failed"
        exit 1
    }
else
        echo "virtualenv found"
fi

#create /var/www if not exixting
sudo mkdir -p $WWWPATH

if [ ! -d "./FRA" ]; then
   echo "main project file FRA missing"
   exit 1
fi
sudo cp -r ./FRA $WWWPATH
virtualenv -p python3 $WWWPATH"venv"
source $WWWPATH"venv/bin/activate"
{
    echo "installing requirements ..."
    pip install -r requirements.txt 
}||{
    echo "wrong package in requirements.tex"
    exit 0
}
echo "$WWWPATH"
sudo echo  "$WSGI_FILE" > $WWWPATH"/app.wsgi"

##apache2
apache=`which apache2`
if [ "$apache" == "" ]; then
    {
        echo "installing apache2 ..."
        sudo apt install apache2
    }||{
        echo "apache installation failed"
    }
fi

{apt-get install libapache2-mod-wsgi}||{echo "python3 wsgi installation failed"}
#insatll python3 wsgi module
sudo apt-get install libapache2-mod-wsgi-py3
#enable wsgi module
sudo a2enmod 

sudo echo  "$SITE_CONF" > $SITE_CONF_PATH
#enable siteconf
sudo a2ensite FRA.conf

#reload apache
sudo systemctl reload apache2

#restart apache
sudo service apache2 restart 

echo "$venv"
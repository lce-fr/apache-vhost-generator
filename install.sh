installPath=$(pwd)
cd /usr/local/bin
echo $installPath/new-apache-vhost.py
ln -s "$installPath/new-apache-vhost.py" new-apache-vhost.py

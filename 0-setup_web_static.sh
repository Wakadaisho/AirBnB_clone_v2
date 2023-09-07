#!/usr/bin/env bash
# Setup a server for web servicing

CONFIG='\\tlocation /hbnb_static/ \{\n\t\talias /data/web_static/current/;\n\t\}\n'
FILE='/etc/nginx/sites-available/default'

sudo apt-get update
sudo apt-get -y install --no-upgrade nginx

sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

echo 'Hello NGINX' | sudo tee /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test /data/web_static/current

sudo chown -R "ubuntu:ubuntu" /data

if [ "$(grep -c 'location /hbnb_static' $FILE)" -eq 0 ]; then 
	sudo sed -i.bak "/^server/a $CONFIG" "$FILE"
fi

sudo service nginx restart

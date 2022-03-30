#!/bin/bash
# Author: C. J. Burton

pip3 install google-api-python-client google-auth-oauthlib google-auth-httplib2 pytz tzlocal

mkdir ~/.local/share
mkdir ~/.local/share/calcli
cp src/calcli.py ~/.local/share/calcli/calcli.py
cp src/tui.py ~/.local/share/calcli/tui.py
cp src/tui_google.py ~/.local/share/calcli/tui_google.py
cp src/credentials.json ~/.local/share/calcli/credentials.json
cp src/calcli ~/.local/bin/calcli

chmod +x ~/.local/bin/calcli
sed -i -e 's/\r$//' ~/.local/bin/calcli

echo "Installation complete! "

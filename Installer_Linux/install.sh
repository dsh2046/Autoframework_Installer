#!/bin/bash
set -e


sudo cp chromedriver /usr/bin
echo "Installing Pybot"
cd Robot-Framework/robotframework-3.0.1
sudo python setup.py install
pybot --version | grep "Robot Framework"
echo "Robot Framework installed"   
echo "========================================"
echo "========================================"

cd ..
sudo apt-get install python-wxgtk2.8  
dpkg --list | grep "python-wxgtk2.8"
echo "wxgtk2.8 installed"
echo "========================================"
echo "========================================"

cd robotframework-ride-1.5.2.1
sudo python setup.py install
find ~/ -name ride.py | grep "build" 
echo "RIDE installed"
echo "========================================"
echo "========================================"


cd ../robotframework-selenium2library-1.8.0
sudo python setup.py install
#robotframework-selenium2library

python <<EOF
import Selenium2Library
print Selenium2Library
EOF

cd ../PyMySQL-0.7.9
sudo python setup.py install
python <<EOF
import pymysql
print pymysql
EOF

cd ../robotframework-databaselibrary-0.6
sudo python setup.py install

cd ../../Excel/natsort-3.3.0
sudo python setup.py install
cd ../NaviNet-robotframework-excellibrary-8744913
sudo python setup.py install
cd ../xlutils-1.7.1
sudo python setup.py install
cd ../xlrd-1.0.0
sudo python setup.py install
cd ../xlwt-1.2.0
sudo python setup.py install

python <<EOF
import ExcelLibrary
print ExcelLibrary
EOF
echo 'Installed Successfully!'

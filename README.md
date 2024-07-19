Setting Up RS485 Wind (speed/direction)

cd /tmp
wget https://project-downloads.drogon.net/wiringpi-latest.deb   //Download wiringpi library
sudo dpkg -i wiringpi-latest.deb  //Install wiringpi library
cd .....                                                     //Enter the content you want to save file in
git clone https://github.com/DFRobotdl/RS485_Wind_Speed_Transmitter.git     //Download program in github
cd RS485_Wind_Speed_Transmitter/

Error Correction
  If Errors were encountered while processing:
   wiringpi:armhf
sudo apt --fix-broken install


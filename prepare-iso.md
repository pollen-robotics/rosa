# Rosa

This repository contains the RPI code for the robot.

You will also find a minimal Python API to control the robot with a follow line example.

## Installation on RPI

1. Burn a raspbian lite IMG
2. Setup ssh and WiFi (can be done directly on the boot partition)
3. Setup hostname to "rosa"
4. Enable camera (via raspi-config)
5. Update distrib ```sudo apt update```
6. Add v4l2 driver for the cam ```echo "bcm2835-v4l2" | sudo tee /etc/modules-load.d/bcm2835-v4l2.conf```
7. Install numpy
```
sudo apt install libatlas3-base
pip3 install numpy -i https://www.piwheels.org/simple
```
8. Install opencv for python 3
```
wget https://github.com/opencv/opencv/archive/3.4.3.tar.gz
tar xvfz 3.4.3.tar.gz
cd opencv-3.4.3
sudo apt install -y build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev libatlas-base-dev gfortran python3-dev
mkdir build
cd build
cmake -D BUILD_EXAMPLES=OFF -D BUILD_DOCS=OFF -D BUILD_PERF_TESTS=OFF -D BUILD_TESTS=OFF ..
Edit swap size in /etc/dphys-swapfile (CONF_SWAPSIZE=1024) & sudo /etc/init.d/dphys-swapfile restart
make -j4
Restore swap size in /etc/dphys-swapfile (CONF_SWAPSIZE=100) & sudo /etc/init.d/dphys-swapfile restart
sudo make install
sudo ldconfig
```
10. Install python dependencies
```
sudo apt install git
pip3 install git+https://github.com/dpallot/simple-websocket-server.git
pip3 install ipython Pillow websocket-client
```
11. Download and install scripts
```
wget https://github.com/pollen-robotics/rosa/archive/rpi.zip
unzip rpi.zip
cd rosa-rpi/rpi
```
12. Launch video stream as service (run from rpi folder)
```
sudo tee /etc/systemd/system/videostream.service > /dev/null <<EOF
[Unit]
Description=Video Stream to WS
Wants=network-online.target
After=network.target network-online.target
[Service]
PIDFile=/var/run/videostream.pid
Environment="PATH=$PATH"
ExecStart=/usr/bin/python3 "$PWD/streamjpeg.py"
User=pi
Group=pi
Type=simple
[Install]
WantedBy=multi-user.target
EOF
sudo systemctl enable videostream.service
```
13. **TODO** add remote motor controller server as service
14. Reboot

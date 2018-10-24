# Rosa

This repository contains the RPI code for the robot.

You will also find a minimal Python API to control the robot with a follow line example.

## Installation on RPI

1. Burn a raspian lite IMG
2. Setup ssh and WiFi (can be done directly on the boot partition)
3. Setup hostname to "rosa" (used by Scratch and video stream)
4. Enable camera (via raspi-config)
5. Add v4l2 driver for the cam ```echo "bcm2835-v4l2" | sudo tee /etc/modules-load.d/bcm2835-v4l2.conf```
6. Install pip for python3
```
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
```
7. Install opencv for python 3
```
wget https://github.com/opencv/opencv/archive/3.4.3.tar.gz
tar xvfz 3.4.3.tar.gz
cd opencv-3.4.3
sudo apt install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev libatlas-base-dev gfortran python3-dev python3-numpy
mkdir build
cd build
cmake ..
make -j4
sudo make install
sudo ldconfig
```
8. Install GPIO support for python
```
sudo apt install python3-gpiozero
```
9. Install python dependencies
```
sudo pip install websockets ipython
```
10. Download and install scripts
```
wget https://github.com/pollen-robotics/rosa/archive/rpi.zip
unzip rpi.zip
cd rosa-rpi/rpi
```
11. Launch video stream as service (run from rpi folder)
```
sudo tee /etc/systemd/system/videostream.service > /dev/null <<EOF
[Unit]
Description=Video Stream to WS
Wants=network-online.target
After=network.target network-online.target
[Service]
PIDFile=/var/run/videostream.pid
Environment="PATH=$PATH"
ExecStart=/usr/bin/python3 "$PWD/streamcam.py"
User=pi
Group=pi
Type=simple
[Install]
WantedBy=multi-user.target
EOF
sudo systemctl enable videostream.service
```
12. Launch rosa to scratch as service (run from rpi folder)
```
sudo tee /etc/systemd/system/rosa2scratch.service > /dev/null <<EOF
[Unit]
Description=Rosa 2 Scratch ext. manager
Wants=network-online.target
After=network.target network-online.target
[Service]
PIDFile=/var/run/rosa2scratch.pid
Environment="PATH=$PATH"
ExecStart=/usr/bin/python3 "$PWD/rosa.py"
User=pi
Group=pi
Type=simple
[Install]
WantedBy=multi-user.target
EOF
sudo systemctl enable rosa2scratch.service
```
13. Reboot

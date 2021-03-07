#!/bin/sh

set -e
sudo apt update
sudo apt install -y python-pip python3-pip python3-pexpect unzip busybox-static fakeroot kpartx snmp uml-utilities util-linux vlan qemu-system-arm qemu-system-mips qemu-system-x86 qemu-utils

echo "Installing binwalk"
cd binwalk
sudo ./deps.sh
sudo python3 ./setup.py install
sudo -H pip3 install git+https://github.com/ahupp/python-magic
sudo -H pip install git+https://github.com/sviehb/jefferson
cd ..



echo "Setting up firmware analysis toolkit"
chmod +x emu.py
chmod +x reset.py

#Set firmadyne_path in fat.config
sed -i "/firmadyne_path=/c\firmadyne_path=$firmadyne_dir" emu.config

# Comment out psql -d firmware ... in getArch.sh
sed -i 's/psql/#psql/' ./scripts/getArch.sh

#Setting up the toolchains
sudo mkdir -p /opt/cross
sudo cp toolchains/* /opt/cross
cd /opt/cross
sudo tar -xf arm-linux-musleabi.tar.xz 
sudo tar -xf mipseb-linux-musl.tar.xz 
sudo tar -xf mipsel-linux-musl.tar.xz 
cd -

mkdir -p ./source/Kernel-mips/build/mipseb
mkdir -p ./source/Kernel-mips/build/mipsel
mkdir -p ./source/Kernel-armel/build/armel

cp ./source/Kernel-mips/config.mipseb ./source/Kernel-mips/build/mipseb/.config
cp ./source/Kernel-mips/config.mipsel ./source/Kernel-mips//build/mipsel/.config
cp ./source/Kernel-armel/config.armel ./source/Kernel-armel/build/armel/.config

# Adding toolchains to PATH
echo "PATH=$PATH:/opt/cross/mipsel-linux-musl/bin:/opt/cross/mipseb-linux-musl/bin:/opt/cross/arm-linux-musleabi/bin" >> ~/.profile
source ~/.profile

# Make the kernels
cd ./source/Kernel-mips/
make ARCH=mips CROSS_COMPILE=mipseb-linux-musl- O=./build/mipseb -j8
make ARCH=mips CROSS_COMPILE=mipsel-linux-musl- O=./build/mipsel -j8
cd - && cd ./source/Kernel-armel/
make ARCH=arm CROSS_COMPILE=arm-linux-musleabi- O=./build/armel zImage -j8

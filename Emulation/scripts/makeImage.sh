#!/bin/bash

set -e
set -u
source scripts/env.config


IID=${1}
ARCH=${2}


echo "----Running----"
WORK_DIR="${WORK_DIR}/${IID}"
IMAGE="${WORK_DIR}/image.raw"
IMAGE_DIR="${WORK_DIR}/image"

LIBNVRAM="${LIB_DIR}/libnvram.so.${ARCH}"
CONSOLE="${LIB_DIR}/console.${ARCH}"

echo "----Copying Filesystem Tarball----"
mkdir -p "${WORK_DIR}"
chmod a+rwx "${WORK_DIR}"
chown -R "${USER}" "${WORK_DIR}"
chgrp -R "${USER}" "${WORK_DIR}"

if [ ! -e "${WORK_DIR}/${IID}.tar.gz" ]; then
    if [ ! -e "${TARBALL_DIR}/${IID}.tar.gz" ]; then
        echo "Error: Cannot find tarball of root filesystem for ${IID}!"
        exit 1
    else
        cp "${TARBALL_DIR}/${IID}.tar.gz" "${WORK_DIR}/${IID}.tar.gz"
    fi
fi

echo "----Creating QEMU Image----"
qemu-img create -f raw "${IMAGE}" 1G
chmod a+rw "${IMAGE}"

echo "----Creating Partition Table----"
echo -e "o\nn\np\n1\n\n\nw" | /sbin/fdisk "${IMAGE}"

echo "----Mounting QEMU Image----"
DEVICE=`add_partition ${IMAGE}`
echo $DEVICE  
sleep 1

echo "----Creating Filesystem----"
mkfs.ext2 "${DEVICE}"
sync

echo "----Making QEMU Image Mountpoint----"
if [ ! -e "${IMAGE_DIR}" ]; then
    mkdir "${IMAGE_DIR}"
    chown "${USER}" "${IMAGE_DIR}"
fi

echo "----Mounting QEMU Image Partition 1----"
mount "${DEVICE}" "${IMAGE_DIR}"

echo "----Extracting Filesystem Tarball----"
tar -xf "${WORK_DIR}/$IID.tar.gz" -C "${IMAGE_DIR}"
rm "${WORK_DIR}/${IID}.tar.gz"

echo "----Creating FIRMADYNE Directories----"
mkdir "${IMAGE_DIR}/firmadyne/"
mkdir "${IMAGE_DIR}/firmadyne/libnvram/"
mkdir "${IMAGE_DIR}/firmadyne/libnvram.override/"

echo "----Adding CI files----"
cp "${SCRIPT_DIR}/test_${ARCH}" "${IMAGE_DIR}/test"
cp "${SCRIPT_DIR}/ci_file" "${IMAGE_DIR}/"

echo "----Patching Filesystem (chroot)----"
cp $(which busybox) "${IMAGE_DIR}"
cp "${SCRIPT_DIR}/fixImage.sh" "${IMAGE_DIR}"
chroot "${IMAGE_DIR}" /busybox ash /fixImage.sh
rm "${IMAGE_DIR}/fixImage.sh"
rm "${IMAGE_DIR}/busybox"

echo "----Setting up FIRMADYNE----"
cp "${CONSOLE}" "${IMAGE_DIR}/firmadyne/console"
chmod a+x "${IMAGE_DIR}/firmadyne/console"
mknod -m 666 "${IMAGE_DIR}/firmadyne/ttyS1" c 4 65

cp "${LIBNVRAM}" "${IMAGE_DIR}/firmadyne/libnvram.so"
chmod a+x "${IMAGE_DIR}/firmadyne/libnvram.so"

cp "${SCRIPT_DIR}/preInit.sh" "${IMAGE_DIR}/firmadyne/preInit.sh"
chmod a+x "${IMAGE_DIR}/firmadyne/preInit.sh"

# cp -r "${IMAGE_DIR}" "${EMU_DIR}/image_${IID}"




echo "----Unmounting QEMU Image----"
sync
umount "${DEVICE}"
del_partition ${IMAGE}


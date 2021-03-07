#!/bin/bash

set -e
set -u
source scripts/env.config

IID=${1}
ARCH=${2}

WORK_DIR="${WORK_DIR}/${IID}"
IMAGE="${WORK_DIR}/image.raw"
KERNEL="${WORK_DIR}/zImage"



QEMU_AUDIO_DRV=none ./qemu-system-arm -m 256 -M virt -kernel ${KERNEL} -drive if=none,file=${IMAGE},format=raw,id=rootfs -device virtio-blk-device,drive=rootfs -append "firmadyne.syscall=1 root=/dev/vda1 console=ttyS0 nandsim.parts=64,64,64,64,64,64,64,64,64,64 rdinit=/firmadyne/preInit.sh rw debug ignore_loglevel print-fatal-signals=1 user_debug=31" -serial file:${WORK_DIR}/qemu.initial.serial.log -serial unix:/tmp/qemu.${IID}.S1,server,nowait -monitor unix:/tmp/qemu.${IID},server,nowait -display none -device virtio-net-device,netdev=net1 -netdev socket,listen=:2000,id=net1 -device virtio-net-device,netdev=net2 -netdev socket,listen=:2001,id=net2 -device virtio-net-device,netdev=net3 -netdev socket,listen=:2002,id=net3 -device virtio-net-device,netdev=net4 -netdev socket,listen=:2003,id=net4

# QEMU_AUDIO_DRV=none  qemu-system-arm -m 256 -M virt -kernel zImage -drive if=none,file="./image.raw",format=raw,id=rootfs -device virtio-blk-device,drive=rootfs -append "firmadyne.syscall=1 root=/dev/vda1 console=ttyS0 nandsim.parts=64,64,64,64,64,64,64,64,64,64 rdinit=/firmadyne/preInit.sh rw debug ignore_loglevel print-fatal-signals=1 user_debug=31" -serial file:"./qemu.initial.serial.log"  -serial unix:/tmp/qemu.3.S1,server,nowait -monitor unix:/tmp/qemu.3,server,nowait -display none -device virtio-net-device,netdev=net1 -netdev socket,listen=:2000,id=net1 -device virtio-net-device,netdev=net2 -netdev socket,listen=:2001,id=net2 -device virtio-net-device,netdev=net3 -netdev socket,listen=:2002,id=net3 -device virtio-net-device,netdev=net4 -netdev socket,listen=:2003,id=net4

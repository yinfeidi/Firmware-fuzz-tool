#!/bin/bash

set -e
set -u
source scripts/env.config



IID=${1}
ARCH=${2}

WORK_DIR="${WORK_DIR}/${IID}"

# cd ${WORK_DIR}
# qemu-img convert -f raw -O qcow2 image.raw image.qcow2
# cd -
if [ "$ARCH" == "mipseb" ]; then
    cp "${KERNEL_DIR}/${ARCH}/vmlinux" "${WORK_DIR}/vmlinux"
    chmod a+x "${WORK_DIR}/vmlinux"
elif [ "$ARCH" == "mipsel" ]; then
    cp "${KERNEL_DIR}/${ARCH}/vmlinux" "${WORK_DIR}/vmlinux"
    chmod a+x "${WORK_DIR}/vmlinux"
elif [ "$ARCH" == "armel" ]; then
    cp "${KERNEL_DIR_ARMEL}/${ARCH}/arch/arm/boot/zImage" "${WORK_DIR}/zImage"
    chmod a+x "${WORK_DIR}/zImage"
else
    echo "Unsupported architecture"
fi

echo "Running firmware ${IID}: terminating after 60 secs..."
timeout --preserve-status --signal SIGINT 60 "${SCRIPT_DIR}/run.${ARCH}.sh" "${IID}" "${ARCH}"
sleep 1

echo "Inferring network..."
"${SCRIPT_DIR}/makeNetwork.py" -i "${IID}" -q -o -a "${ARCH}" -S "${WORK_DIR}"

echo "Done!"

#!/bin/bash

if [ $(id -u) != 0 ]
then
  echo "requires root/sudo" >&2
  exit 1
fi

mnt_dir="/var/run/media/${SUDO_USER}"
boot_dir="${mnt_dir}/boot"
root_dir="${mnt_dir}/rootfs"

if [ ! -d ${boot_dir} ]
then
  echo "${boot_dir} not found" >&2
  exit 1
fi

if [ ! -f wpa_supplicant.conf ]
then
  echo "wpa_supplicant.conf not found" >&2
  exit 1
fi

echo "Configuring SSH" >&2
cp wpa_supplicant.conf ${boot_dir}
touch ${boot_dir}/ssh

if [ -d ${root_dir} ]
then
  if [ -f "${PUBLIC_KEY}" ]
  then
    echo "setting up ${PUBLIC_KEY}" >&2
    mkdir ${root_dir}/home/pi/.ssh
    chmod 700 ${root_dir}/home/pi/.ssh
    cp ${PUBLIC_KEY} ${root_dir}/home/pi/.ssh/authorized_keys
    chown -R 1000:1000 ${root_dir}/home/pi/.ssh
  fi

  echo "Installing Software" >&2
  cp requirements.txt ${root_dir}/home/pi/
  chown 1000:1000 ${root_dir}/home/pi/requirements.txt
  cp christmas.py ${root_dir}/home/pi/
  cp launch_christmas.sh ${root_dir}/home/pi/
  cp simpletest.py ${root_dir}/home/pi/
  chown 1000:1000 ${root_dir}/home/pi/*py
  cp -R lib ${root_dir}/home/pi/
  chown -R 1000:1000 ${root_dir}/home/pi/lib
  cp -R neopix_controller ${root_dir}/home/pi/
  chown -R 1000:1000 ${root_dir}/home/pi/neopix_controller
else
  echo "Use ssh over wifi to install requirements and ssh public key" >&2d
fi
exit

#!/bin/sh -x
if id | grep -qv uid=0; then
    echo "Must run setup as root"
    exit 1
fi

create_socket_dir() {
    local dirname="$1"
    local ownergroup="$2"
    local perms="$3"

    mkdir -p $dirname
    chown $ownergroup $dirname
    chmod $perms $dirname
}

set_perms() {
    local ownergroup="$1"
    local perms="$2"
    local pn="$3"

    chown $ownergroup $pn
    chmod $perms $pn
}

set_perms_r() {
    local ownergroup="$1"
    local perms="$2"
    local pn="$3"

    chown -R $ownergroup $pn
    chmod -R $perms $pn
}

rm -rf /jail
mkdir -p /jail
cp -p index.html /jail

./chroot-copy.sh zookd /jail
./chroot-copy.sh zookfs /jail

#./chroot-copy.sh /bin/bash /jail

./chroot-copy.sh /usr/bin/env /jail
./chroot-copy.sh /usr/bin/python /jail

# to bring in the crypto libraries
./chroot-copy.sh /usr/bin/openssl /jail

mkdir -p /jail/usr/lib /jail/usr/lib/i386-linux-gnu /jail/lib /jail/lib/i386-linux-gnu
cp -r /usr/lib/python2.7 /jail/usr/lib
cp /usr/lib/i386-linux-gnu/libsqlite3.so.0 /jail/usr/lib/i386-linux-gnu
cp /lib/i386-linux-gnu/libnss_dns.so.2 /jail/lib/i386-linux-gnu
cp /lib/i386-linux-gnu/libresolv.so.2 /jail/lib/i386-linux-gnu
cp -r /lib/resolvconf /jail/lib

mkdir -p /jail/usr/local/lib
cp -r /usr/local/lib/python2.7 /jail/usr/local/lib

mkdir -p /jail/etc
cp /etc/localtime /jail/etc/
cp /etc/timezone /jail/etc/
cp /etc/resolv.conf /jail/etc/

mkdir -p /jail/usr/share/zoneinfo
cp -r /usr/share/zoneinfo/America /jail/usr/share/zoneinfo/

create_socket_dir /jail/echosvc 61010:61010 755
create_socket_dir /jail/authsvc 61030:61030 755
create_socket_dir /jail/banksvc 61040:61040 755
create_socket_dir /jail/profilesvc 0:61020 755

mkdir -p /jail/tmp
chmod a+rwxt /jail/tmp

mkdir -p /jail/dev
mknod /jail/dev/urandom c 1 9

cp -r zoobar /jail/
rm -rf /jail/zoobar/db

python /jail/zoobar/zoodb.py init-person
python /jail/zoobar/zoodb.py init-transfer
python /jail/zoobar/zoodb.py init-cred
python /jail/zoobar/zoodb.py init-bank

# 61020 -> gid for zoofs-based service
# 61021 -> uid for dynamic
# 61022 -> uid for static
# 61025 -> gid for scripts
set_perms 61011:61011 100 /jail/zookd
set_perms 61020:61020 010 /jail/zookfs

# executables must in the group 61025
set_perms 61021:61025 500 /jail/zoobar/index.cgi

# dynamic fs service
set_perms 61020:61020 070 /jail/zoobar/db
set_perms_r 61030:61030 700 /jail/zoobar/db/cred
set_perms_r 61021:61030 770 /jail/zoobar/db/person
set_perms_r 61021:61021 700 /jail/zoobar/db/transfer
set_perms_r 61040:61040 700 /jail/zoobar/db/bank
set_perms 61021:61021 400 /jail/zoobar/*.py
set_perms 61021:61021 400 /jail/zoobar/*.pyc

# static fs service
set_perms 61022:61022 400 /jail/index.html
set_perms 61022:61022 400 /jail/zoobar/media/*
set_perms 61022:61022 400 /jail/zoobar/templates/*

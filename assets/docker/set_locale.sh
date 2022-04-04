# Configuring locales
# https://github.com/oerdnj/deb.sury.org/issues/56#issuecomment-93694233
apt-get install -y locales locales-all
locale-gen en_US.UTF-8
export LANG="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"
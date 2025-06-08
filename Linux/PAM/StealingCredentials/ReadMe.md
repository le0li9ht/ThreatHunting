#### Disclaimer

_This article is intended for educational and awareness purposes only. The techniques demonstrated are for understanding security risks and improving defenses. Unauthorized use or replication of these methods for malicious activities is strictly prohibited and may be illegal. Always obtain proper authorization before testing or simulating attacks on any systems. The author is not responsible for any misuse, damage, or illegal activities resulting from applying the techniques discussed._

### Background  
PAM modules are dynamically loaded components that handle authentication on Linux systems. Attackers can exploit this by installing malicious modules and modifying PAM’s configuration to load them during login. This allows the attacker to secretly capture user credentials whenever authentication occurs, making it a powerful vector for persistent access and data theft  

Note: This was tested on Debian-based systems. The provided steps are specifically tailored for Debian/Ubuntu environments. For Fedora or Red Hat systems, just update the library and configuration file paths—the module code remains the same.  
#### How the backdoor works?
The malicious code hooks into _pam_sm_authenticate()_, capturing the username via _pam_get_user()_ and the password via _pam_get_authtok()_ before silently logging or exfiltrating them. Meanwhile, _pam_sm_setcred()_ completes the authentication process to avoid detection.

I’ve uploaded code for two Linux PAM modules: one logs credentials to disk (already compiled), and the other exfiltrates to Google Forms (requires updating values before compiling). Download [here](https://github.com/le0li9ht/ThreatHunting/blob/main/Linux/PAM/StealingCredentials/pam_backdoor_lab.zip)  
##### Code files

```
pam_backdoor_lab.zip
│
├── pam_backdoor_disklog/
│   ├── pam_backdoor.c
|   ├── pam_backdoor.so
└── pam_backdoor_googleform/
    ├── pam_backdoor.c
```

For the first, just copy the compiled module to the shared library location.  I have not compiled the second module yet because it requires updating the Google Form URL(as shown in below image) and entry values in the source code. Once those are set, you can compile and deploy the module.    

![image](https://github.com/user-attachments/assets/e5021065-7e31-4744-804d-8bf18cf60bcf)  

At the time of writing, this module was not flagged as malicious by VirusTotal, highlighting how such techniques can easily evade standard detection mechanisms.  
![2025-06-08_01-42](https://github.com/user-attachments/assets/2a19e69b-50cc-4979-a96d-056d352f846b)  
https://www.virustotal.com/gui/file/c7022836a3f92a6589df7cce99ee3db69ce0a98a7c266ba90a8ec5e37227329e?nocache=1   

#### Step 1: Install Development Package for PAM Modules    
You need to install libpam0g-dev because it provides the header files and libraries required to compile custom PAM modules  
```
sudo apt update  
sudo apt install libpam0g-dev  
```  
#### Step 2: Compile the Backdoor PAM Module  
```
gcc -fPIC -fno-stack-protector -c pam_backdoor.c  
ld -x --shared -o pam_backdoor.so pam_backdoor.o
```
#### Step3: Deploy the Backdoor Module into PAM's Trusted Directory  
Copy the backdoor module to /lib/x86_64-linux-gnu/security/ because it’s the default trusted location for PAM modules, ensuring it’s automatically loaded by all PAM-aware services and stays hidden among legitimate system files for better stealth and persistence.   
```
sudo cp pam_backdoor.so /lib/x86_64-linux-gnu/security/
```      
Modify the _common-auth_ file under _/etc/pam.d_ , which handles authentication, by inserting the backdoor module at the top of the PAM authentication stack. This ensures it executes first during all authentication requests, allowing the backdoor to intercept credentials stealthily and persistently across system login processes.  
```
sed -i '1i auth required pam_backdoor.so' /etc/pam.d/common-auth
```   

#### Step4: Test the Backdoor Module 
Perform any authentication action like `sudo`, `su`, `su -`, or SSH logins. The backdoor will capture and log all credentials during these authentications.
```
sudo su
su -
ssh user@ip
```

- **If using the disk-logging module:**  
All captured credentials are saved to a hidden, seemingly legitimate file on disk named /tmp/.X11-unixs. To view the stolen creds, run:   
```
cat /tmp/.X11-unixs
```
![2025-06-08_01-34](https://github.com/user-attachments/assets/63e2bfb4-5833-44b1-bce3-e8afeb6fe1ce)


- **If using the Google Forms exfiltration module:**
Credentials are sent silently to your configured Google Form. Check your Google Form responses to verify captured data as shown.
![2025-06-08_00-54_1](https://github.com/user-attachments/assets/ae275802-ce96-4481-9354-c30fae9c7e56)   
![2025-06-08_00-54](https://github.com/user-attachments/assets/8d773b2c-7369-4e9e-af75-7961f9da1fef)
Exfiltrated credentials on google form.
  
#### Detection. 
Always monitor the directories where PAM modules are loaded—such as /etc/pam.d/ and /lib/security/  /lib/x86_64-linux-gnu/security/  —using File Integrity Monitoring (FIM) to detect unauthorized changes.  

Elastic has written a nicr detection rule for the same [persistence_pluggable_authentication_module_creation](https://github.com/elastic/detection-rules/blob/ac541f0b18697e053b3b56544052955d29b440c0/rules/linux/persistence_pluggable_authentication_module_creation.toml)  
##### MITRE. 
[T1556.003 - Pluggable Authentication Modules: Malicious PAM](https://attack.mitre.org/techniques/T1556/003/)  



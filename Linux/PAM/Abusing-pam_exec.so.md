### MITRE ATT&CK
[T1556.003-Modify Authentication Process: Pluggable Authentication Modules](https://attack.mitre.org/techniques/T1556/003/)  

**Goal:**  The pam_exec.so module in Linux Pluggable Authentication Modules (PAM) provides a flexible mechanism to execute custom scripts during various authentication stages. While commonly used for legitimate logging and access control purposes, this feature can be maliciously abused to trigger backdoor scripts in response to specific authentication events. 
**Test Environment:** Ubuntu 22.04  

![PAM-Exec-SSHFailure](https://github.com/user-attachments/assets/d3cf8ab4-b491-46fc-a378-865b55e71808)

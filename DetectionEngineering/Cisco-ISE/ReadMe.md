## Cisco ISE Log Reference Guide
For detection engineers and security analysts, having a structured log reference is critical during log ingestion, parsing, and incident investigation. I wrote a Python script that automates the extraction of Cisco ISE syslog message codes from [official documentation](https://www.cisco.com/c/en/us/td/docs/security/ise/syslog/Cisco_ISE_Syslogs/m_SyslogsList.html) and saves them into a csv file as shown. 
### Prerequisites:  
- Install Python3
- Install the following modules.
```
pip3 install requests
pip3 install beautifulsoup4
pip3 install bs4
```
Download the [script](https://github.com/le0li9ht/ThreatHunting/blob/main/DetectionEngineering/Cisco-ISE/Parse-ISE.py). Finally run the script as shown:  
```
python3 Parse-ISE.py
```
![image](https://github.com/user-attachments/assets/cff986da-5177-4d3d-a2fb-11bfdff75c6d)

[Attached below](https://github.com/le0li9ht/ThreatHunting/blob/main/DetectionEngineering/Cisco-ISE/cisco_ise_syslog_reference.csv.csv) is the list of Cisco ISE message codes that were extracted: 
  
![image](https://github.com/user-attachments/assets/923722d0-6dde-4a8e-bfd4-f9150a6630b4)

### References:  
https://www.cisco.com/c/en/us/td/docs/security/ise/syslog/Cisco_ISE_Syslogs/m_SyslogsList.html  



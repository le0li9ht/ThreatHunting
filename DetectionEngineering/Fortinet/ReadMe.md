### Extracting Fortinet Events from the Log Reference Guide Made Easy
While working on Fortinet log integration with SIEM, one major challenge is identifying and filtering relevant events from the extensive Fortinet Log Reference Guide — which often requires tedious copy-pasting. To simplify this, I built a Python script that extracts all Fortinet event details from the PDF and neatly converts them into a CSV file for easier analysis and use. Sharing it here so others working on similar integrations can save time and effort!
#### How to use the script  
**Step1:** Install Python3  
**Step2:** Install the PyMuPDF module.  
Run the following command to install PyMuPDF module.  
  ``pip install PyMuPDF``  
**Step3:** Run the [script](https://raw.githubusercontent.com/le0li9ht/ThreatHunting/refs/heads/main/DetectionEngineering/Fortinet/Fortievents_to_csv.py) and provide the path to the log reference guide pdf and provide output csv file path.  
   ``python3 Fortievents_to_csv.py``    
     
![image](https://github.com/user-attachments/assets/034591f6-d28c-4c3d-90ee-cac24522a267)  

**NOTE:** I have attached a sample [xls file](https://github.com/le0li9ht/ThreatHunting/blob/main/DetectionEngineering/Fortinet/FortinetLogEvents.xlsx) with extracted events for some versions also I have given some Important events that should be collected and monitor by any SIEM product.   
  
![2025-06-05_19-41](https://github.com/user-attachments/assets/d5150a01-6a9e-4d06-8cdf-4f6675305306)

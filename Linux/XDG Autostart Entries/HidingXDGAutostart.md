### Hide and Persist: XDG Autostart Abuse on Linux Systems
#### [T1547.013 -  Boot or Logon Autostart Execution: XDG Autostart Entries](https://attack.mitre.org/techniques/T1547/013/)  
XDG defines a standardized method for automatically starting applications during the startup of any XDG-compliant desktop environment, stating that _By placing an application's .desktop file in one of the Autostart directories the application will be automatically launched during startup of the user's desktop environment after the user has logged in_   

Autostart directories include:  
- ~/.config/autostart (user-specific)
- /etc/xdg/autostart/ (system-wide)

To understand this better, think about your daily use of an Ubuntu desktop. You might want certain applications—like your browser or messaging app—to open automatically when you log in. To configure this, you can use the Startup Applications utility (gnome-session-properties). For example, if you want Brave Browser to launch on login, you can add it to the startup list through this tool as shown: 

![image](https://github.com/user-attachments/assets/ccbd01dc-768f-4f90-856d-7ef220cab5d6)  

Since this is a user-level startup action, it creates a corresponding .desktop file under the ~/.config/autostart/ directory to launch Brave Browser at startup, as mentioned earlier.  

![2025-06-19_09-20](https://github.com/user-attachments/assets/53cf698d-53a8-4a19-a526-e54791fb21c5)

Alternatively, you can mimic the same action by copying the .desktop file for Brave Browser from /usr/share/applications/brave-browser.desktop to ~/.config/autostart/ as shown.  

![2025-06-19_10-15](https://github.com/user-attachments/assets/4a94ef81-a4bb-4829-ab7c-b83c34142d76)    
Running the above command copies the brave-browser.desktop file from the system-wide applications directory to the user-specific xdg autostart location as shown above.
Now, try logging out and logging back in—or simply restart your system—and you’ll see that Brave Browser launches automatically at startup  
#### How attackers abuse xdg autostart entries
Now that you understand how XDG Autostart functionality works, let’s explore how attackers can abuse it to maintain persistence on a compromised system.  
Adversaries may abuse XDG Autostart entries to establish persistence on XDG-compliant Linux systems by placing malicious .desktop files in the autostart directories mentioned earlier or by modifying the Exec directive within an existing .desktop file to run arbitrary commands or binaries. These files are automatically executed when the user's desktop environment loads at login, making this a prime technique for stealthy backdoors.  
An example malicious file.    
```
[Desktop Entry]
Type=Application
Name=System Application
Exec="/home/mal.sh"
X-GNOME-Autostart-enabled=true
```
#### Hiding xdg autostart backdoor
Wait—we already know this technique; it’s widely used by both threat actors and red teamers. But the problem is, when abused in its default form, it’s easily detectable. For example, if you create a malicious autostart entry as shown below, it will immediately appear in the Startup Applications utility.  

![2025-06-19_11-07_1](https://github.com/user-attachments/assets/d075efc5-7163-4329-a223-49bc52d0a50c)

This means even a regular user could spot it and recognize it as suspicious. So, while the technique is effective, it's not stealthy.  Now, let me show you how to make it invisible to the eyes of a normal desktop user   

to make the .desktop entry invisible in the Startup Applications GUI, you can use either of the following stealth techniques:

- Change **NoDisplay=false** to **NoDisplay=true** - This hides the entry from GUI-based startup managers like gnome-session-properties, but it will still execute at login.  
  
![2025-06-19_11-07](https://github.com/user-attachments/assets/51512a1e-8c56-4e16-b79d-8ef194614b3c)



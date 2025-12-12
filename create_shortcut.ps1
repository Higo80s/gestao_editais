
$WshShell = New-Object -comObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$Shortcut = $WshShell.CreateShortcut("$DesktopPath\Gestao Editais.lnk")
$Shortcut.TargetPath = "c:\Users\higosantos\Documents\gestao_editais\gestao_editais_novo\Gestao_Editais.bat"
$Shortcut.WindowStyle = 1
$Shortcut.IconLocation = "c:\Users\higosantos\Documents\gestao_editais\gestao_editais_novo\static\favicon.ico"
$Shortcut.Save()

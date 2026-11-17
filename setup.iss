; Inno Setup 7 -skripti Theme Studio V.2:lle
; Tekijä: tommi.jalkanen@gmail.com

#define MyAppName "Theme Studio"
#define MyAppVersion "2.1"
#define MyAppPublisher "Tommi Jalkanen"
#define MyAppExeName "theme_studio.exe"

[Setup]
AppId={{B8A19F23-441A-4E32-8C52-F8E32D15A19B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
OutputDir=.
OutputBaseFilename=ThemeStudio_Installer_v2.1

; 1. Asennustiedoston (.exe) oma kuvake:
SetupIconFile=installer_icon.ico
; 2. Kuvake Windowsin "Asennetut sovellukset" (Lisää/Poista sovellus) -listaan:
UninstallDisplayIcon={app}\{#MyAppExeName}
; 3. Oma logo asennusvelhon (Setup Wizard) oikeaan yläkulmaan:
WizardSmallImageFile=wizard_logo.bmp

Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "finnish"; MessagesFile: "compiler:Languages\Finnish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "installer_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\installer_icon.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\installer_icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
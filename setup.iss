; Theme Studio Installer
; Copyright (c) 2026 Tommi Jalkanen
; All rights reserved.

#define MyAppName "Theme Studio"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Tommi Jalkanen"
#define MyAppExeName "theme_studio.exe"

[Setup]
AppId={{B8A19F23-441A-4E32-8C52-F8E32D15A19B}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

AppCopyright=Copyright (c) 2026 Tommi Jalkanen. All rights reserved.

DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}

PrivilegesRequired=admin

DisableProgramGroupPage=yes

OutputDir=.
OutputBaseFilename=ThemeStudio_Installer_v1.0.0

SetupIconFile=app_icon.ico

Compression=lzma
SolidCompression=yes
WizardStyle=modern

VersionInfoVersion=1.0.0.0
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=Theme Studio
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}

UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "finnish"; MessagesFile: "compiler:Languages\Finnish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "app_icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: isreadme ignoreversion
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\app_icon.ico"

Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\app_icon.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; \
Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; \
Flags: nowait postinstall skipifsilent
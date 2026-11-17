# -*- coding: utf-8 -*-
"""
Theme Studio V.2

Copyright (c) 2026 Tommi Jalkanen.
All rights reserved.

This software and its source code are proprietary.
No part of this software may be copied, modified,
distributed, published, sublicensed, reverse engineered,
or used without the prior written permission of the
copyright holder.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
"""

import os
import io
import json
import time
import shutil
import struct
import zipfile
import datetime
import threading
import subprocess
import ctypes
import winreg
import hashlib
import colorsys
import tkinter as tk
from tkinter import font as tkfont
import customtkinter as ctk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageOps, ImageDraw
import windnd
from typing import cast
import locale

def get_system_language() -> str:
    try:
        lang_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        lang_code = locale.windows_locale.get(lang_id, "en_US")

        if lang_code.lower().startswith("fi"):
            return "FI"

        return "EN"

    except Exception:
        return "EN"


LANG = get_system_language()

TEXTS = {
    "FI": {
        "theme_title": "Theme Studio V.2",
        "browse": "Selaa...",
        "ready": "Valmis.",
        "image_gallery": "Kuvagalleria",
        "wallpaper": "Taustakuva",
        "apply": "Käytä",
        "save": "Tallenna",
        "cancel": "Peruuta",
        "close": "Sulje",
        "start_processing": "Aloita käsittely",
        "source_folder": "Lähdekansio:",
        "destination_folder": "Kohdekansio:",
        "theme_taskbar": "Teema, tehtäväpalkki ja resurssienhallinta",
        "sidebar_theme": "Teema, tehtäväpalkki ja resurssienhallinta",
        "sidebar_gallery": "Kuvagalleria",
        "sidebar_icons": "Järjestelmäkuvakkeet ja paketit",
        "sidebar_cursors": "Osoittimet ja luonti",
        "sidebar_folders": "Kansiokuvakkeet",
        "sidebar_batch": "Massakuvakäsittely",
        "sidebar_profiles": "Profiilit ja päivä/yö",
        "theme_page_title": "Teema, resurssienhallinta ja värit",
        "windows_dark_mode": "Windows tumma tila",
        "system_transparency": "Tehtäväpalkin läpinäkyvyys",
        "taskbar_glass_title": "Tehtäväpalkin läpinäkyvyys ja lasiefekti",
        "effect_mode": "Tehoste",
        "opacity": "Läpinäkyvyys",
        "apply_taskbar": "Käytä tehtäväpalkkiin",
        "keep_effect_active": "Pidä tehoste aktiivisena",
        "explorer_title": "Resurssienhallinnan teema ja asettelu",
        "theme_mode": "Teema",
        "compact_spacing": "Tiivis asettelu",
        "restart_explorer": "Käynnistä Explorer uudelleen",
        "wallpaper_title": "Työpöydän taustakuva ja väripaletti",
        "no_file_selected": "Tiedostoa ei ole valittu",
        "browse_wallpaper": "Valitse taustakuva...",
        "fit": "Sovitus",
        "auto_wallpaper_color": "Käytä taustakuvan pääväriä automaattisesti",
        "palette_hint": "Valitse taustakuva nähdäksesi värit",
        "accent_title": "Windows-korostusväri ja paletti",
        "apply": "Käytä",
        "pick_color": "Valitse väri...",
        "colorize_taskbar": "Väritä tehtäväpalkki ja Käynnistä-valikko",
        "colorize_borders": "Väritä otsikkopalkit ja ikkunan reunat",
        "font_preview_title": "Sovelluksen fontti ja esikatselu",
        "shades": "Sävyt",
        "font": "Fontti",
        "style": "Tyyli",
        "color": "Väri",
        "change_color": "Vaihda väri",
        "sample_text": "Esimerkkiteksti näyttää tältä.",
        "undo_last_change": "Kumoa viimeisin muutos",
        "restore_point_before_changes": "Luo palautuspiste ennen järjestelmämuutoksia",
        "restore_point_ready": "Palautuspiste: Valmis",
        "preview_window_title": "Resurssienhallinta - esikatselu",
        "preview_title": "Resurssienhallinta",
        "preview_subtext": "Esikatselu nykyisestä teemasta, korostusväristä ja fontista.",
        "preview_body": "Esikatseluteksti käyttää nykyisiä fontti-, tyyli- ja väriasetuksia.",
        "preview_window_title": "Resurssienhallinta - esikatselu",
        "preview_title": "Resurssienhallinta",
        "preview_subtext": "Esikatselu nykyisestä teemasta, korostusväristä ja fonttiasetuksista.",
        "preview_body": "Esikatseluteksti käyttää nykyisiä fontti-, tyyli- ja väriasetuksia.",
        "preview_textbox": "Esikatselutekstikenttä...",
        "preview_checkbox": "Ota teemaominaisuus käyttöön",
        "preview_accent_button": "Korostuspainike",
        "preview_secondary_button": "Toissijainen toiminto",
        "restore_defaults": "Palauta asetukset",
        "gallery_title": "Kuvagalleria",
        "current_folder": "Nykyinen kansio",
        "change_folder": "Vaihda kansio...",
        "refresh_gallery": "Päivitä galleria",
        "send_to_batch": "Lähetä massakäsittelyyn",
        "include_subfolders": "Sisällytä alikansiot",
        "gallery_status": "Näytetään {shown} / {total} kuvaa. Klikkaa kuvaa kokoruudun esikatseluun tai käytä pikatoimintoja alla.",
        "wallpaper_btn": "Taustakuva",
        "palette_btn": "Paletti",
        "icon_btn": "Kuvake",
        "cursor_btn": "Osoittimeksi",
        "no_images_found": "Tuettuja kuvia ei löytynyt.",
        "icons_title": "Työpöydän järjestelmäkuvakkeet ja kuvakepaketit (.zip)",
        "icons_description": "Valitse yksittäisiä .ico- ja .png-kuvia tai tuo/vie kokonaisia kuvakepaketteja (.zip).",
        "icon_pack": "Kuvakepaketti (.zip)",
        "import_icon_pack": "Tuo kuvakepaketti (.zip)",
        "export_icon_pack": "Vie nykyinen kuvakepaketti (.zip)",
        "this_pc": "Tämä tietokone",
        "recycle_bin": "Roskakori",
        "user_files": "Käyttäjän tiedostot",
        "default_current": "Oletus / Nykyinen",
        "change_icon": "Vaihda kuvake...",
        "cursor_title": "Hiiriosoittimet, osoitinpaketit ja osoittimen luonti",

        "cursor_description": "Määritä .cur- ja .ani-tiedostoja, tuo/vie osoitinpaketteja (.zip) tai luo mukautettuja osoittimia mistä tahansa kuvasta.",

        "cursor_pack": "Osoitinpaketti (.zip)",
        "import_cursor_pack": "Tuo osoitinpaketti (.zip)",
        "export_cursor_pack": "Vie osoitinpaketti (.zip)",

        "cursor_normal": "Normaali valinta (Nuoli)",
        "cursor_link": "Linkin valinta (Käsi)",
        "cursor_text": "Tekstin valinta (I-palkki)",
        "cursor_working": "Työskentely taustalla",

        "default_cursor": "Oletusosoitin",
        "select_cursor": "Valitse .cur / .ani...",

        "cursor_creator_title": "Luo mukautettu Windows-osoitin (.cur) kuvasta (PNG / JPG / WEBP)",

        "cursor_creator_description": "Valitse kuva, määritä hotspot-piste (X,Y) sekä osoittimen koko ja muunna kuva Windows-osoittimeksi.",

        "select_source_image": "Valitse lähdekuva...",
        "no_image_selected": "Kuvaa ei ole valittu",

        "target_role": "Kohderooli",
        "cursor_size": "Koko",

        "generate_cursor": "Luo .CUR ja ota käyttöön",
        "save_cursor_as": "Tallenna .CUR nimellä...",
        "hotspot_x": "Hotspot X",
        "hotspot_y": "Hotspot Y",
        "folder_title": "Kansiokuvakkeiden mukautus (desktop.ini)",

        "folder_description": "Vedä ja pudota kansio sekä PNG/ICO-kuva tähän ikkunaan tai valitse ne alla olevilla painikkeilla.",

        "folder_dropzone": "📁 Pudota kansio tai kuvake (.png / .ico) tähän",

        "target_folder": "Kohdekansio",
        "new_icon": "Uusi kuvake",

        "not_selected": "Ei valittu",

        "browse_folder": "Valitse kansio...",
        "browse_image": "Valitse kuva...",

        "set_folder_icon": "Aseta kansiokuvake",
        "restore_folder_icon": "Palauta oletuskansiokuvake",
        "batch_title": "Massakuvakäsittely",

        "source_folder": "Lähdekansio",
        "destination_folder": "Kohdekansio",

        "browse": "Selaa...",

        "include_subfolders": "Sisällytä alikansiot",

        "naming_style": "Nimeämistapa",
        "prefix_number": "Etuliite + Numero",
        "prefix_original": "Etuliite + Alkuperäinen nimi",

        "name_prefix": "Etuliite",

        "output_format": "Tulostusmuoto",

        "compression_quality": "Pakkauslaatu",

        "resize_images": "Muuta kuvien kokoa",

        "width": "Leveys",
        "height": "Korkeus",

        "center_crop": "Keskitä rajaus",

        "aspect_ratio_hint": "Jätä toinen kenttä tyhjäksi säilyttääksesi kuvasuhteen.",

        "auto_fix_orientation": "Korjaa puhelinkuvien suunta automaattisesti",

        "strip_metadata": "Poista kaikki metatiedot (GPS, kamera jne.) tilan säästämiseksi",

        "start_processing": "Aloita käsittely",
        # Profiilit ja ajastin
        "profiles_main_title": "Teemaprofiilit, teemapaketit (.zip) ja päivä/yö-ajastin",
        "profiles_main_desc": "Tallenna JSON-profiileja, luo siirrettäviä teemapaketteja (.zip) tai automatisoi päivä/yö-vaihto.",
        "enter_profile_name": "Syötä uuden profiilin nimi...",
        "save_profile": "Tallenna profiili",
        "import_json": "Tuo .json",
        "export_theme_zip": "Vie teema (.zip)",
        "import_theme_zip": "Tuo teema (.zip)",
        "auto_day_night_title": "Automaattinen päivä/yö-teeman vaihtaja:",
        "enable_auto_schedule": "Ota automaattinen aikataulu käyttöön",
        "day_profile": "Päiväprofiili:",
        "start_time": "Alkaa (HH:MM):",
        "night_profile": "Yöprofiili:",
        "scheduler_status_inactive": "Ajastimen tila: Ei käytössä",
        "saved_profiles": "Tallennetut profiilit:",
        "no_saved_profiles": "Ei tallennettuja profiileja.",
        "apply": "Ota käyttöön",
        "delete": "Poista",
        "dark": "Tumma",
        "light": "Vaalea"
       
        
    },

    "EN": {
        "theme_title": "Theme Studio V.2",
        "browse": "Browse...",
        "ready": "Ready.",
        "image_gallery": "Image Gallery",
        "wallpaper": "Wallpaper",
        "apply": "Apply",
        "save": "Save",
        "cancel": "Cancel",
        "close": "Close",
        "start_processing": "Start Processing",
        "source_folder": "Source Folder:",
        "destination_folder": "Destination Folder:",
        "theme_taskbar": "Theme, Taskbar & Explorer",
        "sidebar_theme": "Theme, Taskbar & Explorer",
        "sidebar_gallery": "Image Gallery",
        "sidebar_icons": "System Icons & Packs",
        "sidebar_cursors": "Cursors & Creator",
        "sidebar_folders": "Folder Icons",
        "sidebar_batch": "Batch Image Processing",
        "sidebar_profiles": "Profiles & Day/Night",
        "theme_page_title": "Theme, Explorer & Palette",
        "windows_dark_mode": "Windows Dark Mode",
        "system_transparency": "System & Taskbar Transparency",
        "taskbar_glass_title": "Taskbar Live Transparency & Glass Effect",
        "effect_mode": "Effect Mode",
        "opacity": "Opacity",
        "apply_taskbar": "Apply to Taskbar",
        "keep_effect_active": "Keep effect active",
        "explorer_title": "File Explorer Color Theme & Layout Manager",
        "theme_mode": "Theme Mode",
        "compact_spacing": "Compact File Explorer Spacing",
        "restart_explorer": "Restart Explorer.exe",
        "wallpaper_title": "Desktop Wallpaper, Fit Style & Smart Color Palette",
        "no_file_selected": "No file selected",
        "browse_wallpaper": "Browse wallpaper...",
        "fit": "Fit",
        "palette_hint": "Select wallpaper to see colors",
        "auto_wallpaper_color": "Automatically apply wallpaper's primary color",
        "accent_title": "Windows Accent Color & Palette Export",
        "apply": "Apply",
        "pick_color": "Pick color...",
        "colorize_taskbar": "Colorize taskbar and start menu",
        "colorize_borders": "Colorize title bars and window borders",
        "font_preview_title": "App Font & Live Preview",
        "shades": "Shades",
        "font": "Font",
        "style": "Style",
        "color": "Color",
        "change_color": "Change Color",
        "sample_text": "Sample text looks like this.",
        "undo_last_change": "Undo Last Change",
        "restore_point_before_changes": "Create restore point before system changes",
        "restore_point_ready": "Restore Point: Ready",
        "preview_window_title": "File Explorer - Live Preview",
        "preview_title": "File Explorer",
        "preview_subtext": "Live preview of current theme, accent color, and font settings.",
        "preview_body": "Preview text follows current font family, style, and color settings.",
        "preview_window_title": "File Explorer - Live Preview",
        "preview_title": "File Explorer",
        "preview_subtext": "Live preview of current theme, accent color, and font settings.",
        "preview_body": "Preview text follows current font family, style, and color settings.",
        "preview_textbox": "Preview text box...",
        "preview_checkbox": "Enable theme feature",
        "preview_accent_button": "Accent Button",
        "preview_secondary_button": "Secondary Action",
        "restore_defaults": "Restore System Defaults",
        "gallery_title": "Image Gallery",
        "current_folder": "Current folder",
        "change_folder": "Change folder...",
        "refresh_gallery": "Refresh gallery",
        "send_to_batch": "Send Folder to Batch Processing",
        "include_subfolders": "Include subfolders",
        "gallery_status": "Showing {shown} of {total} images. Click image for full preview or use quick actions below.",
        "wallpaper_btn": "Wallpaper",
        "palette_btn": "Palette",
        "icon_btn": "Icon",
        "cursor_btn": "To Cursor",
        "no_images_found": "No supported images found.",
        "icons_title": "Desktop System Icons & Icon Packs (.zip)",
        "icons_description": "Select individual .ico / .png files or import/export complete Icon Pack (.zip) archives.",
        "icon_pack": "Icon Pack (.zip)",
        "import_icon_pack": "Import Icon Pack (.zip)",
        "export_icon_pack": "Export Current as Icon Pack (.zip)",
        "this_pc": "This PC",
        "recycle_bin": "Recycle Bin",
        "user_files": "User's Files",
        "default_current": "Default / Current",
        "change_icon": "Change Icon...",
        "cursor_title": "Mouse Pointers, Cursor Packs & Cursor Creator",

        "cursor_description": "Assign .cur / .ani files, import/export Cursor Packs (.zip), or build custom cursors from any image.",

        "cursor_pack": "Cursor Pack (.zip)",
        "import_cursor_pack": "Import Cursor Pack (.zip)",
        "export_cursor_pack": "Export Cursor Pack (.zip)",

        "cursor_normal": "Normal Select (Arrow)",
        "cursor_link": "Link Select (Hand)",
        "cursor_text": "Text Select (IBeam)",
        "cursor_working": "Working in Background (AppStarting)",

        "default_cursor": "Default Cursor",
        "select_cursor": "Select .cur / .ani...",

        "cursor_creator_title": "Create Custom Windows Cursor (.cur) from Image (PNG / JPG / WEBP)",

        "cursor_creator_description": "Select any image, set the click Hotspot (X,Y) coordinates and cursor size, and convert directly into a native Windows cursor.",

        "select_source_image": "Select Source Image...",
        "no_image_selected": "No image selected",

        "target_role": "Target Role",
        "cursor_size": "Size",

        "generate_cursor": "Generate .CUR & Apply Immediately",
        "save_cursor_as": "Save .CUR File As...",
        "hotspot_x": "Hotspot X",
        "hotspot_y": "Hotspot Y",
        "folder_title": "Folder Customization (desktop.ini)",

        "folder_description": "Drag & Drop a folder and a PNG/ICO image directly to this window or browse below.",

        "folder_dropzone": "📁 Drag a folder or icon (.png / .ico) here",

        "target_folder": "Target Folder",
        "new_icon": "New Icon",

        "not_selected": "Not selected",

        "browse_folder": "Browse folder...",
        "browse_image": "Browse image...",

        "set_folder_icon": "Set Folder Icon",
        "restore_folder_icon": "Restore Default Folder Icon",
        "batch_title": "Mass Image Processing",

        "source_folder": "Source Folder",
        "destination_folder": "Destination Folder",

        "browse": "Browse...",

        "include_subfolders": "Include subfolders",

        "naming_style": "Naming Style",
        "prefix_number": "Prefix + Number",
        "prefix_original": "Prefix + Original Name",

        "name_prefix": "Name Prefix",

        "output_format": "Output Format",

        "compression_quality": "Compression Quality",

        "resize_images": "Resize Images",

        "width": "Width",
        "height": "Height",

        "center_crop": "Center Crop",

        "aspect_ratio_hint": "Leave one field empty to maintain aspect ratio.",

        "auto_fix_orientation": "Auto-fix orientation for phone images",

        "strip_metadata": "Strip all metadata (GPS, Camera, etc.) to save space",

        "start_processing": "Start Processing",
        # Profiles and Scheduler
        "profiles_main_title": "Theme Profiles, Theme Packs (.zip) & Day/Night Scheduler",
        "profiles_main_desc": "Save JSON profiles, create portable theme packs (.zip), or automate day/night switching.",
        "enter_profile_name": "Enter new profile name...",
        "save_profile": "Save Profile",
        "import_json": "Import .json",
        "export_theme_zip": "Export Theme (.zip)",
        "import_theme_zip": "Import Theme (.zip)",
        "auto_day_night_title": "Automatic Day/Night Theme Switcher:",
        "enable_auto_schedule": "Enable auto schedule",
        "day_profile": "Day Profile:",
        "start_time": "Start (HH:MM):",
        "night_profile": "Night Profile:",
        "scheduler_status_inactive": "Scheduler status: Inactive",
        "saved_profiles": "Saved Profiles:",
        "no_saved_profiles": "No saved profiles.",
        "apply": "Apply",
        "delete": "Delete",
        "dark": "Dark",
        "light": "Light"

        
    }
}

T = TEXTS[LANG]

# --- WIN32 API CONSTANTS ---
SPI_SETDESKWALLPAPER = 0x0014
SPI_SETCURSORS = 0x0057
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02

SHCNE_ASSOCCHANGED = 0x08000000
SHCNE_UPDATEDIR = 0x00001000
SHCNF_IDLIST = 0x0000
SHCNF_PATHW = 0x0005

WM_SETTINGCHANGE = 0x001A
HWND_BROADCAST = 0xFFFF
SMTO_ABORTIFHUNG = 0x0002

FILE_ATTRIBUTE_READONLY = 0x01
FILE_ATTRIBUTE_HIDDEN = 0x02
FILE_ATTRIBUTE_SYSTEM = 0x04
FILE_ATTRIBUTE_NORMAL = 0x80

# System Icon CLSIDs
CLSID_THIS_PC = "{20D04FE0-3AEA-1069-A2D8-08002B30309D}"
CLSID_RECYCLE_BIN = "{645FF040-5081-101B-9F08-00AA002F954E}"
CLSID_USER_FILES = "{59031a47-3f72-44a7-89c5-5595fe6b30ee}"

BASE_APP_DIR = os.path.join(os.path.expanduser("~"), ".win_theme_studio_icons")
PROFILES_DIR = os.path.join(BASE_APP_DIR, "profiles")
CUSTOM_CURSORS_DIR = os.path.join(BASE_APP_DIR, "custom_cursors")
PACKS_IMPORT_DIR = os.path.join(BASE_APP_DIR, "imported_packs")
GALLERY_DIR = r"C:\Windows\Web\Wallpaper"

for _d in (BASE_APP_DIR, PROFILES_DIR, CUSTOM_CURSORS_DIR, PACKS_IMPORT_DIR):
    os.makedirs(_d, exist_ok=True)


# --- WIN32 STRUCTURES FOR TASKBAR TRANSPARENCY ---
class ACCENT_POLICY(ctypes.Structure):
    _fields_ = [
        ("AccentState", ctypes.c_int),
        ("AccentFlags", ctypes.c_int),
        ("GradientColor", ctypes.c_uint),
        ("AnimationId", ctypes.c_int),
    ]


class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
    _fields_ = [
        ("Attribute", ctypes.c_int),
        ("Data", ctypes.POINTER(ACCENT_POLICY)),
        ("SizeOfData", ctypes.c_size_t),
    ]


class WindowsThemeEngine:
    """Backend engine for Windows registry, color, cursor, taskbar, and API calls."""

    @staticmethod
    def refresh_shell(folder_path: str | None = None):
        if folder_path and os.path.exists(folder_path):
            ctypes.windll.shell32.SHChangeNotify(
                SHCNE_UPDATEDIR, SHCNF_PATHW, ctypes.c_wchar_p(os.path.abspath(folder_path)), None
            )
        ctypes.windll.shell32.SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, None, None)

    @staticmethod
    def broadcast_theme_change():
        res = ctypes.c_ulong()
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0,
            ctypes.c_wchar_p("ImmersiveColorSet"), SMTO_ABORTIFHUNG, 1000, ctypes.byref(res)
        )

    @staticmethod
    def set_wallpaper(image_path: str, fit_style: str | None = None):
        if not os.path.exists(image_path):
            return
        if fit_style:
            WindowsThemeEngine.set_wallpaper_fit(fit_style)
        abs_path = os.path.abspath(image_path)
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, abs_path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
        )

    @staticmethod
    def set_wallpaper_fit(style: str):
        """Sets desktop wallpaper fit style: Fill, Fit, Stretch, Tile, Center, Span."""
        styles = {
            "Fill": ("10", "0"),
            "Fit": ("6", "0"),
            "Stretch": ("2", "0"),
            "Tile": ("0", "1"),
            "Center": ("0", "0"),
            "Span": ("22", "0"),
        }
        wp_style, tile_wp = styles.get(style, ("10", "0"))
        key_path = r"Control Panel\Desktop"
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, "WallpaperStyle", 0, winreg.REG_SZ, wp_style)
                winreg.SetValueEx(key, "TileWallpaper", 0, winreg.REG_SZ, tile_wp)
        except Exception as e:
            print(f"Error setting wallpaper fit: {e}")

    @staticmethod
    def set_system_transparency(enable: bool):
        """Enables or disables Windows system & taskbar transparency in Registry."""
        val = 1 if enable else 0
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValueEx(key, "EnableTransparency", 0, winreg.REG_DWORD, val)

        adv_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, adv_path) as key:
            winreg.SetValueEx(key, "UseOLEDTaskbarTransparency", 0, winreg.REG_DWORD, val)

        WindowsThemeEngine.broadcast_theme_change()

    @staticmethod
    def apply_taskbar_composition(mode: str, hex_tint: str = "#000000", alpha: int = 120):
        """
        Applies live Win32 composition effect to the Windows Taskbar (Shell_TrayWnd).
        mode: 'Default', 'Clear', 'Blur', 'Acrylic', 'Opaque'
        """
        mode_map = {
            "Default": 0,
            "Opaque": 1,
            "Clear": 2,
            "Blur": 3,
            "Acrylic": 4,
        }
        state = mode_map.get(mode, 0)
        hex_clean = hex_tint.lstrip("#")
        if len(hex_clean) == 6:
            r = int(hex_clean[0:2], 16)
            g = int(hex_clean[2:4], 16)
            b = int(hex_clean[4:6], 16)
        else:
            r, g, b = 0, 0, 0

        a = max(0, min(255, int(alpha)))
        if mode == "Clear":
            a = 0
        abgr = (a << 24) | (b << 16) | (g << 8) | r

        policy = ACCENT_POLICY()
        policy.AccentState = state
        policy.AccentFlags = 2
        policy.GradientColor = abgr
        policy.AnimationId = 0

        data = WINDOWCOMPOSITIONATTRIBDATA()
        data.Attribute = 19  # WCA_ACCENT_POLICY
        data.Data = ctypes.pointer(policy)
        data.SizeOfData = ctypes.sizeof(policy)

        try:
            set_comp = ctypes.windll.user32.SetWindowCompositionAttribute
            for class_name in ("Shell_TrayWnd", "Shell_SecondaryTrayWnd"):
                hwnd = ctypes.windll.user32.FindWindowW(class_name, None)
                if hwnd:
                    set_comp(hwnd, ctypes.byref(data))
        except Exception as e:
            print(f"Taskbar composition error: {e}")

    @staticmethod
    def set_explorer_theme(mode: str, compact_mode: bool = False):
        """
        Controls File Explorer & System Light/Dark theme modes independently.
        mode: 'Dark', 'Light', 'Mixed (Dark System / Light Apps)'
        """
        pers_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, pers_path) as key:
            if mode == "Dark":
                winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, 0)
                winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, 0)
            elif mode == "Light":
                winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, 1)
            else:  # Mixed
                winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, 1)
                winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, 0)

        adv_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, adv_path) as key:
            winreg.SetValueEx(key, "UseCompactMode", 0, winreg.REG_DWORD, 1 if compact_mode else 0)

        WindowsThemeEngine.broadcast_theme_change()
        WindowsThemeEngine.refresh_shell()

    @staticmethod
    def restart_explorer():
        """Restarts Windows Explorer cleanly to apply deep shell & taskbar changes."""
        try:
            subprocess.run(["taskkill", "/F", "/IM", "explorer.exe"], check=False, creationflags=subprocess.CREATE_NO_WINDOW)
            time.sleep(0.6)
            subprocess.Popen(["explorer.exe"])
        except Exception as e:
            print(f"Error restarting Explorer: {e}")

    @staticmethod
    def create_cur_from_image(image_path: str, output_cur_path: str, size: int = 32, hotspot_x: int = 0, hotspot_y: int = 0) -> str:
        """
        Converts any PNG/JPG/WEBP/ICO image into a valid Windows .cur binary file
        with custom dimensions and exact Hotspot (X, Y) coordinates.
        """
        with Image.open(image_path) as raw_img:
            img = ImageOps.exif_transpose(raw_img).convert("RGBA")
            img = img.resize((size, size), Image.Resampling.LANCZOS)

        buf = io.BytesIO()
        img.save(buf, format="ICO", sizes=[(size, size)])
        ico_bytes = bytearray(buf.getvalue())

        # Modify ICONDIR header: bytes 2..4 = type 2 (Cursor)
        # Modify ICONDIRENTRY: bytes 10..12 = Hotspot X, bytes 12..14 = Hotspot Y
        if len(ico_bytes) >= 22:
            hx = max(0, min(size - 1, int(hotspot_x)))
            hy = max(0, min(size - 1, int(hotspot_y)))
            struct.pack_into("<H", ico_bytes, 2, 2)
            struct.pack_into("<HH", ico_bytes, 10, hx, hy)

        os.makedirs(os.path.dirname(os.path.abspath(output_cur_path)), exist_ok=True)
        with open(output_cur_path, "wb") as f:
            f.write(ico_bytes)
        return os.path.abspath(output_cur_path)

    @staticmethod
    def set_cursors(cursor_dict: dict):
        cursor_key = r"Control Panel\Cursors"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, cursor_key, 0, winreg.KEY_SET_VALUE) as key:
            for reg_name, path in cursor_dict.items():
                if path and os.path.exists(path):
                    winreg.SetValueEx(key, reg_name, 0, winreg.REG_EXPAND_SZ, os.path.abspath(path))
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETCURSORS, 0, None, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)

    @staticmethod
    def restore_default_cursors():
        defaults = {
            "Arrow": r"%SystemRoot%\cursors\aero_arrow.cur",
            "Hand": r"%SystemRoot%\cursors\aero_link.cur",
            "IBeam": r"",
            "AppStarting": r"%SystemRoot%\cursors\aero_working.ani",
            "Wait": r"%SystemRoot%\cursors\aero_busy.ani"
        }
        cursor_key = r"Control Panel\Cursors"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, cursor_key, 0, winreg.KEY_SET_VALUE) as key:
            for name, val in defaults.items():
                winreg.SetValueEx(key, name, 0, winreg.REG_EXPAND_SZ, val)
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETCURSORS, 0, None, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)

    @staticmethod
    def extract_top_colors(image_path: str, n: int = 5) -> list:
        img = Image.open(image_path).convert("RGB")
        img = img.resize((64, 64), Image.Resampling.LANCZOS)
        quantized = img.quantize(colors=16)
        palette = quantized.getpalette()
        if palette is None:
            return []
        color_counts = quantized.getcolors()
        if color_counts is None:
            return []
        from typing import cast

        color_counts = cast (list[tuple[int, int]], color_counts)

        candidates = []
        for count, idx in color_counts:
            
            r = palette[idx * 3]
            g = palette[idx * 3 + 1]
            b = palette[idx * 3 + 2]
            h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)

            if 0.15 < l < 0.85 and s > 0.18:
                score = count * (s ** 1.5)
                adj_l = max(0.40, min(0.60, l))
                nr, ng, nb = colorsys.hls_to_rgb(h, adj_l, max(0.50, s))
                hex_val = f"#{int(nr * 255):02X}{int(ng * 255):02X}{int(nb * 255):02X}"
                candidates.append((score, hex_val, h, s))

        candidates.sort(key=lambda x: x[0], reverse=True)
        selected = []
        for score, hex_val, h, s in candidates:
            is_too_similar = False
            for _, sel_hex, sel_h, _ in selected:
                hue_diff = abs(h - sel_h)
                if hue_diff > 0.5:
                    hue_diff = 1.0 - hue_diff
                if hue_diff < 0.08:
                    is_too_similar = True
                    break
            if not is_too_similar:
                selected.append((score, hex_val, h, s))
                if len(selected) >= n:
                    break

        result = [item[1] for item in selected]
        if not result:
            result = ["#0078D4", "#00E5FF", "#8E24AA", "#00C853", "#FFAB00"]
        while len(result) < n:
            result.append(result[0])
        return result

    @staticmethod
    def set_dark_mode(enable: bool):
        value = 0 if enable else 1
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, value)
            winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, value)
        WindowsThemeEngine.broadcast_theme_change()

    @classmethod
    def set_accent_color(cls, hex_color: str, color_taskbar: bool = True, color_borders: bool = True):
        hex_clean = hex_color.lstrip("#")
        if len(hex_clean) != 6:
            return
        r = int(hex_clean[0:2], 16)
        g = int(hex_clean[2:4], 16)
        b = int(hex_clean[4:6], 16)

        abgr_dword = (0xFF << 24) | (b << 16) | (g << 8) | r
        argb_dword = (0xC4 << 24) | (r << 16) | (g << 8) | b

        h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
        lightness_levels = [0.85, 0.75, 0.65, l, max(0.18, l * 0.8), max(0.12, l * 0.62), max(0.08, l * 0.45), 0.0]
        palette_bytes = bytearray()
        for lvl in lightness_levels:
            pr, pg, pb = colorsys.hls_to_rgb(h, min(1.0, max(0.0, lvl)), s)
            palette_bytes.extend([int(pr * 255), int(pg * 255), int(pb * 255), 0xFF])

        accent_key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Accent"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, accent_key_path) as key:
            winreg.SetValueEx(key, "AccentPalette", 0, winreg.REG_BINARY, bytes(palette_bytes))
            winreg.SetValueEx(key, "AccentColorMenu", 0, winreg.REG_DWORD, abgr_dword)
            winreg.SetValueEx(key, "StartColorMenu", 0, winreg.REG_DWORD, abgr_dword)

        dwm_key_path = r"Software\Microsoft\Windows\DWM"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, dwm_key_path) as key:
            winreg.SetValueEx(key, "AccentColor", 0, winreg.REG_DWORD, abgr_dword)
            winreg.SetValueEx(key, "ColorizationColor", 0, winreg.REG_DWORD, argb_dword)
            winreg.SetValueEx(key, "ColorizationAfterglow", 0, winreg.REG_DWORD, argb_dword)
            winreg.SetValueEx(key, "ColorPrevalence", 0, winreg.REG_DWORD, 1 if color_borders else 0)

        pers_key_path = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, pers_key_path) as key:
            if color_taskbar:
                winreg.SetValueEx(key, "SystemUsesLightTheme", 0, winreg.REG_DWORD, 0)
            winreg.SetValueEx(key, "ColorPrevalence", 0, winreg.REG_DWORD, 1 if color_taskbar else 0)

        cls.broadcast_theme_change()

    @staticmethod
    def ensure_ico(file_path: str, target_name: str) -> str:
        if file_path.lower().endswith(".ico"):
            return os.path.abspath(file_path)
        ico_out = os.path.join(BASE_APP_DIR, f"{target_name}.ico")
        img = Image.open(file_path).convert("RGBA")
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        img.save(ico_out, format="ICO", sizes=icon_sizes)
        return os.path.abspath(ico_out)

    @classmethod
    def set_clsid_icon(cls, clsid: str, file_path: str, name_tag: str, is_recycle_bin=False, auto_refresh=True):
        if not os.path.exists(file_path):
            return
        ico_path = cls.ensure_ico(file_path, name_tag)
        reg_val = f"{ico_path},0"
        key_path = fr"Software\Microsoft\Windows\CurrentVersion\Explorer\CLSID\{clsid}\DefaultIcon"

        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, reg_val)
            if is_recycle_bin:
                winreg.SetValueEx(key, "empty", 0, winreg.REG_SZ, reg_val)
                winreg.SetValueEx(key, "full", 0, winreg.REG_SZ, reg_val)
        if auto_refresh:
            cls.refresh_shell()

    @classmethod
    def set_folder_icon(cls, folder_path: str, icon_source_path: str, auto_refresh=True):
        if not os.path.exists(folder_path) or not os.path.exists(icon_source_path):
            return
        folder_abs = os.path.abspath(folder_path)
        folder_hash = hashlib.md5(folder_abs.encode("utf-8")).hexdigest()[:10]
        ico_path = cls.ensure_ico(icon_source_path, f"folder_{folder_hash}")
        ini_path = os.path.join(folder_abs, "desktop.ini")

        if os.path.exists(ini_path):
            ctypes.windll.kernel32.SetFileAttributesW(ini_path, FILE_ATTRIBUTE_NORMAL)

        ini_content = (
            "[.ShellClassInfo]\r\n"
            f"IconResource={ico_path},0\r\n"
            "[ViewState]\r\n"
            "Mode=\r\n"
            "Vid=\r\n"
            "FolderType=Generic\r\n"
        )
        with open(ini_path, "w", encoding="utf-8") as f:
            f.write(ini_content)

        ctypes.windll.kernel32.SetFileAttributesW(ini_path, FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM)
        ctypes.windll.kernel32.SetFileAttributesW(folder_abs, FILE_ATTRIBUTE_READONLY)

        if auto_refresh:
            cls.refresh_shell(folder_abs)

    @classmethod
    def reset_folder_icon(cls, folder_path: str):
        folder_abs = os.path.abspath(folder_path)
        ini_path = os.path.join(folder_abs, "desktop.ini")
        if os.path.exists(ini_path):
            ctypes.windll.kernel32.SetFileAttributesW(ini_path, FILE_ATTRIBUTE_NORMAL)
            os.remove(ini_path)
        ctypes.windll.kernel32.SetFileAttributesW(folder_abs, FILE_ATTRIBUTE_NORMAL)
        cls.refresh_shell(folder_abs)

    @classmethod
    def restore_default_icons(cls):
        defaults = {
            CLSID_THIS_PC: (r"%SystemRoot%\System32\imageres.dll,-109", False),
            CLSID_USER_FILES: (r"%SystemRoot%\System32\imageres.dll,-123", False),
            CLSID_RECYCLE_BIN: (r"%SystemRoot%\System32\imageres.dll,-55", True),
        }
        for clsid, (dll_path, is_bin) in defaults.items():
            key_path = fr"Software\Microsoft\Windows\CurrentVersion\Explorer\CLSID\{clsid}\DefaultIcon"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                winreg.SetValueEx(key, "", 0, winreg.REG_EXPAND_SZ, dll_path)
                if is_bin:
                    winreg.SetValueEx(key, "empty", 0, winreg.REG_EXPAND_SZ, r"%SystemRoot%\System32\imageres.dll,-55")
                    winreg.SetValueEx(key, "full", 0, winreg.REG_EXPAND_SZ, r"%SystemRoot%\System32\imageres.dll,-54")
        cls.refresh_shell()


class ImageManagerWidget:
    """Batch image processing logic."""
    def __init__(self, parent_frame):
        self.frame = parent_frame
        self.settings_file = os.path.join(BASE_APP_DIR, "image_manager_settings.json")

        self.src_folder = tk.StringVar()
        self.dest_folder = tk.StringVar()
        self.prefix = tk.StringVar(value="theme_img_")
        self.output_format = ctk.StringVar(value="PNG")
        self.naming_style = tk.StringVar(value="number")
        self.quality_var = tk.IntVar(value=90)

        self.subfolders_var = tk.BooleanVar(value=False)
        self.resize_var = tk.BooleanVar(value=False)
        self.crop_var = tk.BooleanVar(value=False)
        self.exif_fix_var = tk.BooleanVar(value=True)
        self.strip_meta_var = tk.BooleanVar(value=True)
        self.width_var = tk.StringVar()
        self.height_var = tk.StringVar()

        self.load_settings()
        self.create_widgets()

    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    self.src_folder.set(settings.get("src_folder", ""))
                    self.subfolders_var.set(settings.get("subfolders_var", False))
                    self.dest_folder.set(settings.get("dest_folder", ""))
                    self.prefix.set(settings.get("prefix", "theme_img_"))
                    self.output_format.set(settings.get("output_format", "PNG"))
                    self.naming_style.set(settings.get("naming_style", "number"))
                    self.quality_var.set(settings.get("quality_var", 90))
                    self.resize_var.set(settings.get("resize_var", False))
                    self.crop_var.set(settings.get("crop_var", False))
                    self.exif_fix_var.set(settings.get("exif_fix_var", True))
                    self.strip_meta_var.set(settings.get("strip_meta_var", True))
                    self.width_var.set(settings.get("width_var", ""))
                    self.height_var.set(settings.get("height_var", ""))
            except Exception as e:
                print(f"Error loading settings: {e}")

    def save_settings(self):
        settings = {
            "src_folder": self.src_folder.get(),
            "subfolders_var": self.subfolders_var.get(),
            "dest_folder": self.dest_folder.get(),
            "prefix": self.prefix.get(),
            "output_format": self.output_format.get(),
            "naming_style": self.naming_style.get(),
            "quality_var": self.quality_var.get(),
            "resize_var": self.resize_var.get(),
            "crop_var": self.crop_var.get(),
            "exif_fix_var": self.exif_fix_var.get(),
            "strip_meta_var": self.strip_meta_var.get(),
            "width_var": self.width_var.get(),
            "height_var": self.height_var.get(),
        }
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def create_widgets(self):
        self.frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.frame, text=T["batch_title"], font=ctk.CTkFont(size=22, weight="bold")).grid(
            row=0, column=0, columnspan=3, padx=30, pady=(25, 15), sticky="w"
        )

        ctk.CTkLabel(self.frame, text=f"{T['source_folder']}:").grid(row=1, column=0, sticky="w", padx=30, pady=(10, 5))
        ctk.CTkEntry(self.frame, textvariable=self.src_folder).grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(10, 5))
        ctk.CTkButton(self.frame, text=T["browse"], command=self.browse_src, width=80).grid(row=1, column=2, padx=(0, 30), pady=(10, 5))

        ctk.CTkCheckBox(self.frame, text=T["include_subfolders"], variable=self.subfolders_var).grid(
            row=2, column=1, columnspan=2, sticky="w", pady=(0, 10)
        )

        ctk.CTkLabel(self.frame, text=f"{T['destination_folder']}:").grid(row=3, column=0, sticky="w", padx=30, pady=10)
        ctk.CTkEntry(self.frame, textvariable=self.dest_folder).grid(row=3, column=1, sticky="ew", padx=(0, 10))
        ctk.CTkButton(self.frame, text=T["browse"], command=self.browse_dest, width=80).grid(row=3, column=2, padx=(0, 30))

        ctk.CTkLabel(self.frame, text=f"{T['naming_style']}:").grid(row=4, column=0, sticky="w", padx=30, pady=10)
        style_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        style_frame.grid(row=4, column=1, columnspan=2, sticky="w")
        ctk.CTkRadioButton(style_frame, text=T["prefix_number"], variable=self.naming_style, value="number").pack(side="left", padx=(0, 15))
        ctk.CTkRadioButton(style_frame, text=T["prefix_original"], variable=self.naming_style, value="original").pack(side="left")

        ctk.CTkLabel(self.frame, text=f"{T['name_prefix']}:").grid(row=5, column=0, sticky="w", padx=30, pady=10)
        ctk.CTkEntry(self.frame, textvariable=self.prefix).grid(row=5, column=1, sticky="ew", padx=(0, 10))

        ctk.CTkLabel(self.frame, text=f"{T['output_format']}:").grid(row=6, column=0, sticky="w", padx=30, pady=10)
        formats = ["PNG", "JPEG", "WEBP", "BMP", "ICO", "CUR (Cursor)"]
        self.format_dropdown = ctk.CTkComboBox(self.frame, variable=self.output_format, values=formats, command=self.on_format_change)
        self.format_dropdown.grid(row=6, column=1, sticky="w", padx=(0, 10))

        self.quality_label = ctk.CTkLabel(self.frame, text=f"{T['compression_quality']} ({self.quality_var.get()}%):", text_color="gray")
        self.quality_label.grid(row=7, column=0, sticky="w", padx=30, pady=10)

        self.quality_slider = ctk.CTkSlider(self.frame, from_=1, to=100, variable=self.quality_var, command=self.update_quality_label, state="disabled")
        self.quality_slider.grid(row=7, column=1, sticky="we", padx=(0, 10))

        ctk.CTkCheckBox(self.frame, text=T["resize_images"], variable=self.resize_var, command=self.toggle_resize).grid(
            row=8, column=0, columnspan=2, sticky="w", padx=30, pady=(15, 5)
        )

        dim_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        dim_frame.grid(row=9, column=0, columnspan=3, sticky="w", padx=30)
        ctk.CTkLabel(dim_frame, text=f"{T['width']}:").pack(side="left")
        self.width_entry = ctk.CTkEntry(dim_frame, textvariable=self.width_var, width=80, state="disabled")
        self.width_entry.pack(side="left", padx=(10, 20))

        ctk.CTkLabel(dim_frame, text=f"{T['height']}:").pack(side="left")
        self.height_entry = ctk.CTkEntry(dim_frame, textvariable=self.height_var, width=80, state="disabled")
        self.height_entry.pack(side="left", padx=(10, 10))

        self.crop_checkbox = ctk.CTkCheckBox(self.frame, text=T["center_crop"], variable=self.crop_var, state="disabled")
        self.crop_checkbox.grid(row=10, column=0, columnspan=3, sticky="w", padx=30, pady=(5, 5))

        info_text = "(Leave one empty to maintain aspect ratio. ICO/CUR formats auto-build valid Windows icons/cursors.)"
        ctk.CTkLabel(self.frame, text=T["aspect_ratio_hint"], text_color="gray", font=ctk.CTkFont(size=11)).grid(
            row=11, column=0, columnspan=3, sticky="w", padx=30, pady=(0, 10)
        )

        self.exif_checkbox = ctk.CTkCheckBox(self.frame, text=T["auto_fix_orientation"], variable=self.exif_fix_var)
        self.exif_checkbox.grid(row=12, column=0, columnspan=3, sticky="w", padx=30, pady=(10, 5))

        self.meta_checkbox = ctk.CTkCheckBox(self.frame, text=T["strip_metadata"], variable=self.strip_meta_var)
        self.meta_checkbox.grid(row=13, column=0, columnspan=3, sticky="w", padx=30, pady=(5, 10))

        self.start_button = ctk.CTkButton(
            self.frame, text=T["start_processing"], font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2FA572", hover_color="#106A43", command=self.start_processing_thread
        )
        self.start_button.grid(row=14, column=0, columnspan=3, pady=(15, 10), ipadx=20, ipady=5)

        self.progress_bar = ctk.CTkProgressBar(self.frame, width=400)
        self.progress_bar.grid(row=15, column=0, columnspan=3, pady=(10, 5))
        self.progress_bar.set(0)
        self.progress_bar.grid_remove()

        self.status_label = ctk.CTkLabel(self.frame, text=T["ready"], text_color="gray")
        self.status_label.grid(row=16, column=0, columnspan=3, pady=(0, 20))

        self.on_format_change(self.output_format.get())
        self.toggle_resize()

    def browse_src(self):
        folder = filedialog.askdirectory()
        if folder:
            self.src_folder.set(folder)

    def browse_dest(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dest_folder.set(folder)

    def toggle_resize(self):
        state = "normal" if self.resize_var.get() else "disabled"
        self.width_entry.configure(state=state)
        self.height_entry.configure(state=state)
        self.crop_checkbox.configure(state=state)

    def on_format_change(self, choice):
        if choice in ["JPEG", "WEBP"]:
            self.quality_slider.configure(state="normal")
            self.quality_label.configure(text_color=("black", "white"))
        else:
            self.quality_slider.configure(state="disabled")
            self.quality_label.configure(text_color="gray")

    def update_quality_label(self, value):
        self.quality_label.configure(text=f"{T['compression_quality']} ({int(value)}%):")

    def update_ui(self, progress_val, status_text, status_color="gray"):
        self.progress_bar.set(progress_val)
        self.status_label.configure(text=status_text, text_color=status_color)

    def finish_processing(self, success_msg=None, error_msg=None):
        self.start_button.configure(state="normal")
        self.progress_bar.grid_remove()
        self.save_settings()
        if error_msg:
            messagebox.showerror("Error", error_msg)
            self.status_label.configure(text="An error occurred.", text_color="red")
        elif success_msg:
            messagebox.showinfo("Complete", success_msg)

    def start_processing_thread(self):
        src = self.src_folder.get().strip()
        dest = self.dest_folder.get().strip()
        prefix = self.prefix.get()
        out_format = self.output_format.get()
        naming_style = self.naming_style.get()
        do_resize = self.resize_var.get()
        do_crop = self.crop_var.get()
        do_subfolders = self.subfolders_var.get()
        do_exif_fix = self.exif_fix_var.get()
        do_strip_meta = self.strip_meta_var.get()
        quality_val = self.quality_var.get()
        target_w = target_h = None

        if not src or not dest:
            messagebox.showerror("Error", "Please select both source and destination folders!")
            return

        if not os.path.isdir(src):
            messagebox.showerror("Error", "The selected source folder does not exist!")
            return

        if do_resize:
            w_str = self.width_var.get().strip()
            h_str = self.height_var.get().strip()
            if not w_str and not h_str:
                messagebox.showerror("Error", "Please enter at least width or height to resize images!")
                return
            try:
                target_w = int(w_str) if w_str else None
                target_h = int(h_str) if h_str else None
                if (target_w is not None and target_w <= 0) or (target_h is not None and target_h <= 0):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Dimensions must be integers greater than zero!")
                return

            if do_crop and (target_w is None or target_h is None):
                messagebox.showerror("Error", "Center crop strictly requires both width and height!")
                return

        os.makedirs(dest, exist_ok=True)
        self.start_button.configure(state="disabled")
        self.progress_bar.grid()
        self.progress_bar.set(0)
        self.status_label.configure(text="Finding images...", text_color="#3A7EBF")

        thread = threading.Thread(
            target=self.process_images_worker,
            args=(
                src, dest, prefix, out_format, naming_style,
                do_resize, do_crop, do_subfolders, do_exif_fix,
                do_strip_meta, target_w, target_h, quality_val,
            ),
            daemon=True,
        )
        thread.start()

    def process_images_worker(
        self, src, dest, prefix, out_format, naming_style,
        do_resize, do_crop, do_subfolders, do_exif_fix,
        do_strip_meta, target_w, target_h, quality_val
    ):
        valid_extensions = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".ico")
        files_to_process = []

        try:
            if do_subfolders:
                for root_dir, _, files in os.walk(src):
                    for f in files:
                        if f.lower().endswith(valid_extensions):
                            files_to_process.append(os.path.join(root_dir, f))
            else:
                for f in os.listdir(src):
                    if f.lower().endswith(valid_extensions):
                        full_path = os.path.join(src, f)
                        if os.path.isfile(full_path):
                            files_to_process.append(full_path)

            total_files = len(files_to_process)
            if total_files == 0:
                self.frame.after(0, self.finish_processing, None, "No supported images found in the source folder.")
                return

            ext_map = {
                "JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp",
                "BMP": ".bmp", "ICO": ".ico", "CUR (Cursor)": ".cur"
            }
            extension = ext_map.get(out_format, f".{out_format.lower()}")

            count = 1
            for i, filepath in enumerate(files_to_process):
                filename = os.path.basename(filepath)
                try:
                    if naming_style == "number":
                        base_new_name = f"{prefix}{count}"
                    else:
                        base_name = os.path.splitext(filename)[0]
                        base_new_name = f"{prefix}{base_name}"

                    new_filename = f"{base_new_name}{extension}"
                    new_filepath = os.path.join(dest, new_filename)

                    if os.path.exists(new_filepath):
                        dup_count = 1
                        while os.path.exists(new_filepath):
                            new_filename = f"{base_new_name}_{dup_count}{extension}"
                            new_filepath = os.path.join(dest, new_filename)
                            dup_count += 1

                    if out_format == "CUR (Cursor)":
                        cur_size = target_w if (do_resize and target_w) else 32
                        WindowsThemeEngine.create_cur_from_image(filepath, new_filepath, size=cur_size, hotspot_x=0, hotspot_y=0)
                        count += 1
                    else:
                        with Image.open(filepath) as img:
                            if do_exif_fix:
                                img = ImageOps.exif_transpose(img)

                            exif_data = img.info.get("exif")
                            icc_profile = img.info.get("icc_profile")

                            if out_format in ["JPEG", "BMP"] and img.mode != "RGB":
                                img = img.convert("RGB")
                            elif out_format == "ICO" and img.mode != "RGBA":
                                img = img.convert("RGBA")

                            if do_resize:
                                if do_crop and target_w is not None and target_h is not None:
                                    img = ImageOps.fit(img, (target_w, target_h), method=Image.Resampling.LANCZOS)
                                else:
                                    orig_w, orig_h = img.size
                                    final_w, final_h = target_w, target_h
                                    if target_w is not None and target_h is None:
                                        ratio = target_w / orig_w
                                        final_h = max(1, int(orig_h * ratio))
                                    elif target_h is not None and target_w is None:
                                        ratio = target_h / orig_h
                                        final_w = max(1, int(orig_w * ratio))
                                    img = img.resize((final_w, final_h), Image.Resampling.LANCZOS)

                            save_kwargs = {"format": out_format}
                            if out_format in ["JPEG", "WEBP"]:
                                save_kwargs["quality"] = quality_val
                            elif out_format == "ICO" and not do_resize:
                                save_kwargs["sizes"] = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

                            if not do_strip_meta and out_format != "ICO":
                                if exif_data:
                                    save_kwargs["exif"] = exif_data
                                if icc_profile:
                                    save_kwargs["icc_profile"] = icc_profile

                            img.save(new_filepath, **save_kwargs)
                            count += 1
                except Exception as e:
                    print(f"Error processing image {filename}: {e}")

                progress = (i + 1) / total_files
                status_text = f"Processing images: {i + 1}/{total_files} ({filename})"
                self.frame.after(0, self.update_ui, progress, status_text, "#3A7EBF")

            success_msg = f"Processing completed successfully!\nImages processed: {count - 1}"
            self.frame.after(0, self.update_ui, 1.0, f"Processing complete! {count - 1} images moved and converted.", "#2FA572")
            self.frame.after(100, self.finish_processing, success_msg, None)

        except Exception as e:
            self.frame.after(0, self.finish_processing, None, f"Critical error: {str(e)}")


class ThemeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(T["theme_title"])
        self.geometry("1160x800")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.selected_folder = None
        self.selected_folder_icon = None
        self.active_view = "theme"
        self.cursor_gen_source_path = None
        self.last_auto_applied_slot = None

        self.current_state = {
            "dark_mode": True,
            "explorer_mode": "Dark",
            "compact_explorer": False,
            "system_transparency": True,
            "taskbar_effect": "Default",
            "taskbar_alpha": 120,
            "wallpaper": None,
            "wallpaper_fit": "Fill",
            "auto_accent_from_wp": True,
            "accent_color": "#0078D4",
            "color_taskbar": True,
            "color_borders": True,
            "extracted_palette": ["#0078D4", "#00E5FF", "#8E24AA", "#00C853", "#FFAB00"],
            "cursors": {"Arrow": None, "Hand": None, "IBeam": None, "AppStarting": None},
            "system_icons": {"this_pc": None, "recycle_bin": None, "user_files": None},
            "folders": {},
            "font_family": "Segoe UI",
            "font_style": "Regular",
            "font_color": "#FFFFFF",
            "create_restore_point": True,
            "auto_day_night": False,
            "day_profile": "",
            "night_profile": "",
            "day_time": "07:00",
            "night_time": "20:00",
        }
        self.undo_state = None
        self.icon_preview_labels = {}
        self.cursor_labels = {}
        self.gallery_images = []
        self.gallery_subfolders_var = tk.BooleanVar(value=True)
        self.taskbar_keepalive_var = tk.BooleanVar(value=False)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main_views()
        self.show_view("theme")

        windnd.hook_dropfiles(self, func=self.on_drop_files)
        self.protocol("WM_DELETE_WINDOW", self.on_app_close)

        # Start background schedulers (Day/Night check & Taskbar transparency keep-alive)
        self.after(3000, self._background_scheduler_tick)
        self.after(2000, self._taskbar_keepalive_tick)

    def on_app_close(self):
        if hasattr(self, "image_manager_instance"):
            self.image_manager_instance.save_settings()
        self.destroy()

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=225, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        title = ctk.CTkLabel(self.sidebar, text="🎨 Theme Studio V.2", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(padx=20, pady=(25, 20))

        ctk.CTkButton(
            self.sidebar, 
            text=f"🎨 {T['theme_taskbar']}",
            command=lambda: self.show_view("theme")
            ).pack(padx=20, pady=6, fill="x")
        ctk.CTkButton(
            self.sidebar, 
            text=f"🖼️ {T['sidebar_gallery']}",
            command=lambda: self.show_view("gallery")
            ).pack(padx=20, pady=6, fill="x")
        ctk.CTkButton(
            self.sidebar, 
            text=f"💻 {T['sidebar_icons']}", 
            command=lambda: self.show_view("icons")
            ).pack(padx=20, pady=6, fill="x")
        ctk.CTkButton(
            self.sidebar, 
            text=f"🖱️ {T['sidebar_cursors']}", 
            command=lambda: self.show_view("cursors")
            ).pack(padx=20, pady=6, fill="x")
        ctk.CTkButton(
            self.sidebar, 
            text=f"📁 {T['sidebar_folders']}", 
            command=lambda: self.show_view("folders")
            ).pack(padx=20, pady=6, fill="x")
        ctk.CTkButton(
            self.sidebar, 
            text=f"⚙️ {T['sidebar_batch']}", 
            command=lambda: self.show_view("img_mgr")
            ).pack(padx=20, pady=6, fill="x")
        ctk.CTkButton(
            self.sidebar, 
            text=f"💾 {T['sidebar_profiles']}", 
            command=lambda: self.show_view("profiles")
        ).pack(padx=20, pady=6, fill="x")

        author_label = ctk.CTkLabel(
            self.sidebar,
            text="tommi.jalkanen@gmail.com\n© 2026 Theme Studio V.2",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        author_label.pack(side="bottom", pady=(0, 10))

        btn_reset = ctk.CTkButton(
            self.sidebar, text=T["restore_defaults"], fg_color="#8B0000", hover_color="#5A0000",
            command=self.reset_defaults
        )
        btn_reset.pack(side="bottom", padx=20, pady=(0, 15), fill="x")

    def _build_main_views(self):
        # =========================================================
        # 1. THEME, TASKBAR, EXPLORER & COLORS
        # =========================================================
        self.view_theme = ctk.CTkScrollableFrame(self, corner_radius=12)
        ctk.CTkLabel(self.view_theme,  text=T["theme_page_title"], font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=30, pady=(20, 10))

        top_switches = ctk.CTkFrame(self.view_theme, fg_color="transparent")
        top_switches.pack(fill="x", padx=30, pady=4)

        self.dark_switch = ctk.CTkSwitch(top_switches, text=T["windows_dark_mode"], command=self.toggle_dark_mode, font=ctk.CTkFont(size=14))
        self.dark_switch.select()
        self.dark_switch.pack(side="left", padx=(0, 25))

        self.trans_switch = ctk.CTkSwitch(top_switches, text=T["system_transparency"], command=self.toggle_system_transparency, font=ctk.CTkFont(size=14))
        self.trans_switch.select()
        self.trans_switch.pack(side="left")

        # --- TASKBAR TRANSPARENCY & GLASS ENGINE ---
        tb_frame = ctk.CTkFrame(self.view_theme)
        tb_frame.pack(fill="x", padx=30, pady=8)

        ctk.CTkLabel(tb_frame, text=f"🪟 {T['taskbar_glass_title']}", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=15, pady=(10, 4))
        tb_row = ctk.CTkFrame(tb_frame, fg_color="transparent")
        tb_row.pack(fill="x", padx=15, pady=(2, 10))

        ctk.CTkLabel(
            tb_row, 
            text=f"{T['effect_mode']}:"
        ) .pack(side="left", padx=(0, 8))
        self.tb_effect_var = ctk.StringVar(value="Default")
        self.tb_effect_dropdown = ctk.CTkComboBox(
            tb_row, variable=self.tb_effect_var,
            values=["Default", "Clear", "Blur", "Acrylic", "Opaque"],
            width=120, command=self.apply_taskbar_effect_ui
        )
        self.tb_effect_dropdown.pack(side="left", padx=(0, 15))

        ctk.CTkLabel(tb_row, text=f"{T['opacity']}:").pack(side="left", padx=(0, 8))
        self.tb_alpha_slider = ctk.CTkSlider(tb_row, from_=0, to=255, width=130, command=self.on_tb_alpha_change)
        self.tb_alpha_slider.set(120)
        self.tb_alpha_slider.pack(side="left", padx=(0, 12))

        ctk.CTkButton(tb_row, text=f"{T['apply_taskbar']}", width=125, command=self.apply_taskbar_effect_ui).pack(side="left", padx=(0, 12))
        ctk.CTkCheckBox(tb_row, text=T["keep_effect_active"], variable=self.taskbar_keepalive_var).pack(side="left")

        # --- FILE EXPLORER THEME MANAGER ---
        exp_frame = ctk.CTkFrame(self.view_theme)
        exp_frame.pack(fill="x", padx=30, pady=8)

        ctk.CTkLabel(exp_frame, text=f"📂 {T['explorer_title']}:", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=15, pady=(10, 4))
        exp_row = ctk.CTkFrame(exp_frame, fg_color="transparent")
        exp_row.pack(fill="x", padx=15, pady=(2, 10))

        ctk.CTkLabel(exp_row, text=f"{T['theme_mode']}:").pack(side="left", padx=(0, 8))
        self.exp_mode_var = ctk.StringVar(value="Dark")
        ctk.CTkComboBox(
            exp_row, variable=self.exp_mode_var,
            values=["Dark", "Light", "Mixed (Dark System / Light Apps)"],
            width=235, command=self.apply_explorer_theme_ui
        ).pack(side="left", padx=(0, 15))

        self.exp_compact_var = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            exp_row, text=T["compact_spacing"], variable=self.exp_compact_var,
            command=self.apply_explorer_theme_ui
        ).pack(side="left", padx=(0, 15))

        ctk.CTkButton(
            exp_row, text=f"🔄 {T['restart_explorer']}", width=155, fg_color="#444444", hover_color="#333333",
            command=WindowsThemeEngine.restart_explorer
        ).pack(side="right")

        # --- WALLPAPER & FIT STYLE ---
        wp_frame = ctk.CTkFrame(self.view_theme)
        wp_frame.pack(fill="x", padx=30, pady=8)

        ctk.CTkLabel(wp_frame, text=T["wallpaper_title"], font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=15, pady=(10, 2))
        self.wp_label = ctk.CTkLabel(wp_frame, text=T["no_file_selected"], text_color="gray")
        self.wp_label.pack(anchor="w", padx=15, pady=(0, 6))

        wp_btn_row = ctk.CTkFrame(wp_frame, fg_color="transparent")
        wp_btn_row.pack(fill="x", padx=15, pady=(0, 8))
        ctk.CTkButton(wp_btn_row, text=T["browse_wallpaper"], command=self.pick_wallpaper).pack(side="left", padx=(0, 10))

        ctk.CTkLabel(wp_btn_row, text=T["fit"] ).pack(side="left", padx=(5, 5))
        self.wp_fit_var = ctk.StringVar(value="Fill")
        ctk.CTkComboBox(
            wp_btn_row, variable=self.wp_fit_var,
            values=["Fill", "Fit", "Stretch", "Tile", "Center", "Span"],
            width=95, command=self.change_wallpaper_fit
        ).pack(side="left", padx=(0, 10))

        self.palette_container = ctk.CTkFrame(wp_btn_row, fg_color="transparent")
        self.palette_container.pack(side="left", padx=5)
        self._build_empty_palette_preview()

        self.chk_auto_wp_color = ctk.CTkCheckBox(wp_frame, text=T["auto_wallpaper_color"],)
        self.chk_auto_wp_color.select()
        self.chk_auto_wp_color.pack(anchor="w", padx=15, pady=(0, 10))

        # --- ACCENT COLOR & DEVELOPER EXPORT ---
        color_frame = ctk.CTkFrame(self.view_theme)
        color_frame.pack(fill="x", padx=30, pady=8)

        ctk.CTkLabel(color_frame, text=f"🎨 {T['accent_title']}", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=15, pady=(10, 6))
        picker_row = ctk.CTkFrame(color_frame, fg_color="transparent")
        picker_row.pack(fill="x", padx=15, pady=4)

        self.color_swatch = ctk.CTkFrame(picker_row, width=42, height=36, corner_radius=6, fg_color="#0078D4", border_width=2, border_color="white")
        self.color_swatch.pack(side="left", padx=(0, 12))
        self.lbl_hex_color = ctk.CTkLabel(picker_row, text="#0078D4", font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), width=80, anchor="w")
        self.lbl_hex_color.pack(side="left", padx=(0, 10))

        self.hex_entry = ctk.CTkEntry(picker_row, width=100)
        self.hex_entry.pack(side="left", padx=(0, 8))
        self.hex_entry.insert(0, "#0078D4")
        self.hex_entry.bind("<Return>", lambda event: self.apply_hex_color())

        ctk.CTkButton(picker_row, text=T["apply"], width=65, command=self.apply_hex_color).pack(side="left", padx=(0, 8))
        ctk.CTkButton(picker_row, text=f"🎨 {T['pick_color']}", width=125, command=self.open_color_picker).pack(side="left", padx=(0, 10))

        for hex_val in ["#0078D4", "#00E5FF", "#8E24AA", "#00C853", "#FFAB00"]:
            ctk.CTkButton(
                picker_row, text="", width=26, height=26, corner_radius=13,
                fg_color=hex_val, hover_color=hex_val,
                command=lambda h=hex_val: self.apply_selected_color(h)
            ).pack(side="left", padx=2)

        ctk.CTkButton(
            picker_row, text="📤 Export CSS / Tailwind", width=165, fg_color="#2FA572", hover_color="#106A43",
            command=self.open_export_code_modal
        ).pack(side="right", padx=(5, 0))

        opts_row = ctk.CTkFrame(color_frame, fg_color="transparent")
        opts_row.pack(fill="x", padx=15, pady=(8, 12))
        self.chk_taskbar = ctk.CTkCheckBox(opts_row, text=T["colorize_taskbar"], command=self.refresh_accent_options)
        self.chk_taskbar.select()
        self.chk_taskbar.pack(side="left", padx=(0, 25))
        self.chk_borders = ctk.CTkCheckBox(opts_row, text=T["colorize_borders"], command=self.refresh_accent_options)
        self.chk_borders.select()
        self.chk_borders.pack(side="left")

        # --- FONT & LIVE PREVIEW ---
        font_frame = ctk.CTkFrame(self.view_theme)
        font_frame.pack(fill="x", padx=30, pady=8)

        ctk.CTkLabel(font_frame, text=T["font_preview_title"], font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=15, pady=(10, 6))
        font_row = ctk.CTkFrame(font_frame, fg_color="transparent")
        font_row.pack(fill="x", padx=15, pady=4)

        ctk.CTkLabel(font_row, text=f"{T['font']}:").pack(side="left", padx=(0, 10))
        available_fonts = list(tkfont.families())
        safe_fonts = [f for f in available_fonts if not f.startswith('@')]
        self.font_var = ctk.StringVar(value="Segoe UI")
        self.font_dropdown = ctk.CTkComboBox(font_row, variable=self.font_var, values=sorted(safe_fonts), command=self.apply_font)
        self.font_dropdown.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(font_row, text=f"{T['style']}:").pack(side="left", padx=(0, 10))
        self.font_style_var = ctk.StringVar(value="Regular")
        self.font_style_dropdown = ctk.CTkComboBox(
            font_row, variable=self.font_style_var,
            values=["Regular", "Bold", "Italic", "Bold Italic"],
            width=120, command=self.apply_font_style
        )
        self.font_style_dropdown.pack(side="left", padx=(0, 20))

        ctk.CTkLabel(font_row, text=f"{T['color']}:").pack(side="left", padx=(0, 10))
        
        self.font_color_swatch = ctk.CTkFrame(font_row, width=24, height=24, corner_radius=12, fg_color="#FFFFFF", border_width=1, border_color="gray")
        self.font_color_swatch.pack(side="left", padx=(0, 5))
        
        # UUSI: Tekstikenttä fontin HEX-koodille
        self.font_hex_entry = ctk.CTkEntry(font_row, width=80)
        self.font_hex_entry.pack(side="left", padx=(5, 10))
        self.font_hex_entry.insert(0, "#FFFFFF")
        self.font_hex_entry.bind("<Return>", lambda event: self.apply_font_hex_color())
        
        ctk.CTkButton(font_row, text=T["change_color"], width=100, command=self.open_font_color_picker).pack(side="left")

        self.lbl_demo_text = ctk.CTkLabel(font_frame, text=T["sample_text"], font=ctk.CTkFont(family="Segoe UI", size=14), text_color="#FFFFFF")
        self.lbl_demo_text.pack(anchor="w", padx=15, pady=(8, 8))

        undo_restore_row = ctk.CTkFrame(font_frame, fg_color="transparent")
        undo_restore_row.pack(fill="x", padx=15, pady=(0, 10))

        ctk.CTkButton(undo_restore_row, text=f"↶ {T['undo_last_change']}", width=150, command=self.undo_last_change).pack(side="left", padx=(0, 20))

        self.create_restore_point_var = ctk.BooleanVar(value=True)
        self.restore_checkbox = ctk.CTkCheckBox(
            undo_restore_row, text=T["restore_point_before_changes"],
            variable=self.create_restore_point_var, command=self.toggle_restore_points
        )
        self.restore_checkbox.pack(side="left", padx=(0, 15))

        self.restore_status = ctk.CTkLabel(undo_restore_row, text=T["restore_point_ready"], text_color="gray")
        self.restore_status.pack(side="left")

        # Live Preview Card
        self.preview_frame = ctk.CTkFrame(font_frame)
        self.preview_frame.pack(fill="x", padx=15, pady=(5, 15))

        self.preview_titlebar = ctk.CTkFrame(self.preview_frame, height=32, fg_color=self.current_state["accent_color"], corner_radius=6)
        self.preview_titlebar.pack(fill="x", padx=4, pady=(4, 10))

        self.preview_window_text = ctk.CTkLabel(self.preview_titlebar, text=T["preview_window_title"], text_color="white", font=ctk.CTkFont(weight="bold"))
        self.preview_window_text.pack(side="left", padx=12, pady=4)

        self.preview_window_buttons = ctk.CTkLabel(self.preview_titlebar, text="─   □   ✕", text_color="white")
        self.preview_window_buttons.pack(side="right", padx=12, pady=4)

        self.preview_title = ctk.CTkLabel(self.preview_frame, text=T["preview_title"], font=ctk.CTkFont(size=18, weight="bold"))
        self.preview_title.pack(anchor="w", padx=15, pady=(4, 2))

        self.preview_subtext = ctk.CTkLabel(self.preview_frame, text=T["preview_subtext"], text_color="gray")
        self.preview_subtext.pack(anchor="w", padx=15, pady=(0, 6))

        self.preview_body = ctk.CTkLabel(self.preview_frame, text=T["preview_body"])
        self.preview_body.pack(anchor="w", padx=15, pady=(0, 8))

        self.preview_accent = ctk.CTkFrame(self.preview_frame, height=8, fg_color=self.current_state["accent_color"], corner_radius=4)
        self.preview_accent.pack(fill="x", padx=15, pady=(0, 10))

        self.preview_entry = ctk.CTkEntry(self.preview_frame, placeholder_text=T["preview_textbox"])
        self.preview_entry.pack(fill="x", padx=15, pady=(0, 10))

        preview_actions = ctk.CTkFrame(self.preview_frame, fg_color="transparent")
        preview_actions.pack(fill="x", padx=15, pady=(0, 12))

        self.preview_checkbox = ctk.CTkCheckBox(preview_actions, text=T["preview_checkbox"])
        self.preview_checkbox.select()
        self.preview_checkbox.pack(side="left", padx=(0, 20))

        self.preview_button = ctk.CTkButton(preview_actions, text=T["preview_accent_button"], width=130, fg_color=self.current_state["accent_color"])
        self.preview_button.pack(side="left", padx=(0, 10))

        self.preview_secondary_button = ctk.CTkButton(preview_actions, text=T["preview_secondary_button"], width=130, fg_color="gray35")
        self.preview_secondary_button.pack(side="left")

        # =========================================================
        # 2. IMAGE GALLERY
        # =========================================================
        self.view_gallery = ctk.CTkScrollableFrame(self, corner_radius=12)
        ctk.CTkLabel(self.view_gallery, text=T["gallery_title"], font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=30, pady=(25, 5))

        self.lbl_gallery_dir = ctk.CTkLabel(self.view_gallery, text=f"{T['current_folder']}: {GALLERY_DIR}", text_color="gray")
        self.lbl_gallery_dir.pack(anchor="w", padx=30, pady=(0, 12))

        gal_controls = ctk.CTkFrame(self.view_gallery, fg_color="transparent")
        gal_controls.pack(fill="x", padx=30, pady=(0, 10))

        ctk.CTkButton(gal_controls, text=f"📁 {T['change_folder']}", command=self.change_gallery_dir).pack(side="left", padx=(0, 10))
        ctk.CTkButton(gal_controls, text=f"🔄 {T['refresh_gallery']}", command=self.load_gallery_images).pack(side="left", padx=(0, 10))
        ctk.CTkButton(
            gal_controls, text=f"⚙️ {T['send_to_batch']}", fg_color="#2FA572", hover_color="#106A43",
            command=self.send_gallery_to_batch
        ).pack(side="left", padx=(0, 15))
        ctk.CTkCheckBox(
            gal_controls, text=T["include_subfolders"], variable=self.gallery_subfolders_var, command=self.load_gallery_images
        ).pack(side="left")

        self.gallery_status_lbl = ctk.CTkLabel(self.view_gallery, text="", text_color="gray")
        self.gallery_status_lbl.pack(anchor="w", padx=30, pady=(0, 5))

        self.gallery_grid = ctk.CTkFrame(self.view_gallery, fg_color="transparent")
        self.gallery_grid.pack(fill="both", expand=True, padx=25, pady=10)
        for c in range(3):
            self.gallery_grid.grid_columnconfigure(c, weight=1)

        # =========================================================
        # 3. SYSTEM ICONS & ICON PACK (.ZIP)
        # =========================================================
        self.view_icons = ctk.CTkFrame(self, corner_radius=12)
        ctk.CTkLabel(self.view_icons, text=T["icons_title"], font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=30, pady=(25, 5))
        ctk.CTkLabel(self.view_icons, text=T["icons_description"], text_color="gray").pack(anchor="w", padx=30, pady=(0, 15))

        icon_pack_bar = ctk.CTkFrame(self.view_icons)
        icon_pack_bar.pack(fill="x", padx=30, pady=(0, 15))
        ctk.CTkLabel(icon_pack_bar, text=f"📦 {T['icon_pack']}:", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=15, pady=12)
        ctk.CTkButton(icon_pack_bar, text=f"📤 {T['import_icon_pack']}", fg_color="#2FA572", hover_color="#106A43", command=self.import_icon_pack_zip).pack(side="left", padx=8, pady=12)
        ctk.CTkButton(icon_pack_bar, text=f"💾 {T['export_icon_pack']}", command=self.export_icon_pack_zip).pack(side="left", padx=8, pady=12)

        self._create_icon_row(self.view_icons, f"💻 {T['this_pc']}", CLSID_THIS_PC, "this_pc", False)

        self._create_icon_row(self.view_icons, f"🗑️ {T['recycle_bin']}", CLSID_RECYCLE_BIN, "recycle_bin", True)

        self._create_icon_row(self.view_icons, f"📁 {T['user_files']}", CLSID_USER_FILES, "user_files", False)

        # =========================================================
        # 4. MOUSE POINTERS, CURSOR PACK (.ZIP) & IMAGE-TO-CURSOR CREATOR
        # =========================================================
        self.view_cursors = ctk.CTkScrollableFrame(self, corner_radius=12)
        ctk.CTkLabel(self.view_cursors, text=T["cursor_title"], font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=30, pady=(20, 5))
        ctk.CTkLabel(self.view_cursors, text=T["cursor_description"], text_color="gray").pack(anchor="w", padx=30, pady=(0, 12))

        cur_pack_bar = ctk.CTkFrame(self.view_cursors)
        cur_pack_bar.pack(fill="x", padx=30, pady=(0, 12))
        ctk.CTkLabel(cur_pack_bar, text=f"📦 {T['cursor_pack']}:", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=15, pady=12)
        ctk.CTkButton(cur_pack_bar, text=f"📥 {T['import_cursor_pack']}", fg_color="#2FA572", hover_color="#106A43", command=self.import_cursor_pack_zip).pack(side="left", padx=8, pady=12)
        ctk.CTkButton(cur_pack_bar, text=f"💾 {T['export_cursor_pack']}", command=self.export_cursor_pack_zip).pack(side="left", padx=8, pady=12)

        self._create_cursor_row(self.view_cursors, f"🖱️ {T['cursor_normal']}", "Arrow")
        self._create_cursor_row(self.view_cursors, f"🔗 {T['cursor_link']}", "Hand")
        self._create_cursor_row(self.view_cursors, f"📝 {T['cursor_text']}", "IBeam")
        self._create_cursor_row(self.view_cursors, f"⏳ {T['cursor_working']}", "AppStarting")

        # --- CURSOR CREATOR FROM IMAGE ---
        gen_frame = ctk.CTkFrame(self.view_cursors)
        gen_frame.pack(fill="x", padx=30, pady=(18, 20))

        ctk.CTkLabel(gen_frame, text=f"✨ {T['cursor_creator_title']}", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=15, pady=(12, 4))
        ctk.CTkLabel(gen_frame, text=T["cursor_creator_description"], text_color="gray", font=ctk.CTkFont(size=12)).pack(anchor="w", padx=15, pady=(0, 10))

        gen_top = ctk.CTkFrame(gen_frame, fg_color="transparent")
        gen_top.pack(fill="x", padx=15, pady=5)

        ctk.CTkButton(gen_top, text=f"🖼️ {T['select_source_image']}", command=self.pick_cursor_gen_image).pack(side="left", padx=(0, 12))
        self.lbl_cur_gen_src = ctk.CTkLabel(gen_top, text=T["no_image_selected"], text_color="gray")
        self.lbl_cur_gen_src.pack(side="left", padx=(0, 15))
        self.cur_gen_preview_lbl = ctk.CTkLabel(gen_top, text="")
        self.cur_gen_preview_lbl.pack(side="right", padx=15)

        gen_opts = ctk.CTkFrame(gen_frame, fg_color="transparent")
        gen_opts.pack(fill="x", padx=15, pady=8)

        ctk.CTkLabel(gen_opts, text=f"{T['target_role']}:").pack(side="left", padx=(0, 6))
        self.cur_gen_role_var = ctk.StringVar(value="Arrow")
        ctk.CTkComboBox(gen_opts, variable=self.cur_gen_role_var, values=["Arrow", "Hand", "IBeam", "AppStarting"], width=120).pack(side="left", padx=(0, 15))

        ctk.CTkLabel(gen_opts, text=f"{T['cursor_size']}:").pack(side="left", padx=(0, 6))
        self.cur_gen_size_var = ctk.StringVar(value="32")
        ctk.CTkComboBox(gen_opts, variable=self.cur_gen_size_var, values=["32", "48", "64"], width=75, command=lambda _: self._update_cursor_gen_preview()).pack(side="left", padx=(0, 15))

        ctk.CTkLabel(gen_opts, text=f"{T['hotspot_x']}:").pack(side="left", padx=(0, 6))
        self.cur_gen_hx_var = tk.IntVar(value=0)
        self.cur_hx_slider = ctk.CTkSlider(gen_opts, from_=0, to=63, width=100, variable=self.cur_gen_hx_var, command=lambda _: self._update_cursor_gen_preview())
        self.cur_hx_slider.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(gen_opts, text=f"{T['hotspot_y']}:").pack(side="left", padx=(0, 6))
        self.cur_gen_hy_var = tk.IntVar(value=0)
        self.cur_hy_slider = ctk.CTkSlider(gen_opts, from_=0, to=63, width=100, variable=self.cur_gen_hy_var, command=lambda _: self._update_cursor_gen_preview())
        self.cur_hy_slider.pack(side="left", padx=(0, 10))

        self.lbl_hotspot_coords = ctk.CTkLabel(gen_opts, text="(0, 0)", font=ctk.CTkFont(family="Consolas", size=12))
        self.lbl_hotspot_coords.pack(side="left", padx=5)

        gen_actions = ctk.CTkFrame(gen_frame, fg_color="transparent")
        gen_actions.pack(fill="x", padx=15, pady=(6, 15))

        ctk.CTkButton(
            gen_actions, text=f"⚡ {T['generate_cursor']}", fg_color="#2FA572", hover_color="#106A43",
            command=lambda: self.generate_cursor_from_image(apply_now=True)
        ).pack(side="left", padx=(0, 12))
        ctk.CTkButton(
            gen_actions, text=f"💾 {T['save_cursor_as']}", fg_color="#444444", hover_color="#333333",
            command=lambda: self.generate_cursor_from_image(apply_now=False)
        ).pack(side="left")

        # =========================================================
        # 5. FOLDER ICONS
        # =========================================================
        self.view_folders = ctk.CTkFrame(self, corner_radius=12)
        ctk.CTkLabel(self.view_folders, text=T["folder_title"], font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=30, pady=(25, 5))
        ctk.CTkLabel(self.view_folders, text=T["folder_description"], text_color="gray").pack(anchor="w", padx=30, pady=(0, 15))

        self.drop_zone = ctk.CTkFrame(self.view_folders, height=130, border_width=2, border_color="#3B8ED0")
        self.drop_zone.pack(fill="x", padx=30, pady=10)
        self.drop_zone.pack_propagate(False)

        self.drop_label = ctk.CTkLabel(self.drop_zone, text=f"📁 {T['folder_dropzone']}", font=ctk.CTkFont(size=16, weight="bold"), text_color="#3B8ED0")
        self.drop_label.place(relx=0.5, rely=0.5, anchor="center")

        status_frame = ctk.CTkFrame(self.view_folders)
        status_frame.pack(fill="x", padx=30, pady=10)

        f_row = ctk.CTkFrame(status_frame, fg_color="transparent")
        f_row.pack(fill="x", padx=15, pady=(12, 6))
        ctk.CTkLabel(f_row, text=f"{T['target_folder']}:", font=ctk.CTkFont(weight="bold"), width=110, anchor="w").pack(side="left")
        self.lbl_folder_path = ctk.CTkLabel(f_row, text=T["not_selected"], text_color="gray", anchor="w")
        self.lbl_folder_path.pack(side="left", fill="x", expand=True, padx=10)
        ctk.CTkButton(f_row, text=T["browse_folder"], width=120, command=self.browse_folder).pack(side="right")

        i_row = ctk.CTkFrame(status_frame, fg_color="transparent")
        i_row.pack(fill="x", padx=15, pady=(6, 12))
        ctk.CTkLabel(i_row, text=f"{T['new_icon']}:", font=ctk.CTkFont(weight="bold"), width=110, anchor="w").pack(side="left")
        self.lbl_folder_icon = ctk.CTkLabel(i_row, text=T["not_selected"], text_color="gray", anchor="w")
        self.lbl_folder_icon.pack(side="left", fill="x", expand=True, padx=10)
        self.folder_icon_preview = ctk.CTkLabel(i_row, text="")
        self.folder_icon_preview.pack(side="left", padx=10)
        ctk.CTkButton(i_row, text=T["browse_image"], width=120, command=self.browse_folder_icon).pack(side="right")

        action_row = ctk.CTkFrame(self.view_folders, fg_color="transparent")
        action_row.pack(fill="x", padx=30, pady=15)
        ctk.CTkButton(action_row, text=f"✨ {T['set_folder_icon']}", height=40, font=ctk.CTkFont(size=14, weight="bold"), command=self.apply_folder_icon).pack(side="left", expand=True, fill="x", padx=(0, 10))
        ctk.CTkButton(action_row, text=T["restore_folder_icon"], height=40, fg_color="#444444", hover_color="#333333", command=self.clear_folder_icon).pack(side="right", padx=(10, 0))

        # =========================================================
        # 6. BATCH IMAGE MANAGEMENT
        # =========================================================
        self.view_img_mgr = ctk.CTkScrollableFrame(self, corner_radius=12)
        self.image_manager_instance = ImageManagerWidget(self.view_img_mgr)

        # =========================================================
        # 7. THEME PROFILES, FULL ZIP PACKS & AUTO DAY/NIGHT SCHEDULER
        # =========================================================

        self.view_profiles = ctk.CTkScrollableFrame(self, corner_radius=12)
        ctk.CTkLabel(self.view_profiles, text=T["profiles_main_title"], font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=30, pady=(20, 5))

        save_box = ctk.CTkFrame(self.view_profiles)
        save_box.pack(fill="x", padx=30, pady=5)
        self.entry_profile_name = ctk.CTkEntry(save_box, placeholder_text=T["enter_profile_name"], height=36)
        self.entry_profile_name.pack(side="left", fill="x", expand=True, padx=(15, 10), pady=12)
        ctk.CTkButton(save_box, text=f"💾 {T['save_profile']}", height=36, command=self.save_current_profile).pack(side="left", padx=(0, 8), pady=12)
        ctk.CTkButton(save_box, text=f"📂 {T['import_json']}", width=110, height=36, fg_color="#444444", hover_color="#333333", command=self.import_external_profile).pack(side="left", padx=(0, 8), pady=12)
        ctk.CTkButton(save_box, text=f"📦 {T['export_theme_zip']}", width=145, height=36, fg_color="#2FA572", hover_color="#106A43", command=self.export_full_theme_pack_zip).pack(side="left", padx=(0, 8), pady=12)
        ctk.CTkButton(save_box, text=f"📥 {T['import_theme_zip']}", width=145, height=36, command=self.import_full_theme_pack_zip).pack(side="right", padx=(0, 15), pady=12)

        # --- AUTO DAY / NIGHT SCHEDULER ---
        sched_frame = ctk.CTkFrame(self.view_profiles)
        sched_frame.pack(fill="x", padx=30, pady=10)

        sched_top = ctk.CTkFrame(sched_frame, fg_color="transparent")
        sched_top.pack(fill="x", padx=15, pady=(10, 4))

        ctk.CTkLabel(sched_top, text=f"🌗 {T['auto_day_night_title']}", font=ctk.CTkFont(size=15, weight="bold")).pack(side="left")
        self.auto_dn_var = tk.BooleanVar(value=False)
        ctk.CTkSwitch(
            sched_top, text=T["enable_auto_schedule"], variable=self.auto_dn_var,
            command=self.on_toggle_day_night_schedule
        ).pack(side="right")

        sched_row = ctk.CTkFrame(sched_frame, fg_color="transparent")
        sched_row.pack(fill="x", padx=15, pady=(4, 12))

        ctk.CTkLabel(sched_row, text=f"☀️ {T['day_profile']}").pack(side="left", padx=(0, 6))
        self.day_prof_var = ctk.StringVar(value="")
        self.day_prof_combo = ctk.CTkComboBox(sched_row, variable=self.day_prof_var, values=[""], width=150)
        self.day_prof_combo.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(sched_row, text=T["start_time"]).pack(side="left", padx=(0, 6))
        self.day_time_entry = ctk.CTkEntry(sched_row, width=65)
        self.day_time_entry.pack(side="left", padx=(0, 20))
        self.day_time_entry.insert(0, "07:00")

        ctk.CTkLabel(sched_row, text=f"🌙 {T['night_profile']}").pack(side="left", padx=(0, 6))
        self.night_prof_var = ctk.StringVar(value="")
        self.night_prof_combo = ctk.CTkComboBox(sched_row, variable=self.night_prof_var, values=[""], width=150)
        self.night_prof_combo.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(sched_row, text=T["start_time"]).pack(side="left", padx=(0, 6))
        self.night_time_entry = ctk.CTkEntry(sched_row, width=65)
        self.night_time_entry.pack(side="left", padx=(0, 12))
        self.night_time_entry.insert(0, "20:00")

        self.sched_status_lbl = ctk.CTkLabel(sched_frame, text=T["scheduler_status_inactive"], text_color="gray", font=ctk.CTkFont(size=12))
        self.sched_status_lbl.pack(anchor="w", padx=15, pady=(0, 10))

        ctk.CTkLabel(self.view_profiles, text=T["saved_profiles"], font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=30, pady=(10, 5))
        self.profiles_list_frame = ctk.CTkScrollableFrame(self.view_profiles, height=280)
        self.profiles_list_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

    def _create_icon_row(self, parent, title, clsid, tag, is_bin):
        row = ctk.CTkFrame(parent)
        row.pack(fill="x", padx=30, pady=8)
        ctk.CTkLabel(row, text=title, font=ctk.CTkFont(size=15, weight="bold"), width=180, anchor="w").pack(side="left", padx=15, pady=15)
        preview_lbl = ctk.CTkLabel(row, text=T["default_current"], text_color="gray")
        preview_lbl.pack(side="left", padx=10)
        self.icon_preview_labels[tag] = preview_lbl
        ctk.CTkButton(row, text=T["change_icon"], width=140, command=lambda: self.pick_icon(clsid, tag, is_bin, preview_lbl)).pack(side="right", padx=15, pady=15)

    def _create_cursor_row(self, parent, title, cursor_key):
        row = ctk.CTkFrame(parent)
        row.pack(fill="x", padx=30, pady=6)
        ctk.CTkLabel(row, text=title, font=ctk.CTkFont(size=15, weight="bold"), width=250, anchor="w").pack(side="left", padx=15, pady=12)
        lbl_path = ctk.CTkLabel(row, text=T["default_cursor"], text_color="gray", anchor="w")
        lbl_path.pack(side="left", fill="x", expand=True, padx=10)
        self.cursor_labels[cursor_key] = lbl_path
        ctk.CTkButton(row, text=T["select_cursor"], width=150, command=lambda: self.pick_cursor_file(cursor_key, lbl_path)).pack(side="right", padx=15, pady=12)

    def show_view(self, name: str):
        self.active_view = name
        for v in (self.view_theme, self.view_gallery, self.view_icons, self.view_cursors, self.view_folders, self.view_img_mgr, self.view_profiles):
            v.grid_forget()
        if name == "theme":
            self.view_theme.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif name == "gallery":
            self.load_gallery_images()
            self.view_gallery.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif name == "icons":
            self.view_icons.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif name == "cursors":
            self.view_cursors.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif name == "folders":
            self.view_folders.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif name == "img_mgr":
            self.view_img_mgr.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        elif name == "profiles":
            self.refresh_profiles_list()
            self.view_profiles.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    # =========================================================
    # TASKBAR TRANSPARENCY & EXPLORER THEME HANDLERS
    # =========================================================
    def toggle_system_transparency(self):
        enabled = bool(self.trans_switch.get())
        self.current_state["system_transparency"] = enabled
        WindowsThemeEngine.set_system_transparency(enabled)

    def on_tb_alpha_change(self, val):
        self.current_state["taskbar_alpha"] = int(val)
        if self.tb_effect_var.get() != "Default":
            self.apply_taskbar_effect_ui()

    def apply_taskbar_effect_ui(self, choice=None):
        mode = self.tb_effect_var.get()
        alpha = int(self.tb_alpha_slider.get())
        self.current_state["taskbar_effect"] = mode
        self.current_state["taskbar_alpha"] = alpha
        WindowsThemeEngine.apply_taskbar_composition(mode, self.current_state["accent_color"], alpha)

    def _taskbar_keepalive_tick(self):
        if self.taskbar_keepalive_var.get() and self.current_state.get("taskbar_effect", "Default") != "Default":
            WindowsThemeEngine.apply_taskbar_composition(
                self.current_state["taskbar_effect"],
                self.current_state["accent_color"],
                self.current_state.get("taskbar_alpha", 120)
            )
        self.after(2500, self._taskbar_keepalive_tick)

    def apply_explorer_theme_ui(self, choice=None):
        mode = self.exp_mode_var.get()
        compact = bool(self.exp_compact_var.get())
        self.current_state["explorer_mode"] = mode
        self.current_state["compact_explorer"] = compact

        if mode == "Dark":
            self.dark_switch.select()
            self.current_state["dark_mode"] = True
        elif mode == "Light":
            self.dark_switch.deselect()
            self.current_state["dark_mode"] = False

        WindowsThemeEngine.set_explorer_theme(mode, compact)

    def change_wallpaper_fit(self, choice=None):
        fit = self.wp_fit_var.get()
        self.current_state["wallpaper_fit"] = fit
        WindowsThemeEngine.set_wallpaper_fit(fit)
        if self.current_state.get("wallpaper") and os.path.exists(self.current_state["wallpaper"]):
            WindowsThemeEngine.set_wallpaper(self.current_state["wallpaper"], fit)

    # =========================================================
    # DEVELOPER EXPORT (CSS / TAILWIND / JSON MODAL)
    # =========================================================
    def open_export_code_modal(self):
        win = ctk.CTkToplevel(self)
        win.title("Export Theme Palette & Typography (CSS / Tailwind / JSON)")
        win.geometry("680x520")
        win.attributes("-topmost", True)

        accent = self.current_state.get("accent_color", "#0078D4")
        palette = self.current_state.get("extracted_palette") or [accent, "#00E5FF", "#8E24AA", "#00C853", "#FFAB00"]
        font_fam = self.current_state.get("font_family", "Segoe UI")
        font_col = self.current_state.get("font_color", "#FFFFFF")

        css_code = (
            ":root {\n"
            f"  --theme-accent: {accent};\n"
            f"  --theme-text-color: {font_col};\n"
            f"  --theme-font-family: '{font_fam}', sans-serif;\n"
            + "".join(f"  --theme-palette-{i+1}: {c};\n" for i, c in enumerate(palette))
            + "}\n"
        )

        tw_code = (
            "// tailwind.config.js\n"
            "module.exports = {\n"
            "  theme: {\n"
            "    extend: {\n"
            "      colors: {\n"
            f"        accent: '{accent}',\n"
            f"        themeText: '{font_col}',\n"
            "        palette: {\n"
            + "".join(f"          {i+1}00: '{c}',\n" for i, c in enumerate(palette))
            + "        }\n"
            "      },\n"
            "      fontFamily: {\n"
            f"        theme: ['{font_fam}', 'sans-serif'],\n"
            "      }\n"
            "    }\n"
            "  }\n"
            "};\n"
        )

        combined = f"/* === CSS VARIABLES === */\n{css_code}\n/* === TAILWIND CONFIG === */\n{tw_code}"

        ctk.CTkLabel(win, text="Generated CSS Variables & Tailwind Configuration:", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=20, pady=(15, 8))

        textbox = ctk.CTkTextbox(win, font=ctk.CTkFont(family="Consolas", size=13), height=360)
        textbox.pack(fill="both", expand=True, padx=20, pady=5)
        textbox.insert("1.0", combined)

        btn_bar = ctk.CTkFrame(win, fg_color="transparent")
        btn_bar.pack(fill="x", padx=20, pady=15)

        def copy_clip():
            self.clipboard_clear()
            self.clipboard_append(textbox.get("1.0", "end-1c"))
            messagebox.showinfo("Copied", "CSS & Tailwind config copied to clipboard!", parent=win)

        def save_file():
            p = filedialog.asksaveasfilename(defaultextension=".css", filetypes=[("CSS File", "*.css"), ("JS File", "*.js"), ("Text File", "*.txt")], parent=win)
            if p:
                with open(p, "w", encoding="utf-8") as f:
                    f.write(textbox.get("1.0", "end-1c"))
                messagebox.showinfo("Saved", f"Saved to {p}", parent=win)

        ctk.CTkButton(btn_bar, text="📋 Copy to Clipboard", fg_color="#2FA572", hover_color="#106A43", command=copy_clip).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_bar, text="💾 Save to File...", command=save_file).pack(side="left")
        ctk.CTkButton(btn_bar, text="Close", fg_color="#444444", command=win.destroy).pack(side="right")

    # =========================================================
    # FONTS & COLORS
    # =========================================================
    def apply_font_hex_color(self):
        hex_color = self.font_hex_entry.get().strip().upper()
        if not hex_color.startswith("#"):
            hex_color = "#" + hex_color

        if len(hex_color) != 7:
            messagebox.showerror("Invalid HEX", "HEX color must be in format #RRGGBB")
            return

        try:
            int(hex_color[1:], 16)
        except ValueError:
            messagebox.showerror("Invalid HEX", "HEX color is not valid.")
            return

        self.current_state["font_color"] = hex_color
        self.font_color_swatch.configure(fg_color=hex_color)
        self.update_demo_text()
    
    def apply_font(self, choice=None):
        font_name = self.font_var.get()
        self.current_state["font_family"] = font_name
        self.update_demo_text()

    def apply_font_style(self, choice=None):
        self.current_state["font_style"] = self.font_style_var.get()
        self.update_demo_text()

    def open_font_color_picker(self):
        color = colorchooser.askcolor(initialcolor=self.current_state["font_color"], title="Select Font Color")
        if color and color[1]:
            hex_upper = color[1].upper()
            self.current_state["font_color"] = hex_upper
            self.font_color_swatch.configure(fg_color=hex_upper)
            
            # Päivitetään myös tekstikenttä
            if hasattr(self, 'font_hex_entry'):
                self.font_hex_entry.delete(0, "end")
                self.font_hex_entry.insert(0, hex_upper)
                
            self.update_demo_text()
          
    def apply_font_hex_color(self):
        hex_color = self.font_hex_entry.get().strip().upper()
        if not hex_color.startswith("#"):
            hex_color = "#" + hex_color

        if len(hex_color) != 7:
            messagebox.showerror("Invalid HEX", "HEX color must be in format #RRGGBB")
            return

        try:
            int(hex_color[1:], 16)
        except ValueError:
            messagebox.showerror("Invalid HEX", "HEX color is not valid.")
            return

        self.current_state["font_color"] = hex_color
        self.font_color_swatch.configure(fg_color=hex_color)
        self.update_demo_text()      
            
            # Päivitetään myös tekstikenttä
        if hasattr(self, 'font_hex_entry'):
            self.font_hex_entry.delete(0, "end")
            self.font_hex_entry.insert(0, hex_upper)
                
            self.update_demo_text()

    def update_demo_text(self):
        f_family = self.current_state.get("font_family", "Segoe UI")
        f_color = self.current_state.get("font_color", "#FFFFFF")
        f_style = self.current_state.get("font_style", "Regular")

        weight = "normal"
        slant = "roman"

        if f_style == "Bold":
            weight = "bold"
        elif f_style == "Italic":
            slant = "italic"
        elif f_style == "Bold Italic":
            weight = "bold"
            slant = "italic"

        self.lbl_demo_text.configure(
            font=ctk.CTkFont(family=f_family, size=16, weight=weight, slant=slant),
            text_color=f_color
        )

        if hasattr(self, "preview_body"):
            self.preview_body.configure(
                text_color=f_color,
                font=ctk.CTkFont(family=f_family, size=14, weight=weight, slant=slant)
            )
        if hasattr(self, "preview_title"):
            self.preview_title.configure(
                text_color=f_color,
                font=ctk.CTkFont(family=f_family, size=18, weight="bold" if weight == "bold" else "normal", slant=slant)
            )
        if hasattr(self, "preview_entry"):
            self.preview_entry.configure(
                font=ctk.CTkFont(family=f_family, size=13, weight=weight, slant=slant)
            )

    # =========================================================
    # IMAGE GALLERY + LIGHTBOX PREVIEW + PALETTE ONLY
    # =========================================================
    def change_gallery_dir(self):
        global GALLERY_DIR
        folder = filedialog.askdirectory(initialdir=GALLERY_DIR if os.path.exists(GALLERY_DIR) else os.path.expanduser("~"))
        if folder:
            GALLERY_DIR = os.path.abspath(folder)
            self.lbl_gallery_dir.configure(text=f"Current folder: {GALLERY_DIR}")
            self.load_gallery_images()

    def send_gallery_to_batch(self):
        if os.path.exists(GALLERY_DIR):
            self.image_manager_instance.src_folder.set(GALLERY_DIR)
            self.show_view("img_mgr")

    def use_gallery_image_as_folder_icon(self, image_path: str):
        self._set_selected_folder_icon(image_path)
        self.show_view("folders")

    def extract_palette_only_from_gallery(self, image_path: str):
        try:
            top_colors = WindowsThemeEngine.extract_top_colors(image_path, n=5)
            self.current_state["extracted_palette"] = top_colors
            self._update_dynamic_palette(top_colors)
            self.apply_selected_color(top_colors[0])
            self.show_view("theme")
        except Exception as e:
            messagebox.showerror("Error", f"Could not extract palette:\n{e}")

    def open_gallery_lightbox(self, image_path: str):
        win = ctk.CTkToplevel(self)
        win.title(f"Preview - {os.path.basename(image_path)}")
        win.geometry("860x640")
        win.attributes("-topmost", True)

        try:
            with Image.open(image_path) as raw:
                img = ImageOps.exif_transpose(raw).convert("RGBA")
                orig_w, orig_h = img.size
                img.thumbnail((800, 480), Image.Resampling.LANCZOS)
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)

            lbl_img = ctk.CTkLabel(win, image=ctk_img, text="")
            lbl_img.image = ctk_img
            lbl_img.pack(padx=20, pady=(20, 8))

            ctk.CTkLabel(
                win, text=f"{os.path.basename(image_path)}  ({orig_w} × {orig_h} px)",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(pady=(0, 10))

            bar = ctk.CTkFrame(win, fg_color="transparent")
            bar.pack(pady=10)
            ctk.CTkButton(bar, text="🖼️ Set as Wallpaper", command=lambda: [self.set_wallpaper_from_gallery(image_path), win.destroy()]).pack(side="left", padx=6)
            ctk.CTkButton(bar, text="🎨 Extract Palette Only", fg_color="#2FA572", hover_color="#106A43", command=lambda: [self.extract_palette_only_from_gallery(image_path), win.destroy()]).pack(side="left", padx=6)
            ctk.CTkButton(bar, text="🖱️ Send to Cursor Creator", command=lambda: [self.send_image_to_cursor_creator(image_path), win.destroy()]).pack(side="left", padx=6)
            ctk.CTkButton(bar, text="📁 Use as Folder Icon", fg_color="#444444", command=lambda: [self.use_gallery_image_as_folder_icon(image_path), win.destroy()]).pack(side="left", padx=6)
        except Exception as e:
            ctk.CTkLabel(win, text=f"Error opening image: {e}", text_color="red").pack(pady=30)

    def send_image_to_cursor_creator(self, image_path: str):
        self.cursor_gen_source_path = image_path
        self.lbl_cur_gen_src.configure(text=os.path.basename(image_path), text_color="white")
        self._update_cursor_gen_preview()
        self.show_view("cursors")

    def load_gallery_images(self):
        for widget in self.gallery_grid.winfo_children():
            widget.destroy()
        self.gallery_images.clear()

        if hasattr(self, "lbl_gallery_dir"):
            self.lbl_gallery_dir.configure(
                text=f"{T['current_folder']}: {GALLERY_DIR}"
            )


        if not os.path.exists(GALLERY_DIR):
            self.gallery_status_lbl.configure(text="Folder not found.", text_color="red")
            return

        valid_exts = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
        image_paths = []

        try:
            if self.gallery_subfolders_var.get():
                for root_dir, _, files in os.walk(GALLERY_DIR):
                    for f in files:
                        if f.lower().endswith(valid_exts):
                            image_paths.append(os.path.join(root_dir, f))
            else:
                for f in os.listdir(GALLERY_DIR):
                    if f.lower().endswith(valid_exts):
                        full_p = os.path.join(GALLERY_DIR, f)
                        if os.path.isfile(full_p):
                            image_paths.append(full_p)
        except Exception as e:
            self.gallery_status_lbl.configure(text=f"Error reading folder: {e}", text_color="red")
            return

        if not image_paths:
            self.gallery_status_lbl.configure(
                text=T["no_images_found"],
                text_color="gray"
            )
            return


        max_display = 36
        shown_count = min(len(image_paths), max_display)
        self.gallery_status_lbl.configure(
            text=T["gallery_status"].format(
                shown=shown_count,
                total=len(image_paths)
        ),
        text_color="gray"
)

        col_count = 3
        for i, fpath in enumerate(image_paths[:max_display]):
            fname = os.path.basename(fpath)
            try:
                with Image.open(fpath) as raw_img:
                    img = ImageOps.exif_transpose(raw_img).convert("RGBA")
                    img.thumbnail((220, 135), Image.Resampling.LANCZOS)
                    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
                    self.gallery_images.append(ctk_img)

                card = ctk.CTkFrame(self.gallery_grid, corner_radius=8)
                card.grid(row=i // col_count, column=i % col_count, padx=8, pady=8, sticky="nsew")

                btn_img = ctk.CTkButton(
                    card, image=ctk_img, text="", width=230, height=140,
                    fg_color="transparent", hover_color="#2b2b2b",
                    command=lambda p=fpath: self.open_gallery_lightbox(p)
                )
                btn_img.pack(padx=6, pady=(6, 2))

                short_name = fname[:24] + ("..." if len(fname) > 24 else "")
                ctk.CTkLabel(card, text=short_name, font=ctk.CTkFont(size=11, weight="bold")).pack(pady=(0, 4))

                btn_row1 = ctk.CTkFrame(card, fg_color="transparent")
                btn_row1.pack(pady=(0, 3))
                ctk.CTkButton(
                    btn_row1, text=f"🖼️ {T['wallpaper_btn']}", width=105, height=25, font=ctk.CTkFont(size=11),
                    command=lambda p=fpath: self.set_wallpaper_from_gallery(p)
                ).pack(side="left", padx=2)
                ctk.CTkButton(
                    btn_row1, text=f"🎨 {T['palette_btn']}", width=105, height=25, font=ctk.CTkFont(size=11),
                    fg_color="#2FA572", hover_color="#106A43",
                    command=lambda p=fpath: self.extract_palette_only_from_gallery(p)
                ).pack(side="left", padx=2)

                btn_row2 = ctk.CTkFrame(card, fg_color="transparent")
                btn_row2.pack(pady=(0, 8))
                ctk.CTkButton(
                    btn_row2, text=f"📂 {T['icon_btn']}", width=105, height=25, font=ctk.CTkFont(size=11),
                    fg_color="#444444", hover_color="#333333",
                    command=lambda p=fpath: self.use_gallery_image_as_folder_icon(p)
                ).pack(side="left", padx=2)
                ctk.CTkButton(
                    btn_row2, text=f"🖱️ {T['cursor_btn']}", width=105, height=25, font=ctk.CTkFont(size=11),
                    fg_color="#444444", hover_color="#333333",
                    command=lambda p=fpath: self.send_image_to_cursor_creator(p)
                ).pack(side="left", padx=2)
            except Exception as e:
                print(f"Error loading image {fname}: {e}")

    def set_wallpaper_from_gallery(self, path):
        self.apply_wallpaper_path(path)
        messagebox.showinfo("Wallpaper", f"Wallpaper updated to:\n{os.path.basename(path)}")

    # =========================================================
    # ICON PACK (.ZIP) & CURSOR PACK (.ZIP) + CURSOR CREATOR
    # =========================================================
    def export_icon_pack_zip(self):
        icons = self.current_state.get("system_icons", {})
        valid = {k: v for k, v in icons.items() if v and os.path.exists(v)}
        if not valid:
            messagebox.showwarning("No Icons", "Please assign at least one custom System Icon before exporting an Icon Pack.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("Icon Pack ZIP", "*.zip")], title="Export Icon Pack (.zip)")
        if not save_path:
            return

        try:
            manifest = {"type": "icon_pack", "icons": {}}
            with zipfile.ZipFile(save_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for tag, path in valid.items():
                    ico_p = WindowsThemeEngine.ensure_ico(path, f"pack_{tag}")
                    arcname = f"{tag}.ico"
                    zf.write(ico_p, arcname=arcname)
                    manifest["icons"][tag] = arcname
                zf.writestr("manifest.json", json.dumps(manifest, indent=4))
            messagebox.showinfo("Exported", f"Icon Pack exported successfully to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export Icon Pack:\n{e}")

    def import_icon_pack_zip(self):
        zip_path = filedialog.askopenfilename(filetypes=[("Icon Pack ZIP", "*.zip")], title="Select Icon Pack (.zip)")
        if not zip_path:
            return

        pack_name = os.path.splitext(os.path.basename(zip_path))[0]
        extract_dir = os.path.join(PACKS_IMPORT_DIR, f"icons_{pack_name}")
        os.makedirs(extract_dir, exist_ok=True)

        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(extract_dir)

            clsid_map = {
                "this_pc": (CLSID_THIS_PC, False),
                "recycle_bin": (CLSID_RECYCLE_BIN, True),
                "user_files": (CLSID_USER_FILES, False),
            }
            applied_count = 0

            for root_d, _, files in os.walk(extract_dir):
                for f in files:
                    low = f.lower()
                    if not low.endswith((".ico", ".png")):
                        continue
                    full_p = os.path.join(root_d, f)
                    matched_tag = None
                    if "this_pc" in low or "computer" in low or "pc" in low:
                        matched_tag = "this_pc"
                    elif "recycle" in low or "bin" in low or "trash" in low:
                        matched_tag = "recycle_bin"
                    elif "user" in low or "files" in low or "home" in low:
                        matched_tag = "user_files"

                    if matched_tag:
                        clsid, is_bin = clsid_map[matched_tag]
                        WindowsThemeEngine.set_clsid_icon(clsid, full_p, matched_tag, is_bin, auto_refresh=False)
                        self.current_state["system_icons"][matched_tag] = full_p
                        if matched_tag in self.icon_preview_labels:
                            img = Image.open(full_p)
                            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(32, 32))
                            self.icon_preview_labels[matched_tag].configure(image=ctk_img, text="")
                        applied_count += 1

            WindowsThemeEngine.refresh_shell()
            messagebox.showinfo("Icon Pack Imported", f"Imported and applied {applied_count} system icons from pack!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import Icon Pack:\n{e}")

    def export_cursor_pack_zip(self):
        cursors = self.current_state.get("cursors", {})
        valid = {k: v for k, v in cursors.items() if v and os.path.exists(v)}
        if not valid:
            messagebox.showwarning("No Cursors", "Please select or generate at least one custom cursor before exporting a Cursor Pack.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("Cursor Pack ZIP", "*.zip")], title="Export Cursor Pack (.zip)")
        if not save_path:
            return

        try:
            manifest = {"type": "cursor_pack", "cursors": {}}
            with zipfile.ZipFile(save_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for role, path in valid.items():
                    ext = os.path.splitext(path)[1]
                    arcname = f"{role}{ext}"
                    zf.write(path, arcname=arcname)
                    manifest["cursors"][role] = arcname
                zf.writestr("manifest.json", json.dumps(manifest, indent=4))
            messagebox.showinfo("Exported", f"Cursor Pack exported successfully to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export Cursor Pack:\n{e}")

    def import_cursor_pack_zip(self):
        zip_path = filedialog.askopenfilename(filetypes=[("Cursor Pack ZIP", "*.zip")], title="Select Cursor Pack (.zip)")
        if not zip_path:
            return

        pack_name = os.path.splitext(os.path.basename(zip_path))[0]
        extract_dir = os.path.join(PACKS_IMPORT_DIR, f"cursors_{pack_name}")
        os.makedirs(extract_dir, exist_ok=True)

        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(extract_dir)

            new_cursors = {}
            for root_d, _, files in os.walk(extract_dir):
                for f in files:
                    low = f.lower()
                    if not low.endswith((".cur", ".ani")):
                        continue
                    full_p = os.path.join(root_d, f)
                    if "arrow" in low or "normal" in low:
                        new_cursors["Arrow"] = full_p
                    elif "hand" in low or "link" in low:
                        new_cursors["Hand"] = full_p
                    elif "ibeam" in low or "text" in low:
                        new_cursors["IBeam"] = full_p
                    elif "appstarting" in low or "work" in low or "wait" in low or "busy" in low:
                        new_cursors["AppStarting"] = full_p

            if not new_cursors:
                messagebox.showwarning("No Matching Cursors", "No .cur or .ani files matching Arrow/Hand/IBeam/AppStarting were found in the ZIP.")
                return

            WindowsThemeEngine.set_cursors(new_cursors)
            for k, p in new_cursors.items():
                self.current_state["cursors"][k] = p
                if k in self.cursor_labels:
                    self.cursor_labels[k].configure(text=os.path.basename(p), text_color="white")

            messagebox.showinfo("Cursor Pack Imported", f"Applied {len(new_cursors)} cursors from pack!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import Cursor Pack:\n{e}")

    def pick_cursor_gen_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.bmp *.ico")])
        if path:
            self.cursor_gen_source_path = path
            self.lbl_cur_gen_src.configure(text=os.path.basename(path), text_color="white")
            self._update_cursor_gen_preview()

    def _update_cursor_gen_preview(self):
        size = int(self.cur_gen_size_var.get())
        self.cur_hx_slider.configure(to=max(1, size - 1))
        self.cur_hy_slider.configure(to=max(1, size - 1))
        hx = min(size - 1, int(self.cur_gen_hx_var.get()))
        hy = min(size - 1, int(self.cur_gen_hy_var.get()))
        self.lbl_hotspot_coords.configure(text=f"({hx}, {hy})")

        if not self.cursor_gen_source_path or not os.path.exists(self.cursor_gen_source_path):
            return

        try:
            with Image.open(self.cursor_gen_source_path) as raw:
                img = ImageOps.exif_transpose(raw).convert("RGBA")
                img = img.resize((size, size), Image.Resampling.LANCZOS)
                # Draw red crosshair on preview to show Hotspot
                preview_canvas = img.resize((64, 64), Image.Resampling.NEAREST)
                draw = ImageDraw.Draw(preview_canvas)
                px = int((hx / size) * 64)
                py = int((hy / size) * 64)
                draw.line([(max(0, px - 6), py), (min(63, px + 6), py)], fill="#FF1744", width=2)
                draw.line([(px, max(0, py - 6)), (px, min(63, py + 6))], fill="#FF1744", width=2)

                ctk_img = ctk.CTkImage(light_image=preview_canvas, dark_image=preview_canvas, size=(64, 64))
                self.cur_gen_preview_lbl.configure(image=ctk_img, text="")
        except Exception as e:
            print(f"Preview error: {e}")

    def generate_cursor_from_image(self, apply_now: bool = True):
        if not self.cursor_gen_source_path or not os.path.exists(self.cursor_gen_source_path):
            messagebox.showwarning("Select Image", "Please select a source image first!")
            return

        role = self.cur_gen_role_var.get()
        size = int(self.cur_gen_size_var.get())
        hx = min(size - 1, int(self.cur_gen_hx_var.get()))
        hy = min(size - 1, int(self.cur_gen_hy_var.get()))

        if apply_now:
            out_path = os.path.join(CUSTOM_CURSORS_DIR, f"custom_{role}_{size}px.cur")
        else:
            out_path = filedialog.asksaveasfilename(defaultextension=".cur", filetypes=[("Windows Cursor", "*.cur")], initialfile=f"custom_{role}.cur")
            if not out_path:
                return

        try:
            saved_cur = WindowsThemeEngine.create_cur_from_image(self.cursor_gen_source_path, out_path, size=size, hotspot_x=hx, hotspot_y=hy)
            if apply_now:
                self.current_state["cursors"][role] = saved_cur
                if role in self.cursor_labels:
                    self.cursor_labels[role].configure(text=os.path.basename(saved_cur), text_color="white")
                WindowsThemeEngine.set_cursors({role: saved_cur})
                messagebox.showinfo("Cursor Applied", f"Created & applied custom '{role}' cursor ({size}x{size}, hotspot {hx},{hy})!")
            else:
                messagebox.showinfo("Cursor Saved", f"Custom cursor saved to:\n{saved_cur}")
        except Exception as e:
            messagebox.showerror("Error", f"Cursor generation failed:\n{e}")

    def pick_cursor_file(self, cursor_key: str, lbl_widget):
        path = filedialog.askopenfilename(filetypes=[("Mouse Pointers", "*.cur *.ani")])
        if path:
            abs_p = os.path.abspath(path)
            self.current_state["cursors"][cursor_key] = abs_p
            lbl_widget.configure(text=os.path.basename(abs_p), text_color="white")
            WindowsThemeEngine.set_cursors({cursor_key: abs_p})

    # =========================================================
    # PALETTE & COLOR ENGINE
    # =========================================================
    def _build_empty_palette_preview(self):
        for w in self.palette_container.winfo_children():
            w.destroy()
        ctk.CTkLabel(self.palette_container, text=f"({T['palette_hint']})", text_color="gray", font=ctk.CTkFont(size=12)).pack(side="left", padx=5)

    def _update_dynamic_palette(self, colors: list):
        for w in self.palette_container.winfo_children():
            w.destroy()
        ctk.CTkLabel(self.palette_container, text=f"{T['shades']}:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(5, 6))
        for hex_val in colors:
            ctk.CTkButton(
                self.palette_container, text="", width=26, height=26, corner_radius=13,
                fg_color=hex_val, hover_color=hex_val,
                command=lambda h=hex_val: self.apply_selected_color(h)
            ).pack(side="left", padx=2)

    def apply_hex_color(self):
        hex_color = self.hex_entry.get().strip().upper()
        if not hex_color.startswith("#"):
            hex_color = "#" + hex_color

        if len(hex_color) != 7:
            messagebox.showerror("Invalid HEX", "HEX color must be in format #RRGGBB")
            return

        try:
            int(hex_color[1:], 16)
        except ValueError:
            messagebox.showerror("Invalid HEX", "HEX color is not valid.")
            return

        self.apply_selected_color(hex_color)

    def open_color_picker(self):
        color = colorchooser.askcolor(initialcolor=self.current_state["accent_color"], title="Select Accent Color")
        if color and color[1]:
            self.apply_selected_color(color[1].upper())

    def save_undo_state(self):
        self.undo_state = json.loads(json.dumps(self.current_state))

    def toggle_restore_points(self):
        enabled = bool(self.create_restore_point_var.get())
        self.current_state["create_restore_point"] = enabled
        if hasattr(self, "restore_status"):
            status_txt = "Restore Point: Ready" if enabled else "Restore Point: Disabled"
            self.restore_status.configure(text=status_txt)

    def create_restore_point(self, description: str):
        if not self.current_state.get("create_restore_point", True):
            return
        if hasattr(self, "restore_status"):
            self.restore_status.configure(text=f"Restore Point: {description}")

    def undo_last_change(self):
        if not self.undo_state:
            messagebox.showinfo("Undo", "No previous changes to undo.")
            return

        prev = self.undo_state
        self.undo_state = None
        self.current_state = prev.copy()

        self.font_var.set(self.current_state.get("font_family", "Segoe UI"))
        self.font_style_var.set(self.current_state.get("font_style", "Regular"))
        f_color = self.current_state.get("font_color", "#FFFFFF")
        self.font_color_swatch.configure(fg_color=f_color)

        self.apply_selected_color(self.current_state["accent_color"], record_undo=False)
        self.update_demo_text()

    def apply_selected_color(self, hex_color: str, record_undo: bool = True):
        if record_undo:
            self.save_undo_state()
        self.create_restore_point("Accent Color Change")

        hex_upper = hex_color.upper()
        self.current_state["accent_color"] = hex_upper
        self.current_state["color_taskbar"] = bool(self.chk_taskbar.get())
        self.current_state["color_borders"] = bool(self.chk_borders.get())

        if hasattr(self, "preview_accent"):
            self.preview_accent.configure(fg_color=hex_upper)
        if hasattr(self, "preview_button"):
            self.preview_button.configure(fg_color=hex_upper)
        if hasattr(self, "preview_titlebar"):
            self.preview_titlebar.configure(fg_color=hex_upper)

        self.color_swatch.configure(fg_color=hex_upper)
        self.lbl_hex_color.configure(text=hex_upper)
        self.hex_entry.delete(0, "end")
        self.hex_entry.insert(0, hex_upper)

        if self.current_state["color_taskbar"]:
            self.dark_switch.select()
            self.current_state["dark_mode"] = True

        WindowsThemeEngine.set_accent_color(
            hex_upper,
            color_taskbar=self.current_state["color_taskbar"],
            color_borders=self.current_state["color_borders"]
        )

    def refresh_accent_options(self):
        self.apply_selected_color(self.current_state["accent_color"])

    # =========================================================
    # PROFILES, PORTABLE THEME PACK (.ZIP) & DAY/NIGHT SCHEDULER
    # =========================================================
    def _build_profile_payload(self, name: str) -> dict:
        return {
            "name": name,
            "dark_mode": bool(self.dark_switch.get()),
            "explorer_mode": self.exp_mode_var.get(),
            "compact_explorer": bool(self.exp_compact_var.get()),
            "system_transparency": bool(self.trans_switch.get()),
            "taskbar_effect": self.tb_effect_var.get(),
            "taskbar_alpha": int(self.tb_alpha_slider.get()),
            "wallpaper": self.current_state["wallpaper"],
            "wallpaper_fit": self.wp_fit_var.get(),
            "auto_accent_from_wp": bool(self.chk_auto_wp_color.get()),
            "accent_color": self.current_state["accent_color"],
            "color_taskbar": bool(self.chk_taskbar.get()),
            "color_borders": bool(self.chk_borders.get()),
            "extracted_palette": self.current_state["extracted_palette"],
            "cursors": self.current_state["cursors"],
            "system_icons": self.current_state["system_icons"],
            "folders": self.current_state["folders"],
            "font_family": self.current_state.get("font_family", "Segoe UI"),
            "font_style": self.current_state.get("font_style", "Regular"),
            "font_color": self.current_state.get("font_color", "#FFFFFF"),
            "create_restore_point": bool(self.create_restore_point_var.get())
        }

    def save_current_profile(self):
        raw_name = self.entry_profile_name.get().strip()
        if not raw_name:
            messagebox.showwarning("Enter Name", "Please enter a name for the profile before saving!")
            return
        safe_name = "".join(c for c in raw_name if c.isalnum() or c in (" ", "-", "_")).strip()
        file_path = os.path.join(PROFILES_DIR, f"{safe_name}.json")
        payload = self._build_profile_payload(raw_name)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=4, ensure_ascii=False)
            self.entry_profile_name.delete(0, "end")
            self.refresh_profiles_list()
            messagebox.showinfo("Saved", f"Profile '{raw_name}' saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving profile:\n{e}")

    def export_full_theme_pack_zip(self):
        raw_name = self.entry_profile_name.get().strip() or "Custom_Theme_Pack"
        save_path = filedialog.asksaveasfilename(
            defaultextension=".zip", filetypes=[("Theme Pack ZIP", "*.zip")],
            initialfile=f"{raw_name}.zip", title="Export Portable Theme Pack (.zip)"
        )
        if not save_path:
            return

        payload = self._build_profile_payload(raw_name)
        try:
            with zipfile.ZipFile(save_path, "w", zipfile.ZIP_DEFLATED) as zf:
                # Bundle Wallpaper
                wp = payload.get("wallpaper")
                if wp and os.path.exists(wp):
                    wp_arc = f"assets/wallpaper{os.path.splitext(wp)[1]}"
                    zf.write(wp, arcname=wp_arc)
                    payload["wallpaper"] = wp_arc

                # Bundle System Icons
                bundled_icons = {}
                for tag, ipath in payload.get("system_icons", {}).items():
                    if ipath and os.path.exists(ipath):
                        ico_arc = f"assets/icons/{tag}{os.path.splitext(ipath)[1]}"
                        zf.write(ipath, arcname=ico_arc)
                        bundled_icons[tag] = ico_arc
                    else:
                        bundled_icons[tag] = None
                payload["system_icons"] = bundled_icons

                # Bundle Cursors
                bundled_cursors = {}
                for role, cpath in payload.get("cursors", {}).items():
                    if cpath and os.path.exists(cpath):
                        cur_arc = f"assets/cursors/{role}{os.path.splitext(cpath)[1]}"
                        zf.write(cpath, arcname=cur_arc)
                        bundled_cursors[role] = cur_arc
                    else:
                        bundled_cursors[role] = None
                payload["cursors"] = bundled_cursors

                zf.writestr("theme_profile.json", json.dumps(payload, indent=4, ensure_ascii=False))
            messagebox.showinfo("Exported", f"Portable Theme Pack (.zip) saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export Theme Pack:\n{e}")

    def import_full_theme_pack_zip(self):
        zip_path = filedialog.askopenfilename(filetypes=[("Theme Pack ZIP", "*.zip")], title="Import Portable Theme Pack (.zip)")
        if not zip_path:
            return

        pack_name = os.path.splitext(os.path.basename(zip_path))[0]
        extract_dir = os.path.join(PACKS_IMPORT_DIR, f"theme_{pack_name}")
        os.makedirs(extract_dir, exist_ok=True)

        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(extract_dir)

            json_file = os.path.join(extract_dir, "theme_profile.json")
            if not os.path.exists(json_file):
                messagebox.showerror("Invalid Pack", "theme_profile.json not found inside the ZIP archive.")
                return

            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Resolve relative asset paths to absolute extracted paths
            if data.get("wallpaper"):
                cand = os.path.join(extract_dir, data["wallpaper"])
                if os.path.exists(cand):
                    data["wallpaper"] = os.path.abspath(cand)

            for tag, rel in list(data.get("system_icons", {}).items()):
                if rel:
                    cand = os.path.join(extract_dir, rel)
                    if os.path.exists(cand):
                        data["system_icons"][tag] = os.path.abspath(cand)

            for role, rel in list(data.get("cursors", {}).items()):
                if rel:
                    cand = os.path.join(extract_dir, rel)
                    if os.path.exists(cand):
                        data["cursors"][role] = os.path.abspath(cand)

            prof_name = data.get("name", pack_name)
            safe_name = "".join(c for c in prof_name if c.isalnum() or c in (" ", "-", "_")).strip()
            with open(os.path.join(PROFILES_DIR, f"{safe_name}.json"), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            self.refresh_profiles_list()
            self.apply_profile(data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import Theme Pack:\n{e}")

    def import_external_profile(self):
        path = filedialog.askopenfilename(filetypes=[("JSON Profile", "*.json")])
        if path:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                name = data.get("name", os.path.splitext(os.path.basename(path))[0])
                safe_name = "".join(c for c in name if c.isalnum() or c in (" ", "-", "_")).strip()
                with open(os.path.join(PROFILES_DIR, f"{safe_name}.json"), "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                self.refresh_profiles_list()
            except Exception as e:
                messagebox.showerror("Error", f"Import failed:\n{e}")

    def refresh_profiles_list(self):
        for widget in self.profiles_list_frame.winfo_children():
            widget.destroy()

        files = sorted([f for f in os.listdir(PROFILES_DIR) if f.endswith(".json")])
        if hasattr(self, "day_prof_combo"):
            prof_names = [f[:-5] for f in files]
            self.day_prof_combo.configure(values=prof_names if prof_names else [""])
            self.night_prof_combo.configure(values=prof_names if prof_names else [""])
            if prof_names and not self.day_prof_var.get():
                self.day_prof_var.set(prof_names[0])
            if prof_names and not self.night_prof_var.get():
                self.night_prof_var.set(prof_names[-1])

        if not files:
            ctk.CTkLabel(self.profiles_list_frame, text=T["no_saved_profiles"], text_color="gray").pack(pady=30)
            return

        for fname in files:
            fpath = os.path.join(PROFILES_DIR, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                continue

            prof_name = data.get("name", fname[:-5])
            mode_txt = f"🌙 {T['dark']}" if data.get("dark_mode", True) else f"☀️ {T['light']}"
            accent_hex = data.get("accent_color", "#0078D4")

            card = ctk.CTkFrame(self.profiles_list_frame)
            card.pack(fill="x", padx=5, pady=6)
            ctk.CTkFrame(card, width=18, height=42, corner_radius=4, fg_color=accent_hex).pack(side="left", padx=(12, 5), pady=10)
            
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)
            
            ctk.CTkLabel(info_frame, text=prof_name, font=ctk.CTkFont(size=16, weight="bold"), anchor="w").pack(fill="x")
            ctk.CTkLabel(info_frame, text=f"{mode_txt}  •  🎨 {accent_hex}", text_color="gray", font=ctk.CTkFont(size=12), anchor="w").pack(fill="x")
            
            ctk.CTkButton(card, text=T["delete"], width=70, fg_color="#6e1c1c", hover_color="#4a1212", command=lambda p=fpath: self.delete_profile(p)).pack(side="right", padx=(5, 15), pady=10)
            ctk.CTkButton(card, text=f"⚡ {T['apply']}", width=130, font=ctk.CTkFont(weight="bold"), command=lambda d=data: self.apply_profile(d)).pack(side="right", padx=5, pady=10)

    def apply_font_style(self, choice=None):
        self.current_state["font_style"] = self.font_style_var.get()
        self.update_demo_text()

    def apply_profile(self, data: dict, silent: bool = False):
        try:
            is_dark = data.get("dark_mode", True)
            WindowsThemeEngine.set_dark_mode(is_dark)
            if is_dark:
                self.dark_switch.select()
            else:
                self.dark_switch.deselect()

            if "explorer_mode" in data:
                self.exp_mode_var.set(data["explorer_mode"])
                self.exp_compact_var.set(bool(data.get("compact_explorer", False)))
                WindowsThemeEngine.set_explorer_theme(data["explorer_mode"], bool(data.get("compact_explorer", False)))

            if "system_transparency" in data:
                if data["system_transparency"]:
                    self.trans_switch.select()
                else:
                    self.trans_switch.deselect()
                WindowsThemeEngine.set_system_transparency(bool(data["system_transparency"]))

            if "taskbar_effect" in data:
                self.tb_effect_var.set(data["taskbar_effect"])
                self.tb_alpha_slider.set(data.get("taskbar_alpha", 120))
                self.apply_taskbar_effect_ui()

            wp = data.get("wallpaper")
            fit = data.get("wallpaper_fit", "Fill")
            self.wp_fit_var.set(fit)
            if wp and os.path.exists(wp):
                WindowsThemeEngine.set_wallpaper_fit(fit)
                self.apply_wallpaper_path(wp)

            accent_hex = data.get("accent_color")
            if accent_hex:
                self.apply_selected_color(accent_hex)

            font_fam = data.get("font_family")
            if font_fam:
                self.font_var.set(font_fam)
                self.current_state["font_family"] = font_fam

            font_style = data.get("font_style")
            if font_style:
                self.font_style_var.set(font_style)
                self.current_state["font_style"] = font_style
            
            f_color = data.get("font_color")
            if f_color:
                self.current_state["font_color"] = f_color
                self.font_color_swatch.configure(fg_color=f_color)
                
                # Päivitetään tekstikenttä profiilia ladattaessa
                if hasattr(self, 'font_hex_entry'):
                    self.font_hex_entry.delete(0, "end")
                    self.font_hex_entry.insert(0, f_color)
            
            self.update_demo_text()

            cursors = data.get("cursors", {})
            if cursors:
                WindowsThemeEngine.set_cursors(cursors)
                for c_key, c_path in cursors.items():
                    if c_path and c_key in self.cursor_labels:
                        self.cursor_labels[c_key].configure(text=os.path.basename(c_path), text_color="white")

            sys_icons = data.get("system_icons", {})
            clsid_map = {"this_pc": (CLSID_THIS_PC, False), "recycle_bin": (CLSID_RECYCLE_BIN, True), "user_files": (CLSID_USER_FILES, False)}
            for tag, (clsid, is_bin) in clsid_map.items():
                icon_path = sys_icons.get(tag)
                if icon_path and os.path.exists(icon_path):
                    WindowsThemeEngine.set_clsid_icon(clsid, icon_path, tag, is_bin, auto_refresh=False)
                    if tag in self.icon_preview_labels:
                        img = Image.open(icon_path)
                        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(32, 32))
                        self.icon_preview_labels[tag].configure(image=ctk_img, text="")

            for folder_path, icon_path in data.get("folders", {}).items():
                if os.path.exists(folder_path) and os.path.exists(icon_path):
                    WindowsThemeEngine.set_folder_icon(folder_path, icon_path, auto_refresh=False)

            WindowsThemeEngine.refresh_shell()
            if not silent:
                messagebox.showinfo("Profile Applied", f"Theme profile '{data.get('name', '')}' applied successfully!")
        except Exception as e:
            if not silent:
                messagebox.showerror("Error", f"Error loading profile:\n{e}")

            WindowsThemeEngine.refresh_shell()
            if not silent:
                messagebox.showinfo("Profile Applied", f"Theme profile '{data.get('name', '')}' applied successfully!")
        except Exception as e:
            if not silent:
                messagebox.showerror("Error", f"Error loading profile:\n{e}")

    def delete_profile(self, file_path: str):
        if messagebox.askyesno("Delete", "Are you sure you want to delete this profile?"):
            os.remove(file_path)
            self.refresh_profiles_list()

    # --- AUTO DAY / NIGHT SCHEDULER ---
    def on_toggle_day_night_schedule(self):
        enabled = bool(self.auto_dn_var.get())
        self.current_state["auto_day_night"] = enabled
        self.last_auto_applied_slot = None
        if enabled:
            self._check_day_night_schedule()
        else:
            self.sched_status_lbl.configure(text="Scheduler status: Inactive", text_color="gray")

    def _parse_hhmm(self, val: str, default_minutes: int) -> int:
        try:
            parts = val.strip().split(":")
            return int(parts[0]) * 60 + int(parts[1])
        except Exception:
            return default_minutes

    def _check_day_night_schedule(self):
        if not self.auto_dn_var.get():
            return

        now = datetime.datetime.now()
        now_mins = now.hour * 60 + now.minute
        day_mins = self._parse_hhmm(self.day_time_entry.get(), 7 * 60)
        night_mins = self._parse_hhmm(self.night_time_entry.get(), 20 * 60)

        if day_mins <= now_mins < night_mins:
            target_slot = "day"
            target_prof = self.day_prof_var.get()
        else:
            target_slot = "night"
            target_prof = self.night_prof_var.get()

        self.sched_status_lbl.configure(
            text=f"Scheduler active: Current slot is {target_slot.upper()} (Profile: {target_prof or 'None'})",
            text_color="#2FA572"
        )

        if target_prof and self.last_auto_applied_slot != (target_slot, target_prof):
            prof_file = os.path.join(PROFILES_DIR, f"{target_prof}.json")
            if os.path.exists(prof_file):
                try:
                    with open(prof_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    self.apply_profile(data, silent=True)
                    self.last_auto_applied_slot = (target_slot, target_prof)
                except Exception as e:
                    print(f"Auto scheduler error: {e}")

    def _background_scheduler_tick(self):
        self._check_day_night_schedule()
        self.after(30000, self._background_scheduler_tick)

    # =========================================================
    # DRAG & DROP AND FOLDERS
    # =========================================================
    def on_drop_files(self, files):
        global GALLERY_DIR
        for raw_path in files:
            path = raw_path.decode("mbcs") if isinstance(raw_path, bytes) else str(raw_path)
            if os.path.isdir(path):
                if self.active_view == "img_mgr":
                    self.image_manager_instance.src_folder.set(path)
                    return
                elif self.active_view == "gallery":
                    GALLERY_DIR = os.path.abspath(path)
                    self.load_gallery_images()
                    return
                else:
                    self.show_view("folders")
                    self._set_selected_folder(path)
            elif path.lower().endswith((".png", ".ico", ".jpg", ".jpeg", ".webp")):
                if self.active_view == "cursors":
                    self.send_image_to_cursor_creator(path)
                else:
                    self.show_view("folders")
                    self._set_selected_folder_icon(path)

    def _set_selected_folder(self, path: str):
        self.selected_folder = path
        self.lbl_folder_path.configure(text=path, text_color="white")

    def _set_selected_folder_icon(self, path: str):
        self.selected_folder_icon = path
        self.lbl_folder_icon.configure(text=os.path.basename(path), text_color="white")
        try:
            img = Image.open(path)
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(32, 32))
            self.folder_icon_preview.configure(image=ctk_img, text="")
        except Exception:
            pass

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self._set_selected_folder(folder)

    def browse_folder_icon(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.ico *.png *.jpg *.jpeg *.webp")])
        if path:
            self._set_selected_folder_icon(path)

    def apply_folder_icon(self):
        if not self.selected_folder or not self.selected_folder_icon:
            messagebox.showwarning("Missing Information", "Please select or drag a folder and an icon!")
            return
        WindowsThemeEngine.set_folder_icon(self.selected_folder, self.selected_folder_icon)
        self.current_state["folders"][os.path.abspath(self.selected_folder)] = os.path.abspath(self.selected_folder_icon)
        messagebox.showinfo("Complete", "Folder icon updated!")

    def clear_folder_icon(self):
        if not self.selected_folder:
            messagebox.showwarning("Select", "Please select a folder first.")
            return
        WindowsThemeEngine.reset_folder_icon(self.selected_folder)
        self.current_state["folders"].pop(os.path.abspath(self.selected_folder), None)
        messagebox.showinfo("Complete", "Default folder icon restored.")

    def toggle_dark_mode(self):
        is_dark = bool(self.dark_switch.get())
        self.current_state["dark_mode"] = is_dark
        self.exp_mode_var.set("Dark" if is_dark else "Light")
        WindowsThemeEngine.set_dark_mode(is_dark)

    def apply_wallpaper_path(self, path):
        abs_p = os.path.abspath(path)
        WindowsThemeEngine.set_wallpaper(abs_p, self.wp_fit_var.get())
        self.current_state["wallpaper"] = abs_p
        self.wp_label.configure(text=os.path.basename(abs_p), text_color="white")
        try:
            top_colors = WindowsThemeEngine.extract_top_colors(abs_p, n=5)
            self.current_state["extracted_palette"] = top_colors
            self._update_dynamic_palette(top_colors)
            if self.chk_auto_wp_color.get() and top_colors:
                self.apply_selected_color(top_colors[0])
        except Exception as e:
            print(f"Color extraction error: {e}")

    def pick_wallpaper(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.webp")])
        if path:
            self.apply_wallpaper_path(path)

    def pick_icon(self, clsid, tag, is_bin, preview_lbl):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.ico *.png")])
        if path:
            img = Image.open(path)
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(32, 32))
            preview_lbl.configure(image=ctk_img, text="")
            WindowsThemeEngine.set_clsid_icon(clsid, path, tag, is_bin)
            self.current_state["system_icons"][tag] = os.path.abspath(path)

    def reset_defaults(self):
        if messagebox.askyesno("Defaults", "Restore system default icons, cursors, and taskbar state?"):
            WindowsThemeEngine.restore_default_icons()
            WindowsThemeEngine.restore_default_cursors()
            WindowsThemeEngine.apply_taskbar_composition("Default")
            self.tb_effect_var.set("Default")
            messagebox.showinfo("Complete", "Defaults restored!")


if __name__ == "__main__":
    app = ThemeApp()
    app.mainloop()
# -*- coding: utf-8 -*-
"""
Theme Studio

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
import json
import threading
import ctypes
import winreg
import hashlib
import colorsys
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image, ImageOps
import windnd

# --- WIN32 API VAKIOT ---
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

# Järjestelmäkuvakkeiden CLSID-tunnukset
CLSID_THIS_PC = "{20D04FE0-3AEA-1069-A2D8-08002B30309D}"
CLSID_RECYCLE_BIN = "{645FF040-5081-101B-9F08-00AA002F954E}"
CLSID_USER_FILES = "{59031a47-3f72-44a7-89c5-5595fe6b30ee}"

BASE_APP_DIR = os.path.join(os.path.expanduser("~"), ".win_theme_studio_icons")
PROFILES_DIR = os.path.join(BASE_APP_DIR, "profiles")
os.makedirs(BASE_APP_DIR, exist_ok=True)
os.makedirs(PROFILES_DIR, exist_ok=True)


class WindowsThemeEngine:
    """Taustamoottori Windowsin rekisteri-, väri-, kursori- ja API-kutsuille."""

    @staticmethod
    def refresh_shell(folder_path: str = None):
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
    def set_wallpaper(image_path: str):
        if not os.path.exists(image_path):
            return
        abs_path = os.path.abspath(image_path)
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, abs_path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
        )

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
                if val:
                    winreg.SetValueEx(key, name, 0, winreg.REG_EXPAND_SZ, val)
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETCURSORS, 0, None, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)

    @staticmethod
    def extract_top_colors(image_path: str, n: int = 5) -> list:
        img = Image.open(image_path).convert("RGB")
        img = img.resize((64, 64), Image.Resampling.LANCZOS)
        quantized = img.quantize(colors=16)
        palette = quantized.getpalette()
        color_counts = quantized.getcolors()

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
    """Kuvien massakäsittelylogiikka osaksi pääsovellusta."""
    def __init__(self, parent_frame):
        self.frame = parent_frame
        self.settings_file = os.path.join(BASE_APP_DIR, "image_manager_settings.json")

        self.src_folder = tk.StringVar()
        self.dest_folder = tk.StringVar()
        self.prefix = tk.StringVar(value="teema_kuva_")
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
                    self.prefix.set(settings.get("prefix", "teema_kuva_"))
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
                print(f"Virhe asetusten lataamisessa: {e}")

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
            print(f"Virhe asetusten tallentamisessa: {e}")

    def create_widgets(self):
        self.frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.frame, text="Kuvien massakäsittely", font=ctk.CTkFont(size=22, weight="bold")).grid(
            row=0, column=0, columnspan=3, padx=30, pady=(25, 15), sticky="w"
        )

        ctk.CTkLabel(self.frame, text="Lähdekansio:").grid(row=1, column=0, sticky="w", padx=30, pady=(10, 5))
        ctk.CTkEntry(self.frame, textvariable=self.src_folder).grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(10, 5))
        ctk.CTkButton(self.frame, text="Selaa...", command=self.browse_src, width=80).grid(row=1, column=2, padx=(0, 30), pady=(10, 5))

        ctk.CTkCheckBox(self.frame, text="Etsi myös alikansioista", variable=self.subfolders_var).grid(
            row=2, column=1, columnspan=2, sticky="w", pady=(0, 10)
        )

        ctk.CTkLabel(self.frame, text="Kohdekansio:").grid(row=3, column=0, sticky="w", padx=30, pady=10)
        ctk.CTkEntry(self.frame, textvariable=self.dest_folder).grid(row=3, column=1, sticky="ew", padx=(0, 10))
        ctk.CTkButton(self.frame, text="Selaa...", command=self.browse_dest, width=80).grid(row=3, column=2, padx=(0, 30))

        ctk.CTkLabel(self.frame, text="Nimeämistapa:").grid(row=4, column=0, sticky="w", padx=30, pady=10)
        style_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        style_frame.grid(row=4, column=1, columnspan=2, sticky="w")
        ctk.CTkRadioButton(style_frame, text="Etuliite + Numero", variable=self.naming_style, value="number").pack(side="left", padx=(0, 15))
        ctk.CTkRadioButton(style_frame, text="Etuliite + Alkuperäinen nimi", variable=self.naming_style, value="original").pack(side="left")

        ctk.CTkLabel(self.frame, text="Nimen etuliite:").grid(row=5, column=0, sticky="w", padx=30, pady=10)
        ctk.CTkEntry(self.frame, textvariable=self.prefix).grid(row=5, column=1, sticky="ew", padx=(0, 10))

        ctk.CTkLabel(self.frame, text="Uusi formaatti:").grid(row=6, column=0, sticky="w", padx=30, pady=10)
        formats = ["PNG", "JPEG", "WEBP", "BMP", "ICO"]
        self.format_dropdown = ctk.CTkComboBox(self.frame, variable=self.output_format, values=formats, command=self.on_format_change)
        self.format_dropdown.grid(row=6, column=1, sticky="w", padx=(0, 10))

        self.quality_label = ctk.CTkLabel(self.frame, text=f"Pakkauslaatu ({self.quality_var.get()}%):", text_color="gray")
        self.quality_label.grid(row=7, column=0, sticky="w", padx=30, pady=10)

        self.quality_slider = ctk.CTkSlider(self.frame, from_=1, to=100, variable=self.quality_var, command=self.update_quality_label, state="disabled")
        self.quality_slider.grid(row=7, column=1, sticky="we", padx=(0, 10))

        ctk.CTkCheckBox(self.frame, text="Muuta kuvien kokoa", variable=self.resize_var, command=self.toggle_resize).grid(
            row=8, column=0, columnspan=2, sticky="w", padx=30, pady=(15, 5)
        )

        dim_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        dim_frame.grid(row=9, column=0, columnspan=3, sticky="w", padx=30)
        ctk.CTkLabel(dim_frame, text="Leveys:").pack(side="left")
        self.width_entry = ctk.CTkEntry(dim_frame, textvariable=self.width_var, width=80, state="disabled")
        self.width_entry.pack(side="left", padx=(10, 20))

        ctk.CTkLabel(dim_frame, text="Korkeus:").pack(side="left")
        self.height_entry = ctk.CTkEntry(dim_frame, textvariable=self.height_var, width=80, state="disabled")
        self.height_entry.pack(side="left", padx=(10, 10))

        self.crop_checkbox = ctk.CTkCheckBox(self.frame, text="Rajaa keskitetysti (Crop)", variable=self.crop_var, state="disabled")
        self.crop_checkbox.grid(row=10, column=0, columnspan=3, sticky="w", padx=30, pady=(5, 5))

        info_text = "(Jätä toinen tyhjäksi säilyttääksesi kuvasuhteen. Rajaus vaatii molemmat mitat.)"
        ctk.CTkLabel(self.frame, text=info_text, text_color="gray", font=ctk.CTkFont(size=11)).grid(
            row=11, column=0, columnspan=3, sticky="w", padx=30, pady=(0, 10)
        )

        self.exif_checkbox = ctk.CTkCheckBox(self.frame, text="Korjaa puhelinkuvien asento automaattisesti", variable=self.exif_fix_var)
        self.exif_checkbox.grid(row=12, column=0, columnspan=3, sticky="w", padx=30, pady=(10, 5))

        self.meta_checkbox = ctk.CTkCheckBox(self.frame, text="Poista kaikki metadata (GPS, Kamera jne.) - Säästää tilaa", variable=self.strip_meta_var)
        self.meta_checkbox.grid(row=13, column=0, columnspan=3, sticky="w", padx=30, pady=(5, 10))

        self.start_button = ctk.CTkButton(
            self.frame, text="Aloita käsittely", font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2FA572", hover_color="#106A43", command=self.start_processing_thread
        )
        self.start_button.grid(row=14, column=0, columnspan=3, pady=(15, 10), ipadx=20, ipady=5)

        self.progress_bar = ctk.CTkProgressBar(self.frame, width=400)
        self.progress_bar.grid(row=15, column=0, columnspan=3, pady=(10, 5))
        self.progress_bar.set(0)
        self.progress_bar.grid_remove()

        self.status_label = ctk.CTkLabel(self.frame, text="Valmis.", text_color="gray")
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
        self.quality_label.configure(text=f"Pakkauslaatu ({int(value)}%):")

    def update_ui(self, progress_val, status_text, status_color="gray"):
        self.progress_bar.set(progress_val)
        self.status_label.configure(text=status_text, text_color=status_color)

    def finish_processing(self, success_msg=None, error_msg=None):
        self.start_button.configure(state="normal")
        self.progress_bar.grid_remove()
        self.save_settings()
        if error_msg:
            messagebox.showerror("Virhe", error_msg)
            self.status_label.configure(text="Virhe tapahtui.", text_color="red")
        elif success_msg:
            messagebox.showinfo("Valmis", success_msg)

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
            messagebox.showerror("Virhe", "Valitse sekä lähde- että kohdekansio!")
            return

        if not os.path.isdir(src):
            messagebox.showerror("Virhe", "Valittua lähdekansiota ei ole olemassa!")
            return

        if do_resize:
            w_str = self.width_var.get().strip()
            h_str = self.height_var.get().strip()
            if not w_str and not h_str:
                messagebox.showerror("Virhe", "Syötä vähintään leveys tai korkeus kuvien koon muutosta varten!")
                return
            try:
                target_w = int(w_str) if w_str else None
                target_h = int(h_str) if h_str else None
                if (target_w is not None and target_w <= 0) or (target_h is not None and target_h <= 0):
                    raise ValueError
            except ValueError:
                messagebox.showerror("Virhe", "Mittojen täytyy olla nollaa suurempia kokonaislukuja!")
                return

            if do_crop and (target_w is None or target_h is None):
                messagebox.showerror("Virhe", "Keskitetty rajaus vaatii ehdottomasti sekä leveyden että korkeuden!")
                return

        os.makedirs(dest, exist_ok=True)
        self.start_button.configure(state="disabled")
        self.progress_bar.grid()
        self.progress_bar.set(0)
        self.status_label.configure(text="Etsitään kuvia...", text_color="#3A7EBF")

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
                self.frame.after(0, self.finish_processing, None, "Lähdekansiosta ei löytynyt tuettuja kuvia.")
                return

            ext_map = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp", "BMP": ".bmp", "ICO": ".ico"}
            extension = ext_map.get(out_format, f".{out_format.lower()}")

            count = 1
            for i, filepath in enumerate(files_to_process):
                filename = os.path.basename(filepath)
                try:
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
                    print(f"Virhe käsiteltäessä kuvaa {filename}: {e}")

                progress = (i + 1) / total_files
                status_text = f"Käsitellään kuvia: {i + 1}/{total_files} ({filename})"
                self.frame.after(0, self.update_ui, progress, status_text, "#3A7EBF")

            success_msg = f"Käsittely suoritettu onnistuneesti!\nKäsitellyt kuvat: {count - 1} kpl"
            self.frame.after(0, self.update_ui, 1.0, f"Käsittely valmis! {count - 1} kuvaa siirretty ja muunnettu.", "#2FA572")
            self.frame.after(100, self.finish_processing, success_msg, None)

        except Exception as e:
            self.frame.after(0, self.finish_processing, None, f"Kriittinen virhe: {str(e)}")


class ThemeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Theme Studio")
        self.geometry("960x720")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.selected_folder = None
        self.selected_folder_icon = None

        self.current_state = {
            "dark_mode": True,
            "wallpaper": None,
            "auto_accent_from_wp": True,
            "accent_color": "#0078D4",
            "color_taskbar": True,
            "color_borders": True,
            "extracted_palette": [],
            "cursors": {"Arrow": None, "Hand": None, "IBeam": None, "AppStarting": None},
            "system_icons": {"this_pc": None, "recycle_bin": None, "user_files": None},
            "folders": {}
        }
        self.icon_preview_labels = {}
        self.cursor_labels = {}

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main_views()
        self.show_view("theme")

        windnd.hook_dropfiles(self, func=self.on_drop_files)

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        title = ctk.CTkLabel(self.sidebar, text="🎨 Theme Studio", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(padx=20, pady=(25, 20))

        ctk.CTkButton(self.sidebar, text="Teema & Värit", command=lambda: self.show_view("theme")).pack(padx=20, pady=7, fill="x")
        ctk.CTkButton(self.sidebar, text="Järjestelmäkuvakkeet", command=lambda: self.show_view("icons")).pack(padx=20, pady=7, fill="x")
        ctk.CTkButton(self.sidebar, text="Hiiriosoittimet", command=lambda: self.show_view("cursors")).pack(padx=20, pady=7, fill="x")
        ctk.CTkButton(self.sidebar, text="Kansioiden kuvakkeet", command=lambda: self.show_view("folders")).pack(padx=20, pady=7, fill="x")
        ctk.CTkButton(self.sidebar, text="🖼️ Kuvien hallinta", command=lambda: self.show_view("img_mgr")).pack(padx=20, pady=7, fill="x")
        ctk.CTkButton(self.sidebar, text="💾 Teemaprofiilit", command=lambda: self.show_view("profiles")).pack(padx=20, pady=7, fill="x")

        author_label = ctk.CTkLabel(
            self.sidebar,
            text="tommi.jalkanen@gmail.com\n© 2026 Theme Studio",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        author_label.pack(side="bottom", pady=(0, 10))

        btn_reset = ctk.CTkButton(
            self.sidebar, text="Palauta järjestelmäoletukset", fg_color="#8B0000", hover_color="#5A0000",
            command=self.reset_defaults
        )
        btn_reset.pack(side="bottom", padx=20, pady=(0, 15), fill="x")

    def _build_main_views(self):
        # 1. TEEMA & VÄRIT
        self.view_theme = ctk.CTkFrame(self, corner_radius=12)
        ctk.CTkLabel(self.view_theme, text="Teema, Taustakuva & Väripaletti", font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=30, pady=(25, 10))

        self.dark_switch = ctk.CTkSwitch(self.view_theme, text="Windowsin Tumma tila (Dark Mode)", command=self.toggle_dark_mode, font=ctk.CTkFont(size=14))
        self.dark_switch.select()
        self.dark_switch.pack(anchor="w", padx=30, pady=8)

        wp_frame = ctk.CTkFrame(self.view_theme)
        wp_frame.pack(fill="x", padx=30, pady=8)

        ctk.CTkLabel(wp_frame, text="Työpöydän taustakuva & Älykäs väripaletti:", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=15, pady=(10, 2))
        self.wp_label = ctk.CTkLabel(wp_frame, text="Ei tiedostoa valittuna", text_color="gray")
        self.wp_label.pack(anchor="w", padx=15, pady=(0, 6))

        wp_btn_row = ctk.CTkFrame(wp_frame, fg_color="transparent")
        wp_btn_row.pack(fill="x", padx=15, pady=(0, 8))

        ctk.CTkButton(wp_btn_row, text="Valitse taustakuva...", command=self.pick_wallpaper).pack(side="left", padx=(0, 10))
        self.palette_container = ctk.CTkFrame(wp_btn_row, fg_color="transparent")
        self.palette_container.pack(side="left", padx=5)
        self._build_empty_palette_preview()

        self.chk_auto_wp_color = ctk.CTkCheckBox(wp_frame, text="Ota taustakuvan 1. väri käyttöön automaattisesti")
        self.chk_auto_wp_color.select()
        self.chk_auto_wp_color.pack(anchor="w", padx=15, pady=(0, 10))

        color_frame = ctk.CTkFrame(self.view_theme)
        color_frame.pack(fill="x", padx=30, pady=8)

        ctk.CTkLabel(color_frame, text="Windowsin aktiivinen korostusväri:", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=15, pady=(10, 6))
        picker_row = ctk.CTkFrame(color_frame, fg_color="transparent")
        picker_row.pack(fill="x", padx=15, pady=4)

        self.color_swatch = ctk.CTkFrame(picker_row, width=42, height=36, corner_radius=6, fg_color="#0078D4", border_width=2, border_color="white")
        self.color_swatch.pack(side="left", padx=(0, 12))

        self.lbl_hex_color = ctk.CTkLabel(picker_row, text="#0078D4", font=ctk.CTkFont(family="Consolas", size=15, weight="bold"), width=80, anchor="w")
        self.lbl_hex_color.pack(side="left", padx=(0, 10))

        ctk.CTkButton(picker_row, text="🎨 Valitse mukautettu...", width=150, command=self.open_color_picker).pack(side="left", padx=(0, 15))

        for hex_val in ["#0078D4", "#00E5FF", "#8E24AA", "#00C853", "#FFAB00"]:
            ctk.CTkButton(
                picker_row, text="", width=26, height=26, corner_radius=13,
                fg_color=hex_val, hover_color=hex_val,
                command=lambda h=hex_val: self.apply_selected_color(h)
            ).pack(side="left", padx=2)

        opts_row = ctk.CTkFrame(color_frame, fg_color="transparent")
        opts_row.pack(fill="x", padx=15, pady=(8, 12))

        self.chk_taskbar = ctk.CTkCheckBox(opts_row, text="Värjää tehtäväpalkki ja aloitusvalikko", command=self.refresh_accent_options)
        self.chk_taskbar.select()
        self.chk_taskbar.pack(side="left", padx=(0, 25))

        self.chk_borders = ctk.CTkCheckBox(opts_row, text="Värjää otsikkopalkit ja ikkunoiden reunat", command=self.refresh_accent_options)
        self.chk_borders.select()
        self.chk_borders.pack(side="left")

        # 2. JÄRJESTELMÄKUVAKKEET
        self.view_icons = ctk.CTkFrame(self, corner_radius=12)
        ctk.CTkLabel(self.view_icons, text="Työpöydän järjestelmäkuvakkeet", font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=30, pady=(25, 5))
        ctk.CTkLabel(self.view_icons, text="Voit valita suoraan .ico tai .png tiedoston (PNG muunnetaan automaattisesti).", text_color="gray").pack(anchor="w", padx=30, pady=(0, 20))

        self._create_icon_row(self.view_icons, "💻 Tämä tietokone", CLSID_THIS_PC, "this_pc", False)
        self._create_icon_row(self.view_icons, "🗑️ Roskakori", CLSID_RECYCLE_BIN, "recycle_bin", True)
        self._create_icon_row(self.view_icons, "📁 Käyttäjän kansio", CLSID_USER_FILES, "user_files", False)

        # 3. HIIRIOSOITTIMET
        self.view_cursors = ctk.CTkFrame(self, corner_radius=12)
        ctk.CTkLabel(self.view_cursors, text="Hiiren osoittimet (Kursorit)", font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=30, pady=(25, 5))
        ctk.CTkLabel(self.view_cursors, text="Valitse mukautetut .cur tai .ani tiedostot eri kursoritiloille.", text_color="gray").pack(anchor="w", padx=30, pady=(0, 20))

        self._create_cursor_row(self.view_cursors, "🖱️ Normaali nuoli (Arrow)", "Arrow")
        self._create_cursor_row(self.view_cursors, "🔗 Linkkiosoitin (Hand)", "Hand")
        self._create_cursor_row(self.view_cursors, "📝 Tekstikursori (IBeam)", "IBeam")
        self._create_cursor_row(self.view_cursors, "⏳ Taustatyö (AppStarting)", "AppStarting")

        # 4. KANSIOIDEN KUVAKKEET
        self.view_folders = ctk.CTkFrame(self, corner_radius=12)
        ctk.CTkLabel(self.view_folders, text="Kansioiden kustomointi (desktop.ini)", font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=30, pady=(25, 5))
        ctk.CTkLabel(self.view_folders, text="Raahaa (Drag & Drop) kansio ja PNG/ICO-kuva suoraan tähän ikkunaan tai valitse ne alta.", text_color="gray").pack(anchor="w", padx=30, pady=(0, 15))

        self.drop_zone = ctk.CTkFrame(self.view_folders, height=130, border_width=2, border_color="#3B8ED0")
        self.drop_zone.pack(fill="x", padx=30, pady=10)
        self.drop_zone.pack_propagate(False)

        self.drop_label = ctk.CTkLabel(self.drop_zone, text="📥 Raahaa kansio tai kuvake (.png / .ico) tähän", font=ctk.CTkFont(size=16, weight="bold"), text_color="#3B8ED0")
        self.drop_label.place(relx=0.5, rely=0.5, anchor="center")

        status_frame = ctk.CTkFrame(self.view_folders)
        status_frame.pack(fill="x", padx=30, pady=10)

        f_row = ctk.CTkFrame(status_frame, fg_color="transparent")
        f_row.pack(fill="x", padx=15, pady=(12, 6))
        ctk.CTkLabel(f_row, text="Kohdekansio:", font=ctk.CTkFont(weight="bold"), width=110, anchor="w").pack(side="left")
        self.lbl_folder_path = ctk.CTkLabel(f_row, text="Ei valittuna", text_color="gray", anchor="w")
        self.lbl_folder_path.pack(side="left", fill="x", expand=True, padx=10)
        ctk.CTkButton(f_row, text="Selaa kansio...", width=120, command=self.browse_folder).pack(side="right")

        i_row = ctk.CTkFrame(status_frame, fg_color="transparent")
        i_row.pack(fill="x", padx=15, pady=(6, 12))
        ctk.CTkLabel(i_row, text="Uusi kuvake:", font=ctk.CTkFont(weight="bold"), width=110, anchor="w").pack(side="left")
        self.lbl_folder_icon = ctk.CTkLabel(i_row, text="Ei valittuna", text_color="gray", anchor="w")
        self.lbl_folder_icon.pack(side="left", fill="x", expand=True, padx=10)
        self.folder_icon_preview = ctk.CTkLabel(i_row, text="")
        self.folder_icon_preview.pack(side="left", padx=10)
        ctk.CTkButton(i_row, text="Selaa kuva...", width=120, command=self.browse_folder_icon).pack(side="right")

        action_row = ctk.CTkFrame(self.view_folders, fg_color="transparent")
        action_row.pack(fill="x", padx=30, pady=15)
        ctk.CTkButton(action_row, text="✨ Aseta kansion kuvake", height=40, font=ctk.CTkFont(size=14, weight="bold"), command=self.apply_folder_icon).pack(side="left", expand=True, fill="x", padx=(0, 10))
        ctk.CTkButton(action_row, text="Palauta kansion oletus", height=40, fg_color="#444444", hover_color="#333333", command=self.clear_folder_icon).pack(side="right", padx=(10, 0))

        # 5. KUVIEN HALLINTA
        self.view_img_mgr = ctk.CTkScrollableFrame(self, corner_radius=12)
        self.image_manager_instance = ImageManagerWidget(self.view_img_mgr)

        # 6. TEEMAPROFIILIT
        self.view_profiles = ctk.CTkFrame(self, corner_radius=12)
        ctk.CTkLabel(self.view_profiles, text="Teemaprofiilit (JSON)", font=ctk.CTkFont(size=22, weight="bold")).pack(anchor="w", padx=30, pady=(25, 5))
        ctk.CTkLabel(self.view_profiles, text="Tallenna nykyiset asetukset tai lataa profiili.", text_color="gray").pack(anchor="w", padx=30, pady=(0, 15))

        save_box = ctk.CTkFrame(self.view_profiles)
        save_box.pack(fill="x", padx=30, pady=5)
        self.entry_profile_name = ctk.CTkEntry(save_box, placeholder_text="Anna uuden profiilin nimi...", height=36)
        self.entry_profile_name.pack(side="left", fill="x", expand=True, padx=(15, 10), pady=12)
        ctk.CTkButton(save_box, text="💾 Tallenna nykyinen", height=36, command=self.save_current_profile).pack(side="left", padx=(0, 10), pady=12)
        ctk.CTkButton(save_box, text="📂 Tuo .json...", width=110, height=36, fg_color="#444444", hover_color="#333333", command=self.import_external_profile).pack(side="right", padx=(0, 15), pady=12)

        ctk.CTkLabel(self.view_profiles, text="Tallennetut profiilit:", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=30, pady=(15, 5))
        self.profiles_list_frame = ctk.CTkScrollableFrame(self.view_profiles, height=270)
        self.profiles_list_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

    def _create_icon_row(self, parent, title, clsid, tag, is_bin):
        row = ctk.CTkFrame(parent)
        row.pack(fill="x", padx=30, pady=8)
        ctk.CTkLabel(row, text=title, font=ctk.CTkFont(size=15, weight="bold"), width=180, anchor="w").pack(side="left", padx=15, pady=15)
        preview_lbl = ctk.CTkLabel(row, text="Oletus / Nykyinen", text_color="gray")
        preview_lbl.pack(side="left", padx=10)
        self.icon_preview_labels[tag] = preview_lbl
        ctk.CTkButton(row, text="Vaihda kuvake...", width=140, command=lambda: self.pick_icon(clsid, tag, is_bin, preview_lbl)).pack(side="right", padx=15, pady=15)

    def _create_cursor_row(self, parent, title, cursor_key):
        row = ctk.CTkFrame(parent)
        row.pack(fill="x", padx=30, pady=8)
        ctk.CTkLabel(row, text=title, font=ctk.CTkFont(size=15, weight="bold"), width=220, anchor="w").pack(side="left", padx=15, pady=15)
        lbl_path = ctk.CTkLabel(row, text="Oletuskursori", text_color="gray", anchor="w")
        lbl_path.pack(side="left", fill="x", expand=True, padx=10)
        self.cursor_labels[cursor_key] = lbl_path
        ctk.CTkButton(row, text="Valitse .cur / .ani...", width=150, command=lambda: self.pick_cursor_file(cursor_key, lbl_path)).pack(side="right", padx=15, pady=15)

    def show_view(self, name: str):
        for v in (self.view_theme, self.view_icons, self.view_cursors, self.view_folders, self.view_img_mgr, self.view_profiles):
            v.grid_forget()
        if name == "theme":
            self.view_theme.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
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

    def pick_cursor_file(self, cursor_key: str, lbl_widget):
        path = filedialog.askopenfilename(filetypes=[("Hiiriosoittimet", "*.cur *.ani")])
        if path:
            abs_p = os.path.abspath(path)
            self.current_state["cursors"][cursor_key] = abs_p
            lbl_widget.configure(text=os.path.basename(abs_p), text_color="white")
            WindowsThemeEngine.set_cursors({cursor_key: abs_p})

    def _build_empty_palette_preview(self):
        for w in self.palette_container.winfo_children():
            w.destroy()
        ctk.CTkLabel(self.palette_container, text="(Valitse taustakuva)", text_color="gray", font=ctk.CTkFont(size=12)).pack(side="left", padx=5)

    def _update_dynamic_palette(self, colors: list):
        for w in self.palette_container.winfo_children():
            w.destroy()
        ctk.CTkLabel(self.palette_container, text="Sävyt:", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(5, 6))
        for hex_val in colors:
            ctk.CTkButton(
                self.palette_container, text="", width=26, height=26, corner_radius=13,
                fg_color=hex_val, hover_color=hex_val,
                command=lambda h=hex_val: self.apply_selected_color(h)
            ).pack(side="left", padx=2)

    def open_color_picker(self):
        color = colorchooser.askcolor(initialcolor=self.current_state["accent_color"], title="Valitse korostusväri")
        if color and color[1]:
            self.apply_selected_color(color[1].upper())

    def apply_selected_color(self, hex_color: str):
        hex_upper = hex_color.upper()
        self.current_state["accent_color"] = hex_upper
        self.current_state["color_taskbar"] = bool(self.chk_taskbar.get())
        self.current_state["color_borders"] = bool(self.chk_borders.get())

        self.color_swatch.configure(fg_color=hex_upper)
        self.lbl_hex_color.configure(text=hex_upper)

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

    def save_current_profile(self):
        raw_name = self.entry_profile_name.get().strip()
        if not raw_name:
            messagebox.showwarning("Anna nimi", "Kirjoita profiilille nimi ennen tallennusta!")
            return
        safe_name = "".join(c for c in raw_name if c.isalnum() or c in (" ", "-", "_")).strip()
        file_path = os.path.join(PROFILES_DIR, f"{safe_name}.json")
        payload = {
            "name": raw_name,
            "dark_mode": bool(self.dark_switch.get()),
            "wallpaper": self.current_state["wallpaper"],
            "auto_accent_from_wp": bool(self.chk_auto_wp_color.get()),
            "accent_color": self.current_state["accent_color"],
            "color_taskbar": bool(self.chk_taskbar.get()),
            "color_borders": bool(self.chk_borders.get()),
            "extracted_palette": self.current_state["extracted_palette"],
            "cursors": self.current_state["cursors"],
            "system_icons": self.current_state["system_icons"],
            "folders": self.current_state["folders"]
        }
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=4, ensure_ascii=False)
            self.entry_profile_name.delete(0, "end")
            self.refresh_profiles_list()
            messagebox.showinfo("Tallennettu", f"Profiili '{raw_name}' tallennettiin onnistuneesti!")
        except Exception as e:
            messagebox.showerror("Virhe", f"Virhe tallennuksessa:\n{e}")

    def import_external_profile(self):
        path = filedialog.askopenfilename(filetypes=[("JSON Profiili", "*.json")])
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
                messagebox.showerror("Virhe", f"Tuonti epäonnistui:\n{e}")

    def refresh_profiles_list(self):
        for widget in self.profiles_list_frame.winfo_children():
            widget.destroy()
        files = sorted([f for f in os.listdir(PROFILES_DIR) if f.endswith(".json")])
        if not files:
            ctk.CTkLabel(self.profiles_list_frame, text="Ei tallennettuja profiileja.", text_color="gray").pack(pady=30)
            return

        for fname in files:
            fpath = os.path.join(PROFILES_DIR, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                continue

            prof_name = data.get("name", fname[:-5])
            mode_txt = "🌙 Tumma" if data.get("dark_mode", True) else "☀️ Vaalea"
            accent_hex = data.get("accent_color", "#0078D4")

            card = ctk.CTkFrame(self.profiles_list_frame)
            card.pack(fill="x", padx=5, pady=6)

            ctk.CTkFrame(card, width=18, height=42, corner_radius=4, fg_color=accent_hex).pack(side="left", padx=(12, 5), pady=10)
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)

            ctk.CTkLabel(info_frame, text=prof_name, font=ctk.CTkFont(size=16, weight="bold"), anchor="w").pack(fill="x")
            ctk.CTkLabel(info_frame, text=f"{mode_txt}  •  🎨 {accent_hex}", text_color="gray", font=ctk.CTkFont(size=12), anchor="w").pack(fill="x")

            ctk.CTkButton(card, text="Poista", width=70, fg_color="#6e1c1c", hover_color="#4a1212", command=lambda p=fpath: self.delete_profile(p)).pack(side="right", padx=(5, 15), pady=10)
            ctk.CTkButton(card, text="⚡ Ota käyttöön", width=130, font=ctk.CTkFont(weight="bold"), command=lambda d=data: self.apply_profile(d)).pack(side="right", padx=5, pady=10)

    def apply_profile(self, data: dict):
        try:
            is_dark = data.get("dark_mode", True)
            WindowsThemeEngine.set_dark_mode(is_dark)
            if is_dark: self.dark_switch.select()
            else: self.dark_switch.deselect()

            wp = data.get("wallpaper")
            if wp and os.path.exists(wp):
                WindowsThemeEngine.set_wallpaper(wp)
                self.wp_label.configure(text=os.path.basename(wp), text_color="white")
                self.current_state["wallpaper"] = wp
                palette = data.get("extracted_palette", [])
                if palette:
                    self.current_state["extracted_palette"] = palette
                    self._update_dynamic_palette(palette)

            accent_hex = data.get("accent_color")
            if accent_hex:
                self.apply_selected_color(accent_hex)

            cursors = data.get("cursors", {})
            if cursors:
                WindowsThemeEngine.set_cursors(cursors)
                for c_key, c_path in cursors.items():
                    if c_path and c_path in self.cursor_labels:
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
            messagebox.showinfo("Profiili aktivoitu", "Teemaprofiili otettu käyttöön!")
        except Exception as e:
            messagebox.showerror("Virhe", f"Virhe profiilin latauksessa:\n{e}")

    def delete_profile(self, file_path: str):
        if messagebox.askyesno("Poista", "Haluatko varmasti poistaa tämän profiilin?"):
            os.remove(file_path)
            self.refresh_profiles_list()

    def on_drop_files(self, files):
        self.show_view("folders")
        for raw_path in files:
            path = raw_path.decode("mbcs") if isinstance(raw_path, bytes) else str(raw_path)
            if os.path.isdir(path):
                self._set_selected_folder(path)
            elif path.lower().endswith((".png", ".ico", ".jpg", ".jpeg")):
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
        if folder: self._set_selected_folder(folder)

    def browse_folder_icon(self):
        path = filedialog.askopenfilename(filetypes=[("Kuvat", "*.ico *.png")])
        if path: self._set_selected_folder_icon(path)

    def apply_folder_icon(self):
        if not self.selected_folder or not self.selected_folder_icon:
            messagebox.showwarning("Puuttuu", "Valitse tai raahaa kansio ja kuvake!")
            return
        WindowsThemeEngine.set_folder_icon(self.selected_folder, self.selected_folder_icon)
        self.current_state["folders"][os.path.abspath(self.selected_folder)] = os.path.abspath(self.selected_folder_icon)
        messagebox.showinfo("Valmis", "Kansion kuvake päivitetty!")

    def clear_folder_icon(self):
        if not self.selected_folder:
            messagebox.showwarning("Valitse", "Valitse ensin kansio.")
            return
        WindowsThemeEngine.reset_folder_icon(self.selected_folder)
        self.current_state["folders"].pop(os.path.abspath(self.selected_folder), None)
        messagebox.showinfo("Valmis", "Kansion oletuskuvake palautettu.")

    def toggle_dark_mode(self):
        WindowsThemeEngine.set_dark_mode(bool(self.dark_switch.get()))

    def pick_wallpaper(self):
        path = filedialog.askopenfilename(filetypes=[("Kuvat", "*.jpg *.jpeg *.png *.bmp")])
        if path:
            abs_p = os.path.abspath(path)
            WindowsThemeEngine.set_wallpaper(abs_p)
            self.current_state["wallpaper"] = abs_p
            self.wp_label.configure(text=os.path.basename(abs_p), text_color="white")
            try:
                top_colors = WindowsThemeEngine.extract_top_colors(abs_p, n=5)
                self.current_state["extracted_palette"] = top_colors
                self._update_dynamic_palette(top_colors)
                if self.chk_auto_wp_color.get() and top_colors:
                    self.apply_selected_color(top_colors[0])
            except Exception as e:
                print(f"Värivirhe: {e}")

    def pick_icon(self, clsid, tag, is_bin, preview_lbl):
        path = filedialog.askopenfilename(filetypes=[("Kuvat", "*.ico *.png")])
        if path:
            img = Image.open(path)
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(32, 32))
            preview_lbl.configure(image=ctk_img, text="")
            WindowsThemeEngine.set_clsid_icon(clsid, path, tag, is_bin)
            self.current_state["system_icons"][tag] = os.path.abspath(path)

    def reset_defaults(self):
        if messagebox.askyesno("Oletukset", "Palautetaanko järjestelmän oletuskuvakkeet ja kursorit?"):
            WindowsThemeEngine.restore_default_icons()
            WindowsThemeEngine.restore_default_cursors()
            messagebox.showinfo("Valmis", "Oletukset palautettu!")


if __name__ == "__main__":
    app = ThemeApp()
    app.mainloop()
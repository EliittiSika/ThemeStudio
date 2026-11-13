# 🎨 Theme Studio V.2

**Theme Studio V.2** is a comprehensive Windows desktop customization, theming, icon/cursor engineering, and batch image processing suite built with Python, CustomTkinter, and native Win32 APIs.

---

## ✨ Key Features in V.2

### 1. 🎨 Theme, Taskbar Transparency & File Explorer Manager
* **System & Explorer Theme Control:** Switch seamlessly between **Dark**, **Light**, and **Mixed (Dark System / Light Apps)** modes, and toggle **Compact File Explorer Spacing**. Includes a one-click `explorer.exe` restart utility.
* **Live Taskbar Transparency & Glass Engine (Win32 DWM):** Apply real-time **Clear Transparent**, **Blur**, **Acrylic**, or **Opaque** composition effects directly to the Windows Taskbar (`Shell_TrayWnd`) with customizable opacity and a background keep-alive option.
* **Smart Wallpaper & 5-Shade Palette Extraction:** Set desktop wallpapers with custom fit modes (*Fill, Fit, Stretch, Tile, Center, Span*) and automatically extract the 5 most vibrant, balanced accent shades into interactive palette buttons.
* **Windows Accent Color Engine:** Dynamically generates a 32-byte 8-shade binary `AccentPalette` and updates DWM title bars, window borders, start menu, and taskbar colors on the fly.
* **Typography & Live UI Preview:** Test fonts, styles (*Regular, Bold, Italic, Bold Italic*), and colors against a live interactive preview window before applying changes, complete with **Undo** support.
* **Developer Export (CSS / Tailwind / JSON):** Export your active color palette and typography directly into ready-to-use `:root` CSS variables and `tailwind.config.js` snippets.

### 2. 🖼️ Interactive Image Gallery
* **Recursive Wallpaper Browser:** Browse images across folders and subfolders (supports `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`).
* **Lightbox Full Preview:** Inspect high-resolution previews and image dimensions in a dedicated modal window.
* **One-Click Actions:** Set any gallery image as your desktop wallpaper, extract its color palette *without* changing your wallpaper, assign it as a folder icon, or send it directly to the Cursor Creator or Batch Processor.

### 3. 💻 Desktop System Icons & Icon Packs (`.zip`)
* **Native CLSID Icon Customization:** Customize desktop icons for **This PC**, **Recycle Bin** (empty & full states), and **User's Files**. Automatically converts `.png` images into multi-resolution `.ico` files (`16x16` up to `256x256`).
* **Icon Pack Import & Export (`.zip`):** Bundle your current system icons into a shareable `.zip` Icon Pack or import and apply external icon packs with one click.

### 4. 🖱️ Mouse Pointers, Cursor Packs (`.zip`) & Image-to-Cursor Creator
* **Custom Cursor States:** Assign `.cur` or `.ani` files to *Normal Select (Arrow)*, *Link Select (Hand)*, *Text Select (IBeam)*, and *Working in Background (AppStarting)*.
* **Built-in Image-to-Cursor (`.cur`) Generator:** Convert any `.png`, `.jpg`, or `.webp` image directly into a native binary Windows `.cur` file. Choose target dimensions (`32x32`, `48x48`, `64x64`) and adjust exact click **Hotspot (X, Y)** coordinates with a live crosshair preview.
* **Cursor Pack Import & Export (`.zip`):** Export your active cursor set to a `.zip` archive or import complete cursor packs.

### 5. 📁 Folder Icon Customizer (`desktop.ini` + Drag & Drop)
* **Smart Drag & Drop:** Drag any folder and `.png`/`.ico` image directly onto the application window to assign custom folder icons.
* **Automatic Attribute & Cache Handling:** Automatically generates hashed `.ico` resources, writes `desktop.ini`, sets `Hidden`/`System`/`Read-Only` Win32 file attributes, and triggers `SHChangeNotify` so Windows Explorer updates immediately.

### 6. ⚙️ Batch Image Processing Studio
* **Bulk Format Conversion:** Convert entire folders (and subfolders) of images into `PNG`, `JPEG`, `WEBP`, `BMP`, multi-size `ICO`, or native Windows `CUR` cursors.
* **Resize & Center Crop:** Maintain aspect ratio automatically or center-crop to exact pixel dimensions.
* **EXIF & Metadata Tools:** Auto-fix smartphone photo orientation and strip EXIF/GPS metadata to save disk space.

### 7. 💾 Theme Profiles, Portable Theme Packs (`.zip`) & Day/Night Scheduler
* **JSON Theme Profiles:** Save and apply your entire desktop state (mode, wallpaper, palette, taskbar effect, icons, cursors, and customized folders) with a single click.
* **Portable Full Theme Packs (`.zip`):** Bundle the JSON profile *along with* all referenced wallpaper, icon, and cursor files into a self-contained `.zip` archive that works across different PCs.
* **Automatic Day / Night Theme Switcher:** Schedule distinct Day and Night profiles to activate automatically at your chosen times (e.g., `07:00` and `20:00`).

---

## 🛠️ Running & Building from Source

### Prerequisites
* Windows 10 / 11
* Python 3.10+

Install dependencies inside your virtual environment:
```powershell
.\.venv\Scripts\python.exe -m pip install customtkinter pillow windnd pyinstaller

🇫🇮 Yhteenveto suomeksi (Theme Studio V.2)
Theme Studio V.2 on monipuolinen Windowsin kustomointi-, teema- ja kuvankäsittelyohjelmisto:

Teemat, tehtäväpalkin läpinäkyvyys & Resurssienhallinta: Hallitse tummaa/vaaleaa tilaa, tehtäväpalkin reaaliaikaista lasi-/läpinäkyvyystehostetta (Clear, Blur, Acrylic) sekä taustakuvasta automaattisesti poimittavaa 5 sävyn väripalettia.

Kehittäjävienti: Vie väripaletti ja fontit suoraan CSS-muuttujiksi tai Tailwind-asetuksiksi.

Kuvagalleria: Selaa taustakuvia alikansioineen, esikatsele täydessä koossa, poimi pelkkä väripaletti tai lähetä kuva suoraan kursorityökaluun.

Järjestelmä- ja kansiokuvakkeet + Icon Pack (.zip): Vaihda työpöydän järjestelmäkuvakkeet ja kansioiden kuvakkeet (Drag & Drop) tai tuo/vie kuvakepaketteja .zip-muodossa.

Hiiriosoittimet, Cursor Pack (.zip) & Kursorinluonti kuvasta: Luo aitoja .cur-osoittimia mistä tahansa kuvasta säädettävällä Hotspot (X, Y) -tähtäimellä.

Kuvien massakäsittely: Muunna, rajaa ja skaalaa kokonaisia kuvakansioita (PNG, JPEG, WEBP, BMP, ICO, CUR).

Profiilit, Theme Pack (.zip) & Päivä/Yö-ajastin: Tallenna teemat JSON-profiileiksi, jaa koko teema tiedostoineen yhtenä .zip-pakettina ja ajasta automaattinen päivä- ja yöteeman vaihto.

📄 Copyright & License
Copyright © 2026 Tommi Jalkanen. All rights reserved.

Contact: tommi.jalkanen@gmail.com

This software and its source code are proprietary. See the License file for details.
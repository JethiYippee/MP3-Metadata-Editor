# MP3 Metadata Editor 🎵

A simple dark mode popup app to edit MP3 metadata and album cover art.

## ✨ Features
- Edit MP3 metadata: Title, Artist, Album, Genre, Date
- View and change the album cover image 🖼️
- Modern dark mode UI 🌙

## 🚀 How to Use
1. **Run the App**
   - Double-click `music_metadata_editor.exe` in the `dist` folder.
2. **Upload an MP3**
   - Click `Upload MP3` and select your file.
3. **Edit Metadata**
   - Change any of the fields (Title, Artist, Album, Genre, Date).
   - Click `Save Metadata` to apply changes.
4. **Change/View Album Cover**
   - Click `Change Song Cover` to select a new image (JPG/PNG).
   - Click `View` to preview the current cover art.

## 🛠️ Build from Source
1. Install requirements:
   ```sh
   pip install -r requirements.txt
   ```
2. Build the executable:
   ```sh
   pyinstaller --onefile --noconsole music_metadata_editor.py
   ```
   The `.exe` will be in the `dist` folder.

## 📦 Requirements (for source build)
- Python 3.8+
- mutagen
- customtkinter
- pyinstaller (for building the exe)

## 📄 License
MIT

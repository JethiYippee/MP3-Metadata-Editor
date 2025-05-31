# music_metadata_editor.py
# A simple dark mode popup app to edit MP3 metadata
# Requirements: pip install mutagen customtkinter

import customtkinter as ctk
from tkinter import filedialog, messagebox
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class MetadataEditor(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MP3 Metadata Editor")
        self.geometry("600x390")  # Slightly reduced window height for a more compact appearance
        self.resizable(False, False)
        self.file_path = None

        self.label = ctk.CTkLabel(self, text="Select an MP3 file to edit metadata:")
        self.label.pack(pady=6)

        self.select_btn = ctk.CTkButton(self, text="Upload MP3", command=self.browse_file)
        self.select_btn.pack(pady=5)

        # File name field under Upload MP3, above the title
        filename_frame = ctk.CTkFrame(self)
        filename_frame.pack(pady=(6, 2), fill="x", padx=20)
        filename_label = ctk.CTkLabel(filename_frame, text="File Name", width=100)
        filename_label.pack(side="left")
        self.filename_var = ctk.StringVar()
        self.filename_entry = ctk.CTkEntry(filename_frame, textvariable=self.filename_var, state="readonly", width=450)
        self.filename_entry.pack(side="left", padx=5, fill="x", expand=True)

        self.fields = {}
        for field in ["title", "artist", "album", "genre", "date"]:
            frame = ctk.CTkFrame(self)
            frame.pack(pady=3, fill="x", padx=20)
            lbl = ctk.CTkLabel(frame, text=field.capitalize(), width=100)
            lbl.pack(side="left")
            entry = ctk.CTkEntry(frame, width=450)
            entry.pack(side="left", padx=5, fill="x", expand=True)
            self.fields[field] = entry

        # Album cover buttons in a horizontal frame
        cover_frame = ctk.CTkFrame(self, fg_color="transparent")  # Remove black background
        cover_frame.pack(pady=(8, 2), fill="x", padx=20)
        cover_frame.grid_columnconfigure(0, weight=1)
        cover_frame.grid_columnconfigure(1, weight=0)
        cover_frame.grid_columnconfigure(2, weight=1)
        # Add an empty label to the left for centering
        left_spacer = ctk.CTkLabel(cover_frame, text="", width=1)
        left_spacer.grid(row=0, column=0, sticky="ew")
        self.cover_btn = ctk.CTkButton(cover_frame, text="Change Song Cover", command=self.change_cover, state="disabled", width=180)
        self.cover_btn.grid(row=0, column=1, sticky="ew", padx=(0, 8))
        self.view_cover_btn = ctk.CTkButton(cover_frame, text="View", command=self.view_cover, state="disabled", width=60, height=28)
        self.view_cover_btn.grid(row=0, column=2, sticky="w")
        self.save_btn = ctk.CTkButton(self, text="Save Metadata", command=self.save_metadata, state="disabled")
        self.save_btn.pack(pady=15)

    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
        if path:
            self.file_path = path
            self.filename_var.set(os.path.basename(path))
            self.load_metadata()
            self.save_btn.configure(state="normal")
            self.cover_btn.configure(state="normal")
            self.view_cover_btn.configure(state="normal")

    def load_metadata(self):
        try:
            audio = MP3(self.file_path, ID3=EasyID3)
            for field in self.fields:
                value = audio.tags.get(field, [""])[0] if audio.tags and field in audio.tags else ""
                self.fields[field].delete(0, "end")
                self.fields[field].insert(0, value)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load metadata: {e}")

    def save_metadata(self):
        try:
            audio = MP3(self.file_path, ID3=EasyID3)
            for field, entry in self.fields.items():
                val = entry.get().strip()
                if val:
                    audio.tags[field] = val
                elif field in audio.tags:
                    del audio.tags[field]
            audio.save()
            messagebox.showinfo("Success", "Metadata updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save metadata: {e}")

    def change_cover(self):
        from mutagen.id3 import ID3, APIC, error
        img_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if not img_path or not self.file_path:
            return
        try:
            audio = MP3(self.file_path, ID3=ID3)
            with open(img_path, 'rb') as img:
                img_data = img.read()
            # Remove old cover(s)
            audio.tags.delall('APIC')
            # Add new cover
            audio.tags.add(
                APIC(
                    encoding=3,
                    mime='image/jpeg' if img_path.lower().endswith(('jpg', 'jpeg')) else 'image/png',
                    type=3, desc=u'Cover', data=img_data
                )
            )
            audio.save()
            messagebox.showinfo("Success", "Cover image updated!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update cover: {e}")

    def view_cover(self):
        from mutagen.id3 import ID3
        import tempfile
        import webbrowser
        if not self.file_path:
            return
        try:
            audio = MP3(self.file_path, ID3=ID3)
            apic = None
            for tag in audio.tags.values():
                if tag.FrameID == 'APIC':
                    apic = tag
                    break
            if apic:
                ext = '.jpg' if apic.mime == 'image/jpeg' else '.png'
                with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
                    tmp.write(apic.data)
                    tmp_path = tmp.name
                webbrowser.open(tmp_path)
            else:
                messagebox.showinfo("No Cover", "No cover image found in this MP3.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view cover: {e}")

if __name__ == "__main__":
    app = MetadataEditor()
    app.mainloop()

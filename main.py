import tkinter as tk
from tkinter import filedialog, Toplevel
from reportlab.pdfgen import canvas
from PIL import Image as PilImage, ImageTk
import os

class ImgToPdfConvert:
    def __init__(self, root):
        self.root = root
        self.image_paths = []
        self.output_pdf_name = tk.StringVar()
        self.selected_images_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
        self.theme = tk.StringVar(value="Dark")
        self.initialize_ui()
        self.apply_theme()

    def initialize_ui(self):
        self.root.configure(bg="#1e1e1e")  # Initial background color for dark theme
        
        title_label = tk.Label(self.root, text="Image to PDF Converter", font=("Italian", 16, "bold"))
        title_label.pack(pady=10)
        
        theme_btn = tk.Button(self.root, text="Change Theme", command=self.change_theme, bd=0, highlightthickness=0)
        theme_btn.pack(pady=(0, 10))
        self.round_button(theme_btn)
        
        select_imgs_btn = tk.Button(self.root, text="Select Images", command=self.select_imgs, bd=0, highlightthickness=0)
        select_imgs_btn.pack(pady=(0, 10))
        self.round_button(select_imgs_btn)
        
        self.selected_images_listbox.pack(pady=(0, 10), fill=tk.BOTH, expand=True)
        
        preview_btn = tk.Button(self.root, text="Preview Image", command=self.preview_image, bd=0, highlightthickness=0)
        preview_btn.pack(pady=(0, 10))
        self.round_button(preview_btn)
        
        label = tk.Label(self.root, text="Enter output PDF Name: ")
        label.pack()
        
        pdf_nameentry = tk.Entry(self.root, textvariable=self.output_pdf_name, width=40, justify="center")
        pdf_nameentry.pack()
        
        convert_btn = tk.Button(self.root, text="Convert to PDF", command=self.convert_imgstopdf, bd=0, highlightthickness=0)
        convert_btn.pack(pady=(20, 40))
        self.round_button(convert_btn)

    def apply_theme(self):
        if self.theme.get() == "Dark":
            colors = {
                "bg": "#1e1e1e",
                "fg": "#ffffff",
                "button_bg": "#404040",
                "listbox_bg": "#3b3b3b",
                "entry_bg": "#3b3b3b"
            }
        else:
            colors = {
                "bg": "#f0f0f0",
                "fg": "#000000",
                "button_bg": "#d3d3d3",
                "listbox_bg": "#ffffff",
                "entry_bg": "#ffffff"
            }
        
        self.root.configure(bg=colors["bg"])
        
        for widget in self.root.winfo_children():
            widget.configure(bg=colors.get("bg", widget.cget("bg")), fg=colors.get("fg", widget.cget("fg")))
            if isinstance(widget, tk.Listbox):
                widget.configure(bg=colors["listbox_bg"], fg=colors["fg"])
            elif isinstance(widget, tk.Entry):
                widget.configure(bg=colors["entry_bg"], fg=colors["fg"])
            elif isinstance(widget, tk.Button):
                widget.configure(bg=colors["button_bg"], fg=colors["fg"])
                self.round_button(widget)

    def round_button(self, button):
        button.config(relief=tk.FLAT)
        button.bind("<Enter>", lambda event, b=button: self.on_enter(b))
        button.bind("<Leave>", lambda event, b=button: self.on_leave(b))

    def on_enter(self, button):
        button.config(bg="#505050")

    def on_leave(self, button):
        button.config(bg="#404040")

    def change_theme(self):
        if self.theme.get() == "Dark":
            self.theme.set("Light")
        else:
            self.theme.set("Dark")
        self.apply_theme()

    def select_imgs(self):
        self.image_paths = filedialog.askopenfilenames(title="Select Images", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        self.update_selected_images_listbox()
        
    def update_selected_images_listbox(self):
        self.selected_images_listbox.delete(0, tk.END)
        
        for image_path in self.image_paths:
            _, image_name = os.path.split(image_path)
            self.selected_images_listbox.insert(tk.END, image_name)
    
    def preview_image(self):
        selected_indices = self.selected_images_listbox.curselection()
        if not selected_indices:
            return
        
        selected_index = selected_indices[0]
        image_path = self.image_paths[selected_index]
        
        preview_window = Toplevel(self.root)
        preview_window.title("Image Preview")
        
        image = PilImage.open(image_path)
        image.thumbnail((500, 500))
        img = ImageTk.PhotoImage(image)
        
        label = tk.Label(preview_window, image=img)
        label.image = img  # Keep a reference to avoid garbage collection
        label.pack()
    
    def convert_imgstopdf(self):
        if not self.image_paths:
            return
        
        output_pdf_path = self.output_pdf_name.get() + ".pdf" if self.output_pdf_name.get() else "output.pdf"
        
        pdf = canvas.Canvas(output_pdf_path, pagesize=(612, 792))
        
        for image_path in self.image_paths:
            image = PilImage.open(image_path)
            available_width = 540 
            available_height = 720
            scale_factor = min(available_width / image.width, available_height / image.height)
            n_width = image.width * scale_factor
            n_height = image.height * scale_factor
            x_center = (612 - n_width) / 2
            y_center = (792 - n_height) / 2
            
            pdf.setFillColorRGB(1, 1, 1)
            pdf.rect(0, 0, 612, 792, fill=True)
            pdf.drawInlineImage(image, x_center, y_center, width=n_width, height=n_height)
            pdf.showPage()
            
        pdf.save()
        
def main():
    root = tk.Tk()
    root.title("Image to PDF")
    converter = ImgToPdfConvert(root)
    root.geometry("400x600")
    root.mainloop()
    
if __name__ == "__main__":
    main()

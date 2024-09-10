import os
import random
import shutil
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def get_unlabeled_image():
    manuscript_dir = 'data/manuscript'
    label_dirs = ['data/labels/has_benedicamus', 'data/labels/does_not_have_benedicamus']
    
    all_images = set(os.listdir(manuscript_dir))
    labeled_images = set()
    
    for label_dir in label_dirs:
        if os.path.exists(label_dir):
            labeled_images.update(os.listdir(label_dir))
    
    unlabeled_images = list(all_images - labeled_images)
    
    if not unlabeled_images:
        return None
    
    return os.path.join(manuscript_dir, random.choice(unlabeled_images))

def label_image(image_path, has_benedicamus):
    target_dir = 'data/labels/has_benedicamus' if has_benedicamus else 'data/labels/does_not_have_benedicamus'
    os.makedirs(target_dir, exist_ok=True)
    shutil.copy(image_path, target_dir)

def show_image(image_path):
    root = tk.Tk()
    root.title("Benedicamus Labeling")

    img = Image.open(image_path)
    img = img.resize((800, 600), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(root, image=photo)
    label.image = photo
    label.pack()

    def on_button_click(has_benedicamus):
        label_image(image_path, has_benedicamus)
        root.destroy()

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    btn_yes = tk.Button(btn_frame, text="Has benedicamus", command=lambda: on_button_click(True))
    btn_yes.pack(side=tk.LEFT, padx=10)

    btn_no = tk.Button(btn_frame, text="Does not have benedicamus", command=lambda: on_button_click(False))
    btn_no.pack(side=tk.LEFT, padx=10)

    root.mainloop()

def main():
    while True:
        image_path = get_unlabeled_image()
        if image_path is None:
            messagebox.showinfo("Labeling Complete", "All images have been labeled!")
            break
        show_image(image_path)

if __name__ == "__main__":
    main()

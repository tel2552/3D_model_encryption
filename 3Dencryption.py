import numpy as np
import trimesh
import random
import tkinter as tk
from tkinter import filedialog, messagebox

def shift_triangles_encrypt(faces, shift_value=0):
    # การเลื่อนพิกัด vertices ภายใน triangles
    for i in range(len(faces)):
        # สลับ vertices ภายใน triangle
        random.shuffle(faces[i])
        # เลื่อนพิกัด vertices
        faces[i] = (faces[i] + shift_value) % len(faces) # ตัวอย่างการเลื่อนแบบ cyclic shift

    return faces

def encrypt_file():
    file_path = file_path_var.get()
    save_path = save_path_var.get()
    shift_value = int(shift_entry.get())

    if not file_path or not save_path:
        messagebox.showerror("Error", "Please select input and output files.")
        return

    try:
        mesh = trimesh.load(file_path)

        # เข้ารหัส triangles (พื้นผิว)
        faces = mesh.faces
        encoded_faces = shift_triangles_encrypt(faces, shift_value)
        mesh.faces = encoded_faces

        if not save_path.endswith(('.ply', '.stl', '.obj')):
            messagebox.showerror("Error", "Unsupported file format. Please use .ply, .stl, or .obj")
            return

        mesh.export(save_path)
        messagebox.showinfo("Success", "File encrypted and saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

## สร้าง GUI ##
root = tk.Tk()
root.title("3D Model Encryptor")

file_path_var = tk.StringVar()
save_path_var = tk.StringVar()

# จัดวาง Label, Entry และ Button ด้วยการเพิ่ม Padding
tk.Label(root, text="Input File:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
tk.Entry(root, textvariable=file_path_var, width=40).grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: file_path_var.set(filedialog.askopenfilename())).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Output File:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
tk.Entry(root, textvariable=save_path_var, width=40).grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: save_path_var.set(filedialog.asksaveasfilename())).grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="Shift Value:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
shift_entry = tk.Entry(root, width=10)
shift_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

tk.Button(root, text="Encrypt", command=encrypt_file).grid(row=3, column=1, padx=10, pady=10)
root.grid_columnconfigure(1, weight=1)

root.mainloop()

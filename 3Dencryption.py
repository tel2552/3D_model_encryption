import numpy as np
import trimesh
import random
import tkinter as tk
from tkinter import filedialog, messagebox
import time

def complex_encrypt_decrypt(faces, vertices, scale_factor, rotation_angle, shift_value, decrypt=False):
    if decrypt:
        # ย้อนการปรับขนาด
        vertices /= scale_factor
        
        # ย้อนการหมุน
        rotation_matrix = trimesh.transformations.rotation_matrix(
            np.deg2rad(-rotation_angle), [random.uniform(-1, 1) for _ in range(3)]
        )
        vertices = trimesh.transformations.transform_points(vertices, rotation_matrix)

        # ย้อนการเลื่อนและสลับตำแหน่ง
        for i in range(len(faces)):
            faces[i] = (faces[i] - shift_value) % len(faces)
            random.shuffle(faces[i])  # สลับตำแหน่งกลับแบบสุ่ม
    else:
        # การเข้ารหัส: สุ่มเปลี่ยนแปลงตำแหน่งของ vertices
        np.random.shuffle(vertices)

        for i in range(len(faces)):
            random.shuffle(faces[i])  # สลับตำแหน่งจุดใน triangles
            faces[i] = (faces[i] + shift_value) % len(faces)  # เลื่อนตำแหน่งจุดใน triangles แบบ cyclic shift

        rotation_matrix = trimesh.transformations.rotation_matrix(
            np.deg2rad(rotation_angle), [random.uniform(-1, 1) for _ in range(3)]
        )

        vertices = trimesh.transformations.transform_points(vertices, rotation_matrix)
        vertices *= scale_factor

    return faces, vertices

def process_file(is_encrypt=True):
    file_path = file_path_var.get()
    save_path = save_path_var.get()
    scale_factor = float(scale_entry.get())
    rotation_angle = float(rotation_entry.get())
    shift_value = int(shift_entry.get())

    if not file_path or not save_path:
        messagebox.showerror("Error", "Please select input and output files.")
        return

    try:
        start_time = time.time()

        mesh = trimesh.load(file_path)

        if is_encrypt:
            faces, vertices = complex_encrypt_decrypt(mesh.faces, mesh.vertices, scale_factor, rotation_angle, shift_value, decrypt=False)
        else:
            faces, vertices = complex_encrypt_decrypt(mesh.faces, mesh.vertices, scale_factor, rotation_angle, shift_value, decrypt=True)

        mesh.faces = faces
        mesh.vertices = vertices

        if not save_path.endswith(('.ply', '.stl', '.obj')):
            messagebox.showerror("Error", "Unsupported file format. Please use .ply, .stl, or .obj")
            return

        mesh.export(save_path)

        elapsed_time = time.time() - start_time

        if is_encrypt:
            messagebox.showinfo("Success", f"File encrypted and saved successfully. Elapsed time: {elapsed_time:.2f} seconds")
        else:
            messagebox.showinfo("Success", f"File decrypted and saved successfully. Elapsed time: {elapsed_time:.2f} seconds")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# สร้าง GUI
root = tk.Tk()
root.title("3D Model Encryptor/Decryptor")

file_path_var = tk.StringVar()
save_path_var = tk.StringVar()

tk.Label(root, text="Input File:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
tk.Entry(root, textvariable=file_path_var, width=40).grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: file_path_var.set(filedialog.askopenfilename())).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Output File:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
tk.Entry(root, textvariable=save_path_var, width=40).grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: save_path_var.set(filedialog.asksaveasfilename())).grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="Scale Factor:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
scale_entry = tk.Entry(root, width=10)
scale_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Rotation Angle:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
rotation_entry = tk.Entry(root, width=10)
rotation_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Triangle Shift:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
shift_entry = tk.Entry(root, width=10)
shift_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

tk.Button(root, text="Encrypt", command=lambda: process_file(is_encrypt=True)).grid(row=5, column=1, padx=10, pady=5)
tk.Button(root, text="Decrypt", command=lambda: process_file(is_encrypt=False)).grid(row=6, column=1, padx=10, pady=5)

root.grid_columnconfigure(1, weight=1)

root.mainloop()

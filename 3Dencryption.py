import tkinter as tk
from tkinter import filedialog, messagebox
import trimesh
import numpy as np

# ฟังก์ชันเข้ารหัสที่เปลี่ยนแปลงพิกัด (Vertices) ของ 3D Model
def shift_vertices_encrypt(vertices, shift_x, shift_y, shift_z):
    vertices[:, 0] += shift_x  # เลื่อนพิกัด X
    vertices[:, 1] += shift_y  # เลื่อนพิกัด Y
    vertices[:, 2] += shift_z  # เลื่อนพิกัด Z
    return vertices

# สร้างหน้าต่างหลักของแอป
root = tk.Tk()
root.title("3D Model Shape Encryption")

# ฟังก์ชันเปิดไฟล์
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("PLY files", "*.ply")])
    if file_path:
        file_path_var.set(file_path)

# ฟังก์ชันบันทึกไฟล์
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".ply", filetypes=[("PLY files", "*.ply")])
    if file_path:
        save_path_var.set(file_path)

# ฟังก์ชันเข้ารหัส
def encrypt_file():
    file_path = file_path_var.get()
    save_path = save_path_var.get()
    shift_x = float(x_shift_entry.get())
    shift_y = float(y_shift_entry.get())
    shift_z = float(z_shift_entry.get())

    if not file_path or not save_path:
        messagebox.showerror("Error", "Please select input and output files.")
        return

    try:
        mesh = trimesh.load(file_path)
        vertices = mesh.vertices
        encoded_vertices = shift_vertices_encrypt(vertices, shift_x, shift_y, shift_z)
        mesh.vertices = encoded_vertices
        mesh.export(save_path)
        messagebox.showinfo("Success", "File encrypted and saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# สร้าง UI ส่วนต่างๆ
file_path_var = tk.StringVar()
save_path_var = tk.StringVar()

tk.Label(root, text="Input File:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=file_path_var, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=open_file).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Output File:").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=save_path_var, width=50).grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Save As", command=save_file).grid(row=1, column=2, padx=10, pady=10)

tk.Label(root, text="X Shift Amount:").grid(row=2, column=0, padx=10, pady=10)
x_shift_entry = tk.Entry(root)
x_shift_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Y Shift Amount:").grid(row=3, column=0, padx=10, pady=10)
y_shift_entry = tk.Entry(root)
y_shift_entry.grid(row=3, column=1, padx=10, pady=10)

tk.Label(root, text="Z Shift Amount:").grid(row=4, column=0, padx=10, pady=10)
z_shift_entry = tk.Entry(root)
z_shift_entry.grid(row=4, column=1, padx=10, pady=10)

tk.Button(root, text="Encrypt", command=encrypt_file).grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# เริ่ม loop ของ Tkinter
root.mainloop()

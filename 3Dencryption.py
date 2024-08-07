import trimesh
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# ฟังก์ชันการเข้ารหัส
def shift_cipher_encrypt(text, shift):
    encrypted = ""
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            char_code = ord(char) + shift_amount
            if char.islower():
                if char_code > ord('z'):
                    char_code -= 26
                encrypted += chr(char_code)
            elif char.isupper():
                if char_code > ord('Z'):
                    char_code -= 26
                encrypted += chr(char_code)
        else:
            encrypted += char
    return encrypted

def shift_cipher_decrypt(text, shift):
    return shift_cipher_encrypt(text, -shift)

# สร้างหน้าต่างหลักของแอป
root = tk.Tk()
root.title("3D ModelEncryption By Shiba")

# สร้างฟังก์ชันเปิดไฟล์
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("PLY files", "*.ply")])
    if file_path:
        file_path_var.set(file_path)

# สร้างฟังก์ชันบันทึกไฟล์
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".ply", filetypes=[("PLY files", "*.ply")])
    if file_path:
        save_path_var.set(file_path)

# สร้างฟังก์ชันเข้ารหัส 3D model
def encrypt_file():
    file_path = file_path_var.get()
    save_path = save_path_var.get()
    shift = int(shift_entry.get())
    
    if not file_path or not save_path:
        messagebox.showerror("Error", "Please select input and output files.")
        return
    
    try:
        mesh = trimesh.load(file_path)
        text_to_encode = "example_text"
        encoded_text = shift_cipher_encrypt(text_to_encode, shift)
        
        # การเขียน property ใหม่ใน comment ของไฟล์ PLY
        mesh.metadata['comment'] = encoded_text
        
        mesh.export(save_path)
        messagebox.showinfo("Success", "File encrypted and saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# สร้างฟังก์ชันถอดรหัส 3D model
# def decrypt_file():
#     file_path = file_path_var.get()
#     shift = int(shift_entry.get())
    
#     if not file_path:
#         messagebox.showerror("Error", "Please select an input file.")
#         return
    
#     try:
#         mesh = trimesh.load(file_path)
#         encoded_text = mesh.metadata.get('comment', '')
#         decoded_text = shift_cipher_decrypt(encoded_text, shift)
#         messagebox.showinfo("Decoded Text", decoded_text)
#     except Exception as e:
#         messagebox.showerror("Error", str(e))

# สร้าง GUI ส่วนต่างๆ
file_path_var = tk.StringVar()
save_path_var = tk.StringVar()

# Load the image
image = Image.open(r"C:\Users\uSeR\OneDrive\เดสก์ท็อป\code\codebask\23.png")
image = image.resize((150, 100),Image.BILINEAR)
photo = ImageTk.PhotoImage(image)
label = tk.Label(root, image=photo)
label.grid(row=3, column=0)
tk.Label(root, text="Input File:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=file_path_var, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=open_file).grid(row=0, column=2, padx=10, pady=10)

tk.Label(root, text="Output File:").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=save_path_var, width=50).grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Save As", command=save_file).grid(row=1, column=2, padx=10, pady=10)

tk.Label(root, text="Shift Amount:").grid(row=2, column=0, padx=10, pady=10)
shift_entry = tk.Entry(root)
shift_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Button(root, text="Encrypt", command=encrypt_file).grid(row=3, column=0, columnspan=3, padx=10, pady=10)
# tk.Button(root, text="Decrypt", command=decrypt_file).grid(row=4, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()

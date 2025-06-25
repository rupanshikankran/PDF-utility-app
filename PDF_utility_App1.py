import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.simpledialog as simpledialog
from pdf2docx import Converter
import PyPDF2
from PIL import Image
import fitz  # PyMuPDF for working with PDFs
import os
from io import BytesIO

class PDFUtilityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Utility Tools")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")
        self.root.iconbitmap("download.ico")
        
        # Top bar with logout button
        top_bar = tk.Frame(self.root, bg="#34495e", height=50)
        top_bar.pack(side=tk.TOP, fill=tk.X)

        Signout_button = tk.Button(
            top_bar,
            text="Signout",
            command=self.Signout,
            font=("Helvetica", 12, "bold"),
            bg="#57a1f8",
            fg="white",
            activebackground="#c0392b",
            activeforeground="white"
        )
        Signout_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Main heading
        heading = tk.Label(
            self.root,
            text="PDF Utility Tools",
            font=("Helvetica", 30, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        heading.pack(pady=20)
        # Subheading
        subheading = tk.Label(
            root,
            text="Merge, Convert, Extract Images, Compress, and more",
            font=("Helvetica", 16),
            bg="#2c3e50",
            fg="#bdc3c7"
        )
        subheading.pack(pady=10)

        # Button frame
        button_frame = tk.Frame(self.root, bg="#34495e")
        button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        button_frame.pack(pady=30)  # Adds vertical padding above the button frame

        # Button configuration
        buttons = [
            ("PDF to DOCX", self.open_pdf_to_docx_window),
            ("Extract Images", self.open_extract_images_window),
            ("Merge PDFs", self.open_merge_pdfs_window),
            ("Image to PDF", self.open_image_to_pdf_window),
            ("Add Page Numbers", self.open_add_page_numbers_window),
            ("Encrypt PDF", self.open_encrypt_pdf_window),
            ("Decrypt PDF", self.open_decrypt_pdf_window),
            ("Remove Page from PDF", self.open_remove_page_from_pdf_window),  # Changed name here
            ("Text to PDF", self.open_text_to_pdf_window),
        ]
        
        # Add buttons in the frame
        for idx, (text, command) in enumerate(buttons):
            button = tk.Button(
                button_frame,
                text=text,
                command=command,
                font=("Helvetica", 14),
                bg="#57a1f8",
                fg="white",
                width=20,
                height=2,
                activebackground="#2980b9",
                activeforeground="white"
            )
            button.grid(row=idx // 2, column=idx % 2, padx=10, pady=10)

    def Signout(self):
        """Signout functionality to close the application."""
        confirm = messagebox.askyesno("Signout", "Are you sure you want to Signout?")
        if confirm:
            self.root.destroy()

    def open_tool_window(self, title, subheading_text, action):
        """Open a tool window for specific functionality."""
        tool_window = tk.Toplevel(self.root)
        tool_window.title(title)
        tool_window.geometry("600x400")
        tool_window.configure(bg="#2c3e50")
        tool_window.iconbitmap("download.ico")

        tk.Label(tool_window, text=title, font=("Helvetica", 20, "bold"), bg="#2c3e50", fg="#ecf0f1").pack(pady=20)
        tk.Label(tool_window, text=subheading_text, font=("Helvetica", 12), bg="#2c3e50", fg="#bdc3c7").pack(pady=10)

        select_button = tk.Button(
            tool_window,
            text="Select Document",
            command=lambda: [action(), tool_window.destroy()],
            font=("Helvetica", 14, "bold"),
            bg="#57a1f8",
            fg="white",
            activebackground="#3498db",
            activeforeground="white"
        )
        select_button.pack(pady=20)

    def open_pdf_to_docx_window(self):
        self.open_tool_window("PDF to DOCX Converter", "Convert your PDF to DOCX format.", self.pdf_to_docx)

    def open_extract_images_window(self):
        self.open_tool_window("Extract Images", "Extract images from a PDF.", self.extract_images)

    def open_merge_pdfs_window(self):
        self.open_tool_window("Merge PDFs", "Merge multiple PDFs into one.", self.merge_pdfs)

    def open_image_to_pdf_window(self):
        self.open_tool_window("Image to PDF Converter", "Convert images to a PDF.", self.image_to_pdf)

    #def open_compress_pdf_window(self):
        #self.open_tool_window("Compress PDF", "Compress your PDF size.", self.compress_pdf)

    def open_add_page_numbers_window(self):
        self.open_tool_window("Add Page Numbers", "Add page numbers to a PDF.", self.add_page_numbers)

    def open_encrypt_pdf_window(self):
        self.open_tool_window("Encrypt PDF", "Secure your PDF with a password.", self.encrypt_pdf)

    def open_decrypt_pdf_window(self):
        self.open_tool_window("Decrypt PDF", "Remove password protection from your PDF.", self.decrypt_pdf)

    def open_remove_page_from_pdf_window(self):
        self.open_tool_window("Remove Page from PDF", "Enter page numbers to remove (comma-separated).", self.remove_page_from_pdf)

    def open_text_to_pdf_window(self):
        self.open_tool_window("Text to PDF", "Convert text files into a PDF document.", self.text_to_pdf)

    def pdf_to_docx(self):
        filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filepath:
            save_path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Documents", "*.docx")])
            if save_path:
                try:
                    cv = Converter(filepath)
                    cv.convert(save_path)
                    cv.close()
                    messagebox.showinfo("Success", f"PDF converted to DOCX and saved to {save_path}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def extract_images(self):
        filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filepath:
            save_dir = filedialog.askdirectory()
            if save_dir:
                try:
                    pdf_document = fitz.open(filepath)
                    image_count = 0

                    for page_num in range(len(pdf_document)):
                        page = pdf_document.load_page(page_num)
                        images = page.get_images(full=True)
                        for img_index, img in enumerate(images):
                            xref = img[0]
                            base_image = pdf_document.extract_image(xref)
                            image_bytes = base_image["image"]
                            image = Image.open(BytesIO(image_bytes))
                            image_format = base_image["ext"].upper()
                            image.save(os.path.join(save_dir, f"image_{page_num+1}_{img_index+1}.{image_format.lower()}"))
                            image_count += 1

                    messagebox.showinfo("Success", f"{image_count} images extracted to {save_dir}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def merge_pdfs(self):
        filepaths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if filepaths:
            save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if save_path:
                pdf_writer = PyPDF2.PdfWriter()
                try:
                    for filepath in filepaths:
                        pdf_reader = PyPDF2.PdfReader(filepath)
                        for page in pdf_reader.pages:
                            pdf_writer.add_page(page)
                    with open(save_path, "wb") as f:
                        pdf_writer.write(f)
                    messagebox.showinfo("Success", f"PDFs merged and saved to {save_path}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def image_to_pdf(self):
        filepaths = filedialog.askopenfilenames(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if filepaths:
            save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if save_path:
                try:
                    images = [Image.open(fp).convert("RGB") for fp in filepaths]
                    images[0].save(save_path, save_all=True, append_images=images[1:])
                    messagebox.showinfo("Success", f"Images converted to PDF and saved to {save_path}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    

    def add_page_numbers(self):
        filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filepath:
            save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if save_path:
                try:
                    pdf_document = fitz.open(filepath)
                    for page_num in range(len(pdf_document)):
                        page = pdf_document.load_page(page_num)
                        page.insert_text((500, 750), f"{page_num + 1}", fontsize=12)
                    pdf_document.save(save_path)
                    messagebox.showinfo("Success", f" numbers added and saved to {save_path}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def encrypt_pdf(self):
        filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filepath:
            password = simpledialog.askstring("Password", "Enter a password to encrypt the PDF:", show="*")
            if password:
                save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
                if save_path:
                    try:
                        pdf_reader = PyPDF2.PdfReader(filepath)
                        pdf_writer = PyPDF2.PdfWriter()
                        for page in pdf_reader.pages:
                            pdf_writer.add_page(page)
                        pdf_writer.encrypt(password)
                        with open(save_path, "wb") as f:
                            pdf_writer.write(f)
                        messagebox.showinfo("Success", f"PDF encrypted and saved to {save_path}")
                    except Exception as e:
                        messagebox.showerror("Error", str(e))

    def decrypt_pdf(self):
        filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filepath:
            password = simpledialog.askstring("Password", "Enter the password to decrypt the PDF:", show="*")
            if password:
                save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
                if save_path:
                    try:
                        pdf_reader = PyPDF2.PdfReader(filepath)
                        if pdf_reader.is_encrypted:
                            pdf_reader.decrypt(password)
                        pdf_writer = PyPDF2.PdfWriter()
                        for page in pdf_reader.pages:
                            pdf_writer.add_page(page)
                        with open(save_path, "wb") as f:
                            pdf_writer.write(f)
                        messagebox.showinfo("Success", f"PDF decrypted and saved to {save_path}")
                    except Exception as e:
                        messagebox.showerror("Error", str(e))

    def remove_page_from_pdf(self):
        filepath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if filepath:
            save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if save_path:
                try:
                    pdf_reader = PyPDF2.PdfReader(filepath)
                    pdf_writer = PyPDF2.PdfWriter()

                    # Ask the user which pages to remove
                    page_nums_to_remove = simpledialog.askstring("Remove Page", "Enter page numbers to remove (comma-separated):")
                    if page_nums_to_remove:
                        page_nums_to_remove = [int(num.strip()) - 1 for num in page_nums_to_remove.split(",")]
                        for page_num in range(len(pdf_reader.pages)):
                            if page_num not in page_nums_to_remove:
                                pdf_writer.add_page(pdf_reader.pages[page_num])

                    with open(save_path, "wb") as f:
                        pdf_writer.write(f)
                    messagebox.showinfo("Success", f"Page removed and PDF saved to {save_path}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def text_to_pdf(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if save_path:
                try:
                    from fpdf import FPDF
                    with open(filepath, "r") as f:
                        text = f.read()

                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_auto_page_break(auto=True, margin=15)
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, text)

                    pdf.output(save_path)
                    messagebox.showinfo("Success", f"Text file converted to PDF and saved to {save_path}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFUtilityApp(root)
    root.mainloop()

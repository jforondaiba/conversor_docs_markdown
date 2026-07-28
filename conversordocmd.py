import sys
import os
import io
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Cargamos las librerías necesarias con detección de errores
try:
    from markitdown import MarkItDown
    HAS_MARKITDOWN = True
except ImportError:
    HAS_MARKITDOWN = False

try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

try:
    import fitz  # PyMuPDF
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False

try:
    import pytesseract
    from PIL import Image
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

# Detectar la ruta base si se empaqueta como ejecutable (.exe) con PyInstaller
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent

# Configuración de Tesseract (portable o ruta por defecto)
tesseract_exe = BASE_DIR / "Tesseract-OCR" / "tesseract.exe"
if tesseract_exe.exists() and HAS_OCR:
    pytesseract.pytesseract.tesseract_cmd = str(tesseract_exe)
elif HAS_OCR:
    default_path = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    if default_path.exists():
        pytesseract.pytesseract.tesseract_cmd = str(default_path)

SUPPORTED_EXTENSIONS = [".pdf", ".docx", ".pptx", ".xlsx", ".html", ".csv", ".json"]

def extraer_texto_ocr(ruta_pdf):
    if not (HAS_FITZ and HAS_OCR):
        return ""
    texto_ocr = ""
    try:
        doc = fitz.open(ruta_pdf)
        for i, pagina in enumerate(doc):
            pix = pagina.get_pixmap(dpi=150)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            try:
                texto_pagina = pytesseract.image_to_string(img, lang="spa")
            except Exception:
                texto_pagina = pytesseract.image_to_string(img, lang="eng")
            if texto_pagina.strip():
                texto_ocr += f"<!-- Página {i+1} -->\n" + texto_pagina + "\n\n"
        doc.close()
    except Exception:
        pass
    return texto_ocr.strip()

def procesar_archivo_individual(archivo, carpeta_destino, log_func):
    archivo = Path(archivo)
    if archivo.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return False
    
    log_func(f"Procesando: {archivo.name}...")
    texto = ""
    
    # 1. Intentar con MarkItDown
    if HAS_MARKITDOWN:
        try:
            md = MarkItDown()
            res = md.convert(str(archivo))
            texto = res.text_content.strip() if res.text_content else ""
        except Exception:
            pass

    # 2. Respaldo con PyPDF para PDFs de texto
    if not texto and archivo.suffix.lower() == ".pdf" and HAS_PYPDF:
        try:
            reader = PdfReader(archivo)
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    texto += t + "\n\n"
            texto = texto.strip()
        except Exception:
            pass

    # 3. Respaldo con OCR para imágenes/escaneos
    if not texto and archivo.suffix.lower() == ".pdf":
        log_func(f"  🔍 Ejecutando OCR en {archivo.name}...")
        texto = extraer_texto_ocr(archivo)

    # Guardar resultado en UTF-8 con BOM (utf-8-sig) para compatibilidad total con NotebookLM
    if texto:
        salida = carpeta_destino / f"{archivo.stem}.md"
        with open(salida, "w", encoding="utf-8-sig", errors="ignore") as f:
            f.write(texto)
        log_func(f"  ✓ Completado: {salida.name}")
        log_func(f"    📍 Guardado en: {salida.resolve()}\n")
        return True
    else:
        log_func(f"  ✕ No se pudo extraer texto de {archivo.name}\n")
        return False

class ConversorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Conversor de Documentos a Markdown | JAFI")
        self.geometry("650x570")
        self.minsize(580, 500)
        self.configure(bg="#f4f6f9")
        
        self.archivos_o_carpeta = []
        self.modo_seleccion = None  # 'archivos' o 'carpeta'

        self.crear_interfaz()

    def crear_interfaz(self):
        # Encabezado
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Header.TLabel", font=("Segoe UI", 13, "bold"), background="#f4f6f9", foreground="#2c3e50")

        header = ttk.Label(self, text="Conversor de Documentos a Markdown (.md)", style="Header.TLabel")
        header.pack(pady=(15, 2))

        subtext = tk.Label(self, text="Soporta PDF (con OCR), DOCX, PPTX, XLSX", font=("Segoe UI", 8), bg="#f4f6f9", fg="#7f8c8d")
        subtext.pack(pady=(0, 15))

        # Panel de Botones de Selección
        frame_botones = tk.Frame(self, bg="#f4f6f9")
        frame_botones.pack(pady=5)

        btn_archivo = tk.Button(frame_botones, text="📄 Seleccionar Archivo(s)", font=("Segoe UI", 10, "bold"), bg="#3498db", fg="white", activebackground="#2980b9", activeforeground="white", relief="flat", padx=12, pady=6, command=self.seleccionar_archivos)
        btn_archivo.grid(row=0, column=0, padx=8)

        btn_carpeta = tk.Button(frame_botones, text="📁 Seleccionar Carpeta", font=("Segoe UI", 10, "bold"), bg="#2ecc71", fg="white", activebackground="#27ae60", activeforeground="white", relief="flat", padx=12, pady=6, command=self.seleccionar_carpeta)
        btn_carpeta.grid(row=0, column=1, padx=8)

        # Label de Estado
        self.lbl_seleccion = tk.Label(self, text="Ningún archivo o carpeta seleccionado", font=("Segoe UI", 9, "italic"), bg="#f4f6f9", fg="#95a5a6")
        self.lbl_seleccion.pack(pady=8)

        # Botón de Inicio
        self.btn_convertir = tk.Button(self, text="🚀 Iniciar Conversión", font=("Segoe UI", 11, "bold"), bg="#e74c3c", fg="white", activebackground="#c0392b", activeforeground="white", relief="flat", padx=20, pady=8, state="disabled", command=self.iniciar_conversion_hilo)
        self.btn_convertir.pack(pady=10)

        # Terminal / Registro de Estado
        frame_log = tk.Frame(self, bg="#f4f6f9")
        frame_log.pack(fill="both", expand=True, padx=20, pady=(10, 5))

        lbl_log = tk.Label(frame_log, text="Registro de proceso:", font=("Segoe UI", 9, "bold"), bg="#f4f6f9", fg="#34495e")
        lbl_log.pack(anchor="w")

        self.txt_log = tk.Text(frame_log, font=("Consolas", 9), bg="#1e1e1e", fg="#dcdcdc", insertbackground="white", relief="flat", height=10)
        self.txt_log.pack(fill="both", expand=True, side="left")

        scrollbar = ttk.Scrollbar(frame_log, command=self.txt_log.yview)
        scrollbar.pack(side="right", fill="y")
        self.txt_log.config(yscrollcommand=scrollbar.set)

        # Pie de página / Firma de la marca
        footer_frame = tk.Frame(self, bg="#2c3e50", pady=6)
        footer_frame.pack(fill="x", side="bottom")

        lbl_branding = tk.Label(
            footer_frame, 
            text="Un producto de Jorge Productos y Servicios Digitales (JAFI)", 
            font=("Segoe UI", 8, "bold"), 
            bg="#2c3e50", 
            fg="#ecf0f1"
        )
        lbl_branding.pack()

    def log(self, mensaje):
        self.txt_log.insert(tk.END, mensaje + "\n")
        self.txt_log.see(tk.END)

    def seleccionar_archivos(self):
        archivos = filedialog.askopenfilenames(
            title="Selecciona documentos",
            filetypes=[("Documentos soportados", "*.pdf *.docx *.pptx *.xlsx *.html *.csv *.json"), ("Todos los archivos", "*.*")]
        )
        if archivos:
            self.archivos_o_carpeta = list(archivos)
            self.modo_seleccion = 'archivos'
            n = len(archivos)
            self.lbl_seleccion.config(text=f"✓ Seleccionado(s) {n} archivo(s)", fg="#27ae60")
            self.btn_convertir.config(state="normal")

    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory(title="Selecciona la carpeta con documentos")
        if carpeta:
            self.archivos_o_carpeta = Path(carpeta)
            self.modo_seleccion = 'carpeta'
            self.lbl_seleccion.config(text=f"✓ Carpeta: {self.archivos_o_carpeta.name}", fg="#27ae60")
            self.btn_convertir.config(state="normal")

    def iniciar_conversion_hilo(self):
        self.btn_convertir.config(state="disabled")
        self.txt_log.delete("1.0", tk.END)
        threading.Thread(target=self.ejecutar_conversion, daemon=True).start()

    def ejecutar_conversion(self):
        self.log("--- Iniciando proceso de conversión ---\n")
        exitos = 0
        total = 0
        carpeta_salida_info = ""

        if self.modo_seleccion == 'archivos':
            total = len(self.archivos_o_carpeta)
            for f in self.archivos_o_carpeta:
                p = Path(f)
                destino = p.parent
                carpeta_salida_info = str(destino.resolve())
                if procesar_archivo_individual(p, destino, self.log):
                    exitos += 1

        elif self.modo_seleccion == 'carpeta':
            carpeta = self.archivos_o_carpeta
            carpeta_salida_info = str(carpeta.resolve())
            archivos_validos = [f for f in carpeta.iterdir() if f.suffix.lower() in SUPPORTED_EXTENSIONS]
            total = len(archivos_validos)
            if total == 0:
                self.log("⚠️ No se encontraron archivos soportados en la carpeta seleccionada.")
            for f in archivos_validos:
                if procesar_archivo_individual(f, carpeta, self.log):
                    exitos += 1

        self.log(f"--- Proceso finalizado: {exitos}/{total} convertidos con éxito ---")
        self.log(f"📁 Directorio de salida: {carpeta_salida_info}")
        
        messagebox.showinfo(
            "Proceso Completado", 
            f"Se procesaron {exitos} de {total} archivos correctamente.\n\n"
            f"Ubicación de los archivos .md:\n{carpeta_salida_info}\n\n"
            f"Desarrollado por Jorge Productos y Servicios Digitales (JAFI)"
        )
        self.btn_convertir.config(state="normal")

if __name__ == "__main__":
    app = ConversorApp()
    app.mainloop()
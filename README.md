# 📄 Conversor de Documentos a Markdown (.md) | JAFI

Una aplicación de escritorio en Python con interfaz gráfica (GUI) diseñada para convertir diversos formatos de documentos (`.pdf`, `.docx`, `.pptx`, `.xlsx`, `.html`, `.csv`, `.json`) a archivos texto plano en formato **Markdown (.md)**, optimizados para su uso en herramientas de IA como NotebookLM.

Desarrollado por **Jorge Productos y Servicios Digitales (JAFI)**.

---

## 🚀 Características

* **Soporte multiformato:** Convierte archivos PDF, Word, PowerPoint, Excel, HTML, CSV y JSON.
* **Procesamiento híbrido y OCR:** 
  1. Utiliza `MarkItDown` de Microsoft como motor principal.
  2. Respaldo de extracción de texto para PDFs con `pypdf`.
  3. Soporte para PDFs escaneados mediante OCR (`PyMuPDF` + `pytesseract`).
* **Codificación UTF-8 con BOM (`utf-8-sig`):** Garantiza compatibilidad al importar los archivos `.md` en plataformas como NotebookLM.
* **Procesamiento individual o por lote:** Convierte archivos seleccionados o carpetas completas.
* **Interfaz amigable:** Registro visual en tiempo real de la conversión sin congelar la aplicación (Multithreading).

---

## 🛠️ Requisitos e Instalación

### 1. Clonar el repositorio
```bash
git clone [https://github.com/jforondaiba/conversor_docs_markdown.git](https://github.com/jforondaiba/conversor_docs_markdown.git)
cd conversor_docs_markdown

2. Instalar dependencias

Asegúrate de tener Python 3.8+ instalado y ejecuta:
Bash

pip install -r requirements.txt

3. (Opcional) Configuración de Tesseract OCR

Para que la conversión de PDFs escaneados (imágenes) funcione por OCR:

    En Windows, instala Tesseract-OCR en la ruta por defecto (C:\Program Files\Tesseract-OCR\tesseract.exe) o incluye la carpeta ejecutable Tesseract-OCR junto al script.

💻 Uso de la Aplicación

Ejecuta el script principal con:
Bash

python app_gui.py

    Haz clic en "📄 Seleccionar Archivo(s)" o "📁 Seleccionar Carpeta".

    Presiona el botón "🚀 Iniciar Conversión".

    Revisa la consola/terminal integrada para seguir el progreso en tiempo real.

    Los archivos .md resultantes se guardarán en la misma ubicación del archivo fuente.

📝 Licencia

Este proyecto es distribuido por Jorge Productos y Servicios Digitales (JAFI).

¡Excelente script! Tu aplicación está muy bien estructurada, incluye un buen manejo de errores, usa subprocesos con `threading` para no congelar la interfaz de Tkinter y cuenta con varias capas de procesamiento (MarkItDown, PyPDF, OCR).

Aquí tienes exactamente los contenidos para los **dos archivos que te faltan** en el repositorio.

---

## 1. Archivo `requirements.txt`

Crea un archivo llamado `requirements.txt` en la raíz de tu proyecto y pega este contenido:

```txt
markitdown
pypdf
PyMuPDF
pytesseract
Pillow

```

---

## 2. Archivo `README.md`

En GitHub, haz clic en el botón verde **"Add a README"** (o crea el archivo `README.md`) y pega la siguiente plantilla lista para tu proyecto:

```markdown
# 📄 Conversor de Documentos a Markdown (.md) | JAFI

Una aplicación de escritorio en Python con interfaz gráfica (GUI) diseñada para convertir diversos formatos de documentos (`.pdf`, `.docx`, `.pptx`, `.xlsx`, `.html`, `.csv`, `.json`) a archivos texto plano en formato **Markdown (.md)**, optimizados para su uso en herramientas de IA como NotebookLM.

Desarrollado por **Jorge Productos y Servicios Digitales (JAFI)**.

---

## 🚀 Características

* **Soporte multiformato:** Convierte archivos PDF, Word, PowerPoint, Excel, HTML, CSV y JSON.
* **Procesamiento híbrido y OCR:** 
  1. Utiliza `MarkItDown` de Microsoft como motor principal.
  2. Respaldo de extracción de texto para PDFs con `pypdf`.
  3. Soporte para PDFs escaneados mediante OCR (`PyMuPDF` + `pytesseract`).
* **Codificación UTF-8 con BOM (`utf-8-sig`):** Garantiza compatibilidad al importar los archivos `.md` en plataformas como NotebookLM.
* **Procesamiento individual o por lote:** Convierte archivos seleccionados o carpetas completas.
* **Interfaz amigable:** Registro visual en tiempo real de la conversión sin congelar la aplicación (Multithreading).

---

## 🛠️ Requisitos e Instalación

### 1. Clonar el repositorio
```bash
git clone [https://github.com/jforondaiba/conversor_docs_markdown.git](https://github.com/jforondaiba/conversor_docs_markdown.git)
cd conversor_docs_markdown

```

### 2. Instalar dependencias

Asegúrate de tener Python 3.8+ instalado y ejecuta:

```bash
pip install -r requirements.txt

```

### 3. (Opcional) Configuración de Tesseract OCR

Para que la conversión de PDFs escaneados (imágenes) funcione por OCR:

* En Windows, instala [Tesseract-OCR](https://www.google.com/search?q=https://github.com/UB-Mannheim/tesseract/wiki) en la ruta por defecto (`C:\Program Files\Tesseract-OCR\tesseract.exe`) o incluye la carpeta ejecutable `Tesseract-OCR` junto al script.

---

## 💻 Uso de la Aplicación

Ejecuta el script principal con:

```bash
python conversordocmd.py

```

1. Haz clic en **"📄 Seleccionar Archivo(s)"** o **"📁 Seleccionar Carpeta"**.
2. Presiona el botón **"🚀 Iniciar Conversión"**.
3. Revisa la consola/terminal integrada para seguir el progreso en tiempo real.
4. Los archivos `.md` resultantes se guardarán en la misma ubicación del archivo fuente.

---

## 📝 Licencia

Este proyecto es distribuido por **Jorge Productos y Servicios Digitales (JAFI)**.

```

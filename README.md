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

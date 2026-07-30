import os
import urllib.request

# Directories to create
dirs = [
    'js/lib',
    'css/lib'
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

libs = {
    'js/lib/tailwind.js': 'https://cdn.tailwindcss.com',
    'js/lib/pdf-lib.min.js': 'https://unpkg.com/pdf-lib@1.17.1/dist/pdf-lib.min.js',
    'js/lib/pdf.min.js': 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js',
    'js/lib/pdf.worker.min.js': 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js',
    'js/lib/jszip.min.js': 'https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js',
    'js/lib/cropper.min.js': 'https://cdnjs.cloudflare.com/ajax/libs/cropperjs/1.6.1/cropper.min.js',
    'css/lib/cropper.min.css': 'https://cdnjs.cloudflare.com/ajax/libs/cropperjs/1.6.1/cropper.min.css',
    'js/lib/lucide.min.js': 'https://unpkg.com/lucide@latest/dist/umd/lucide.min.js'
}

print("Iniciando descarga de librerías locales para PDFito...")

for local_path, url in libs.items():
    try:
        print(f"Descargando {url} -> {local_path} ...")
        # Set a user-agent header to avoid HTTP 403 Forbidden errors from Cloudflare
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            with open(local_path, 'wb') as f:
                f.write(response.read())
        print("¡Descarga completada!")
    except Exception as e:
        print(f"ERROR al descargar {local_path}: {e}")

print("Proceso finalizado.")

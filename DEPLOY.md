# 🚀 PDFito — Despliegue en AWS S3

## ¿Qué archivos subir?

Sube **toda la carpeta `PDFito/`** a tu bucket S3, manteniendo la misma estructura:

```
PDFito/
├── index.html              ← Página principal
├── css/
│   ├── app.css             ← Estilos personalizados
│   └── lib/
│       └── cropper.min.css
├── js/
│   ├── app.bundle.js       ← Bundle único (sin módulos ES)
│   └── lib/
│       ├── tailwind.js
│       ├── pdf-lib.min.js
│       ├── pdf.min.js
│       ├── pdf.worker.min.js
│       ├── jszip.min.js
│       ├── cropper.min.js
│       └── lucide.min.js
```

> **Nota**: Los archivos `js/app.js`, `js/ui/`, `js/utils/`, `js/core/` son el código fuente.
> El archivo que se carga es `js/app.bundle.js` (ya compilado).

---

## Paso a paso — AWS S3 Static Website

### 1. Crear el bucket S3

```bash
aws s3 mb s3://mi-pdfito-app --region us-east-1
```

### 2. Habilitar hosting estático

```bash
aws s3 website s3://mi-pdfito-app \
  --index-document index.html \
  --error-document index.html
```

### 3. Subir todos los archivos

```bash
aws s3 sync . s3://mi-pdfito-app \
  --exclude "*.py" \
  --exclude "*.ps1" \
  --exclude "*.md" \
  --exclude ".git/*" \
  --exclude "node_modules/*" \
  --exclude "js/app.js" \
  --exclude "js/ui/*" \
  --exclude "js/utils/*" \
  --exclude "js/core/*"
```

O subir todo (más simple):

```bash
aws s3 sync . s3://mi-pdfito-app --delete
```

### 4. Hacer el bucket público (política)

Crea el archivo `bucket-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::mi-pdfito-app/*"
    }
  ]
}
```

Aplica la política:

```bash
aws s3api put-bucket-policy \
  --bucket mi-pdfito-app \
  --policy file://bucket-policy.json
```

### 5. Desactivar el bloqueo de acceso público

En la consola de AWS → S3 → tu bucket → **"Permisos"** → **"Bloquear acceso público"** → desactivar.

### 6. URL de tu app

```
http://mi-pdfito-app.s3-website-us-east-1.amazonaws.com
```

---

## Con CloudFront (HTTPS + dominio propio)

```bash
# Crear distribución CloudFront apuntando al bucket S3
aws cloudfront create-distribution \
  --origin-domain-name mi-pdfito-app.s3-website-us-east-1.amazonaws.com \
  --default-root-object index.html
```

---

## Rebuild (cuando hagas cambios al código)

Si modificas algún archivo JS, re-ejecuta el script de build:

```powershell
# En la carpeta PDFito/
.\build.ps1
```

Luego re-sube solo el bundle:

```bash
aws s3 cp js/app.bundle.js s3://mi-pdfito-app/js/app.bundle.js
```

---

## Sin AWS — Otras opciones

| Plataforma | Comando |
|---|---|
| **Netlify** | Arrastra la carpeta al panel de Netlify |
| **GitHub Pages** | Sube a un repo, activa Pages en Settings |
| **Vercel** | `vercel --prod` desde la carpeta |
| **Cualquier servidor** | Copia la carpeta, abre `index.html` |

> ✅ La app funciona en cualquier hosting estático. No requiere Node.js, Python ni ningún backend.

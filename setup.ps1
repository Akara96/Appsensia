# Setup Phase 1
$ErrorActionPreference = "Stop"

Write-Host "Creating main directory..."
New-Item -ItemType Directory -Force -Path "sistema_estudante"
Set-Location -Path "sistema_estudante"

Write-Host "Creating Virtual Environment..."
python -m venv venv

Write-Host "Installing dependencies..."
& .\venv\Scripts\python.exe -m pip install --upgrade pip
& .\venv\Scripts\python.exe -m pip install Django>=5.0 PyMySQL Pillow python-dotenv openpyxl xhtml2pdf django-crispy-forms crispy-bootstrap5

Write-Host "Saving requirements..."
& .\venv\Scripts\pip.exe freeze | Out-File -FilePath requirements.txt -Encoding utf8

Write-Host "Creating Django project..."
& .\venv\Scripts\django-admin.exe startproject konfigurasaun .

Write-Host "Creating .env file..."
@"
SECRET_KEY=your_secret_key_here
DEBUG=True
DB_NAME=student_db
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306
"@ | Out-File -FilePath .env -Encoding utf8
Copy-Item -Path .env -Destination .env.example

Write-Host "Creating directories and apps..."
New-Item -ItemType Directory -Force -Path "templates"
New-Item -ItemType Directory -Force -Path "media"
New-Item -ItemType Directory -Force -Path "static"

& .\venv\Scripts\python.exe manage.py startapp konta
& .\venv\Scripts\python.exe manage.py startapp akademiku
& .\venv\Scripts\python.exe manage.py startapp estudante
& .\venv\Scripts\python.exe manage.py startapp relatoriu

Write-Host "Phase 1 Setup Complete!"

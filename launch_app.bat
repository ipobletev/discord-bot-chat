@echo off
REM Launch the server application

REM Set environment variables from the .env file
if exist .env (
    for /f "usebackq tokens=1* delims==" %%a in (`findstr /r "^[^#]" .env`) do (
        set "%%a=%%b"
    )
)

REM Create and activate the virtual environment if it does not exist
if not exist .venv\Scripts\activate (
    python -m venv .venv
    call .venv\Scripts\activate
) else (
    call .venv\Scripts\activate
)

pip install --upgrade pip
pip install -r requirements.txt

REM Run the application
python main.py
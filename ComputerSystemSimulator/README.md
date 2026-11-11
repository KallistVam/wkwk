# Computer System Simulator

A desktop educational simulator built with Python and Kivy. It simulates CPU arithmetic instructions, a small addressable memory, a virtual file manager, and a simple process manager. It does **not** control Windows processes or physical hardware.

## Requirements
- Windows 10/11
- Python 3.10–3.12 recommended
- VS Code (optional)

## Setup (PowerShell terminal in this folder)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

If PowerShell blocks activation, run this once in the current terminal:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Alternatively, install and run without activating:
```powershell
py -m pip install -r requirements.txt
py main.py
```

## Features
- Dashboard navigation
- CPU arithmetic: ADD, SUB, MUL, DIV
- Simulated RAM read/write/clear
- Virtual file create/read/rename/copy/delete
- Process create/run/stop/delete with JSON persistence

## Data
- `data/virtual_files/` stores simulator-created text files.
- `data/processes.json` stores simulated process records.

Run `python main.py` from this project directory so relative data paths resolve correctly.

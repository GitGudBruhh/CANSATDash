# Installation

1. Create virtual environment: `python -m venv .cansatvenv`
2. Activatate virtual environment: `source .cansatvenv/bin/activate`
3. Install requirements: `pip install requirements.txt`
4. Download ttyd: `wget https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.x86_64`
5. Make ttyd server executable: `chmod +x ttyd.x86_64`
6. Move ttyd server to PATH: `mv ttyd.x86_64 .cansatvenv/bin`

# Usage

1. Run streamlit dashboard: `streamlit run src/main.py`
2. If simulation required, run `python src/py-random-data-gen.py` in a separate terminal window.

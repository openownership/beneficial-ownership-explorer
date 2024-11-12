import httpx
import zipfile
from pathlib import Path

def download_data(url, filename):
    if not Path(f"boexplorer/data/sources/{filename}").is_file():
        response = httpx.get(url, timeout=20)
        zip_filename = url.split("/")[-1]
        with open(zip_filename, 'wb') as file:
            file.write(response.content)
        with zipfile.ZipFile(zip_filename, 'r') as zip_file:
            zip_file.extractall(Path("boexplorer/data/sources"))

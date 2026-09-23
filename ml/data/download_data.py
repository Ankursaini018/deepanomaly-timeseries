import urllib.request
import zipfile
import shutil
from ml.utils.config import RAW_DATA_DIR

DATA_URL = "http://www.timeseriesclassification.com/aeon-toolkit/ECG5000.zip"
EXPECTED_FILES = ["ECG5000_TRAIN.txt", "ECG5000_TEST.txt"]


def files_exist():
    return all((RAW_DATA_DIR / f).exists() for f in EXPECTED_FILES)


def flatten_files():
    for filename in EXPECTED_FILES:
        if (RAW_DATA_DIR / filename).exists():
            continue
        found = list(RAW_DATA_DIR.rglob(filename))
        if found:
            shutil.move(str(found[0]), str(RAW_DATA_DIR / filename))


def download():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    if files_exist():
        print("[OK] Dataset already exists.")
        return True

    zip_path = RAW_DATA_DIR / "ECG5000.zip"
    try:
        urllib.request.urlretrieve(DATA_URL, zip_path)
    except Exception as e:
        print(f"[ERROR] {e}")
        print("Manual download: https://www.timeseriesclassification.com/description.php?Dataset=ECG5000")
        return False

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(RAW_DATA_DIR)

    flatten_files()
    zip_path.unlink()
    print(f"[OK] Dataset ready at {RAW_DATA_DIR}")
    return files_exist()


if __name__ == "__main__":
    download()
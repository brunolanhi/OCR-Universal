from pathlib import Path
from datetime import datetime, timedelta
import shutil

BASE_DIR = Path("/opt/ocr-universal/app")

PASTAS = [
    BASE_DIR / "uploads",
    BASE_DIR / "outputs",
    BASE_DIR / "temp"
]

LIMITE_DIAS = 7

agora = datetime.now()
limite = agora - timedelta(days=LIMITE_DIAS)

for pasta in PASTAS:

    if not pasta.exists():
        continue

    for item in pasta.iterdir():

        try:

            data_modificacao = datetime.fromtimestamp(
                item.stat().st_mtime
            )

            if data_modificacao < limite:

                print(f"Removendo: {item}")

                if item.is_dir():
                    shutil.rmtree(item)

                else:
                    item.unlink()

        except Exception as erro:

            print(
                f"Erro ao remover {item}: {erro}"
            )

print("Limpeza concluída")

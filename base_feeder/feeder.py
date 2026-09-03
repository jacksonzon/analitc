"""
Base Feeder
-----------
Monitora a pasta onde o executavel esta rodando. Toda vez que um arquivo
de "base" (csv ou xlsx cujo nome comece com "base") for adicionado,
alterado ou removido, ele recombina todos os arquivos base encontrados
em:
  - data.json  -> array de objetos (uma linha = um objeto)
  - data.js    -> mesma coisa, mas como variavel global JS
                  (window.BASE_DATA) para o HTML poder usar sem precisar
                  de servidor.

Alem disso, sobe um servidor HTTP local simples servindo a propria pasta,
pra evitar erro de CORS quando o projeto HTML usa fetch('data.json').

Uso:
  python feeder.py            -> usa a pasta atual como pasta monitorada
  python feeder.py "C:\\pasta" -> usa a pasta informada

Depois de compilado em .exe (ver build.bat), basta colocar o .exe dentro
da mesma pasta do projeto HTML e dar 2 cliques nele.
"""

import sys
import os
import json
import time
import glob
import threading
import http.server
import socketserver
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("ERRO: biblioteca 'pandas' nao encontrada. Rode: pip install pandas openpyxl")
    sys.exit(1)

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

PORT = 8000
BASE_PREFIX = "base"  # nome do arquivo precisa comecar com isso (case-insensitive)
VALID_EXTS = {".csv", ".xlsx", ".xls"}


def is_base_file(path: Path) -> bool:
    return (
        path.suffix.lower() in VALID_EXTS
        and path.stem.lower().startswith(BASE_PREFIX)
        and not path.name.startswith("~$")  # ignora arquivos temporarios do Excel
    )


def read_any(path: Path) -> "pd.DataFrame":
    if path.suffix.lower() == ".csv":
        # tenta detectar separador e encoding comuns no Brasil
        for sep in [",", ";"]:
            for enc in ["utf-8-sig", "latin1"]:
                try:
                    df = pd.read_csv(path, sep=sep, encoding=enc)
                    if df.shape[1] > 1:
                        return df
                except Exception:
                    continue
        return pd.read_csv(path)
    else:
        return pd.read_excel(path)


def rebuild(folder: Path):
    files = [p for p in folder.iterdir() if p.is_file() and is_base_file(p)]
    all_rows = []
    for f in sorted(files):
        try:
            df = read_any(f)
            df["_arquivo_origem"] = f.name
            all_rows.extend(df.fillna("").to_dict(orient="records"))
        except Exception as e:
            print(f"[AVISO] Falha ao ler {f.name}: {e}")

    out_json = folder / "data.json"
    out_js = folder / "data.js"

    out_json.write_text(json.dumps(all_rows, ensure_ascii=False, indent=2), encoding="utf-8")
    js_content = (
        "// Gerado automaticamente pelo base_feeder. Nao editar a mao.\n"
        f"window.BASE_DATA = {json.dumps(all_rows, ensure_ascii=False)};\n"
        "window.dispatchEvent(new CustomEvent('basedata:updated', {detail: window.BASE_DATA}));\n"
    )
    out_js.write_text(js_content, encoding="utf-8")

    print(f"[OK] {len(files)} arquivo(s) base -> {len(all_rows)} linha(s) -> data.json / data.js atualizados")


class BaseFileHandler(FileSystemEventHandler):
    def __init__(self, folder: Path):
        self.folder = folder
        self._lock = threading.Lock()
        self._timer = None

    def _debounced_rebuild(self):
        # evita reconstruir varias vezes seguidas quando o SO dispara
        # multiplos eventos para a mesma gravacao de arquivo
        with self._lock:
            if self._timer:
                self._timer.cancel()
            self._timer = threading.Timer(0.7, lambda: rebuild(self.folder))
            self._timer.daemon = True
            self._timer.start()

    def on_any_event(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.name in ("data.json", "data.js"):
            return
        if is_base_file(path):
            print(f"[EVENTO] {event.event_type}: {path.name}")
            self._debounced_rebuild()


def start_server(folder: Path):
    os.chdir(folder)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"[SERVIDOR] Rodando em http://localhost:{PORT}  (pasta: {folder})")
        httpd.serve_forever()


def main():
    folder = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    if not folder.exists():
        print(f"ERRO: pasta nao encontrada: {folder}")
        sys.exit(1)

    print(f"Monitorando pasta: {folder}")
    print(f"Procurando arquivos que comecem com '{BASE_PREFIX}' (.csv, .xlsx, .xls)")

    rebuild(folder)  # gera o data.json/data.js com o que ja existir na pasta

    event_handler = BaseFileHandler(folder)
    observer = Observer()
    observer.schedule(event_handler, str(folder), recursive=False)
    observer.start()

    server_thread = threading.Thread(target=start_server, args=(folder,), daemon=True)
    server_thread.start()

    print("\nPronto! Deixe esta janela aberta.")
    print("Abra seu projeto em http://localhost:8000 no navegador.")
    print("Pressione CTRL+C para encerrar.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()

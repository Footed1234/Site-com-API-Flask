import os
import webbrowser
import subprocess
import time
import requests
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


def testar_conexao():
    try:
        with engine.begin() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Banco de dados conectado!")
        return True
    except Exception as e:
        print(f"❌ Erro no banco: {e}")
        return False


def aguardar_api_pronta(url, timeout=30):
    """Aguarda até que a API esteja respondendo"""
    print(f"⏳ Aguardando API ficar pronta em {url}...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print("✅ API está respondendo!")
                return True
        except requests.exceptions.RequestException:
            pass

        print(".", end="", flush=True)
        time.sleep(1)

    print(f"\n❌ Timeout: API não ficou pronta após {timeout} segundos")
    return False


if __name__ == "__main__":
    print("🎬 Iniciando Sistema CineRate...")

    # DEBUG: Mostra qual Python está sendo usado
    print(f"🔧 Python executando: {sys.executable}")
    print(f"🔧 Diretório atual: {os.getcwd()}")

    if testar_conexao():
        print("🚀 Iniciando API Flask...")

        try:
            # Usa o MESMO Python que está executando este script
            api_process = subprocess.Popen([sys.executable, "Consultar.py"])

            # URL base da API para testar
            url_base_api = "http://127.0.0.1:5000"
            url_afilmes = f"{url_base_api}/afilmes"

            # Aguarda a API ficar pronta
            if aguardar_api_pronta(url_afilmes):
                # URLs para abrir no navegador
                url_index = "http://localhost:63342/SqlFlask/templates/index.html?_ijt=60q993f4526vo1grpli6lsp6ir&_ij_reload=RELOAD_ON_SAVE"

                print(f"🌐 Abrindo {url_afilmes}")
                webbrowser.open(url_afilmes)

                time.sleep(2)

                print(f"🌐 Abrindo {url_index}")
                webbrowser.open_new_tab(url_index)

                print("✅ Sistema iniciado com sucesso!")
                print("⏹️  Pressione Ctrl+C para encerrar")

                try:
                    api_process.wait()
                except KeyboardInterrupt:
                    print("\n👋 Encerrando...")
                    api_process.terminate()
            else:
                print("❌ Não foi possível iniciar a API")
                api_process.terminate()

        except Exception as e:
            print(f"❌ Erro ao executar API: {e}")
            print("💡 Dica: Tente executar 'python Consultar.py' manualmente para ver o erro completo")

    else:
        print("❌ Falha na conexão com o banco.")
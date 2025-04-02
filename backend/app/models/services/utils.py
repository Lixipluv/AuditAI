import os

def ensure_directory_exists(directory, verbose=True):
    try:
        os.makedirs(directory, exist_ok=True)
        if verbose:
            print(f"✅ Diretório '{directory}' está pronto para uso.")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar diretório '{directory}': {e}")
        return False

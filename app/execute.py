import sys
import os

# Obtém o diretório atual do arquivo execute.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Obtém o caminho absoluto para o diretório "utils"
utils_path = os.path.join(current_dir, "utils")

# Adiciona o diretório "utils" ao caminho de busca do Python
sys.path.append(utils_path)

# Importa a classe ProcessUiObjectsFiles do arquivo "process_json_files.py"
from process_json_files import ProcessUiObjectsFiles

instancia_teste = ProcessUiObjectsFiles("data")

print(instancia_teste.extract_text_from_json_list())

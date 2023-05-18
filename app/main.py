# import sys
# import os
# import json

# # Obtém o caminho do diretório 'app'
# app_path = os.path.dirname(os.path.abspath(__file__))

# # Obtém o caminho do diretório 'text_extract_easy_ocr' (diretório principal)
# project_path = os.path.dirname(app_path)

# # Adiciona o diretório principal ao sys.path
# sys.path.append(project_path)

# # Importa a classe ProcessUiObjectsFiles do arquivo 'process_json_files.py'
# from utils.process_json_files import ProcessUiObjectsFiles
# from utils.process_image_files import ProcessImageFiles

# def main():
#     instancia_teste = ProcessUiObjectsFiles("data")
#     instancia_teste.extract_bounds_from_json_list()
#     image = ProcessImageFiles("data")

#     print(json.dumps(image.get_text_dict_in_words(instancia_teste.get_bound_list()), indent=4))


# if __name__ == "__main__":
#     main()

import sys
import os
import json
# Importa a classe ProcessUiObjectsFiles do arquivo 'process_json_files.py'
from utils.process_json_files import ProcessUiObjectsFiles
from utils.process_image_files import ProcessImageFiles

class AccessUtils(str):
    def __init__(self, path):
        self.path = path

    # Obtém o caminho do diretório 'app'
    app_path = os.path.dirname(os.path.abspath(__file__))

    # Obtém o caminho do diretório 'text_extract_easy_ocr' (diretório principal)
    project_path = os.path.dirname(app_path)

    # Adiciona o diretório principal ao sys.path
    sys.path.append(project_path)

    def main(self,path):
        instancia_teste = ProcessUiObjectsFiles(path)
        instancia_teste.get_text_dict_in_words() #garantir que get_json_files() sempre retorne a lista igual para extract_text_from_json_list() e extract_bounds_from_json_list()
        instancia_teste.extract_bounds_from_json_list()
        image = ProcessImageFiles(path)

        print(json.dumps(image.get_text_dict_in_words(instancia_teste.get_bound_list()), indent=4))
        print(json.dumps(instancia_teste.get_words_list(), indent=4))
        #print(json.dumps(instancia_teste.get_bound_list(), indent=4))

if __name__ == "__main__":
    exec = AccessUtils(str)
    exec.main()
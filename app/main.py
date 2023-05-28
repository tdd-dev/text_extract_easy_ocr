import sys
import os
import json
# Importa a classe ProcessUiObjectsFiles do arquivo 'process_json_files.py'
from utils.process_json_files import ProcessUiObjectsFiles
from utils.process_image_files import ProcessImageFiles
from utils.test import ProcessTesting

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
        image = ProcessImageFiles(path)
        testing = ProcessTesting(path)

        uiobjects_dict = instancia_teste.get_text_dict_in_words() #garantir que get_json_files() sempre retorne a lista igual para extract_text_from_json_list() e extract_bounds_from_json_list()
        instancia_teste.extract_bounds_from_json_list()
        image_dict = image.get_text_dict_in_words(instancia_teste.get_bound_list())
        test_results = testing.get_test_results_by_words(uiobjects_dict, image_dict)


        image.retest_with_kerasocr(testing.get_elements_with_fail())
        image_dict = image.get_words_dict()

        test_results = testing.get_test_results_by_words(uiobjects_dict, image_dict)
        test_results_by_image = testing.get_test_results_by_image_name()
        testing.organize_images()

        print(json.dumps(image_dict, indent=4))
        print("\n")
        print(json.dumps(uiobjects_dict, indent=4))
        print("\n")
        print(json.dumps(test_results, indent=4))
        print("\n")
        print(json.dumps(test_results_by_image, indent=4))
        #print(json.dumps(instancia_teste.get_bound_list(), indent=4))

if __name__ == "__main__":
    exec = AccessUtils(str)
    exec.main()
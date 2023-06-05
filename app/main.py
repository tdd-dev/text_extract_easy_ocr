import sys
import os
import json
import subprocess

# Importa a classe ProcessUiObjectsFiles do arquivo 'process_json_files.py'
from utils.process_json_files import ProcessUiObjectsFiles
from utils.process_image_files import ProcessImageFiles
from utils.test import ProcessTesting
from utils.preprocessing_yolo import PreprocessingYOLO

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
    
    def mainYolo(self,path):
        project_name = "text_extract_easy_ocr"
        model_path = r"app\utils\best.pt"
        # main_directory = path
        # print(os.listdir(model_path))
        print("PATHH: ", os.path.dirname(path))
        diretorios = path.split(os.path.sep)
        indice = diretorios.index(project_name)
        diretorio_pai = os.path.sep.join(diretorios[:indice+1])
        print("PAAATHH: ", diretorio_pai, path)
        print(os.listdir(diretorio_pai))
        
        status_bar_folder = "status-bar"
        path_status_bar = os.path.join(path, status_bar_folder)
        teste_classe = PreprocessingYOLO(path)
        teste_classe.crop_images(path)

        os.chdir(diretorio_pai)
        # # os.system(r'python C:\Users\rafae\Documents\UFAM\IARTE_icomp\projeto_final\text_extract_easy_ocr\app\utils\detect.py --weights C:\Users\rafae\Documents\UFAM\IARTE_icomp\projeto_final\text_extract_easy_ocr\app\utils\best.pt --img 1300 --conf 0.20 --source C:\Users\rafae\Documents\UFAM\IARTE_icomp\projeto_final\text_extract_easy_ocr\data\Yolo_samples\status-bar --line-thickness 1')
        command = [
            "python",
            r"app\utils\detect.py",
            "--weights",
            model_path,
            "--img",
            "1300",
            "--conf",
            "0.20",
            "--source",
            path_status_bar,
            "--line-thickness",
            "1"
        ]

        subprocess.run(command)        



if __name__ == "__main__":
    exec = AccessUtils(str)
    exec.main()
    exec.mainYolo()
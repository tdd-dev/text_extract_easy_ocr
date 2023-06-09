import sys
import os
import json
import subprocess
import datetime


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

    def mainOcr(self,path):
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

        # print(json.dumps(image_dict, indent=4))
        # print("\n")
        # print(json.dumps(uiobjects_dict, indent=4))
        # print("\n")
        # print(json.dumps(test_results, indent=4))
        # print("\n")
        #print(test_results_by_image)
        return json.dumps(test_results, indent=4)
        #print(json.dumps(instancia_teste.get_bound_list(), indent=4))
    

    def mainYolo(self, path):
        project_name = "text_extract_easy_ocr"
        model_path = os.path.join("app", "utils", "best.pt")
        yaml_path = os.path.join("app", "utils", "classes_statusbar.yaml")

        # Obter o diretório pai
        diretorios = path.split(os.path.sep)
        indice = diretorios.index(project_name)
        diretorio_pai = os.path.sep.join(diretorios[:indice+1])

        # Obter o timestamp atual
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")

        # Definir caminhos
        status_bar_folder = "status-bar"
        path_status_bar = os.path.join(path, status_bar_folder)
        path_imgs_result = os.path.join("data", "Test Results/yolo")
        path_imgs_inferencia = os.path.join(path_imgs_result, f"exp_{timestamp}")
        path_imgs_classes_found = os.path.join(path_imgs_inferencia, "labels")

        # Criar uma instância de PreprocessingYOLO
        preprocessing_yolo = PreprocessingYOLO(path)

        # Realizar o pré-processamento de imagens
        preprocessing_yolo.crop_images(path)

        # Alterar o diretório para o diretório pai
        os.chdir(diretorio_pai)

        # Executar o comando de detecção de objetos
        command = [
            "python",
            os.path.join("app", "utils", "detect.py"),
            "--weights", model_path,
            "--img", "1300",
            "--conf", "0.20",
            "--source", path_status_bar,
            "--project", path_imgs_result,
            "--name", f"exp_{timestamp}",
            "--line-thickness", "1",
            "--save-txt",
            "--save-conf"
        ]
        subprocess.run(command)

        # Criar uma instância de PreprocessingYOLO para comparar resultados
        compare_results = PreprocessingYOLO(path)

        # Formatar os resultados e retornar o resultado
        return compare_results.format_txt(yaml_path, path_imgs_classes_found, path_imgs_inferencia, diretorio_pai)
    
    def mainYolo2(self, path):
        project_name = "text_extract_easy_ocr"
        model_path = os.path.join("app", "utils", "best2.pt")
        yaml_path = os.path.join("app", "utils", "classes_statusbar.yaml")

        # Obter o diretório pai
        diretorios = path.split(os.path.sep)
        indice = diretorios.index(project_name)
        diretorio_pai = os.path.sep.join(diretorios[:indice+1])

        # Obter o timestamp atual
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")

        # Definir caminhos
        status_bar_folder = "status-bar"
        path_status_bar = os.path.join(path, status_bar_folder)
        path_imgs_result = os.path.join("data", "Test Results/yolo")
        path_imgs_inferencia = os.path.join(path_imgs_result, f"exp_{timestamp}_model2")
        path_imgs_classes_found = os.path.join(path_imgs_inferencia, "labels")

        # Criar uma instância de PreprocessingYOLO
        preprocessing_yolo = PreprocessingYOLO(path)

        # Realizar o pré-processamento de imagens
        preprocessing_yolo.crop_images(path)

        # Alterar o diretório para o diretório pai
        os.chdir(diretorio_pai)

        # Executar o comando de detecção de objetos
        command = [
            "python",
            os.path.join("app", "utils", "detect.py"),
            "--weights", model_path,
            "--img", "1300",
            "--conf", "0.20",
            "--source", path_status_bar,
            "--project", path_imgs_result,
            "--name", f"exp_{timestamp}_model2",
            "--line-thickness", "1",
            "--save-txt",
            "--save-conf"
        ]
        subprocess.run(command)

        # Criar uma instância de PreprocessingYOLO para comparar resultados
        compare_results = PreprocessingYOLO(path)

        # Formatar os resultados e retornar o resultado
        return compare_results.format_txt(yaml_path, path_imgs_classes_found, path_imgs_inferencia, diretorio_pai)

    def mainImages(self,path):
        getImgPath = ProcessImageFiles(path)
        img_list = getImgPath.get_jpg_files(path)
        new_img_list = []
        for img in img_list:
            index = img.find('data')
            if index != -1:
                result = img[index:]
                new_img_list.append(result)
            else:
                print("Word 'data' not found on directory path.")
        print(new_img_list)
        return new_img_list

if __name__ == "__main__":
    exec = AccessUtils(str)
    exec.mainOcr()
    exec.mainYolo()
    exec.mainImages()

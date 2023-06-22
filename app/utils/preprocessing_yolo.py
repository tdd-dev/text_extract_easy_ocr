import os 
import cv2
import yaml 
import json
class PreprocessingYOLO(str):
    def __init__(self, path):
        self.path = path

    def crop_images(self, path):
        directory_path = path
        # rico_coordinates = 
        
        for image_file in os.listdir(directory_path):
            if image_file.endswith(".jpg" or ".png" or ".jpeg"):
                path_total = os.path.join(path, image_file)
                image = cv2.imread(path_total)
                roi_cropped=image[int(2):int(2+65), int(0):int(0+1080)]
                nome_pasta = "status-bar"
                path_status_bar = os.path.join(path, nome_pasta)
                if os.path.exists(path_status_bar):
                    pass
                else:
                    os.makedirs(path_status_bar) 
                os.chdir(path_status_bar)
                # print("PATHH no crop: ", os.getcwd())
                cv2.imwrite("%s" %image_file, roi_cropped)
                os.chdir(path)
            else:
                print(f"{image_file} Não é um arquivo de imagem")
                # print("PATHH no FIM : ", os.getcwd())
            # completeName = os.path.join(path_status_bar, new_image)
    
    def format_txt(self, path_yaml, path_txt, path_results, path_main):
        with open(path_yaml) as file_yaml:
            yaml_data = yaml.load(file_yaml, Loader=yaml.FullLoader)
        # Criar uma lista para armazenar os resultados da comparação
        results = []

        txt_files = os.listdir(path_txt)
        os.chdir(path_txt)

        for txt_file in txt_files:
            result = {
                'arquivo': txt_file,
                'comparacoes': []
            }

            with open(txt_file) as file_txt:
                text_data = file_txt.readlines()  
        
            text_data = [line.strip().split() for line in text_data]

            for line in text_data:
                key = int(line[0])
                if key in yaml_data['names']:
                    value = yaml_data['names'][key]
                else:
                    value = 'Não encontrado'
                result['comparacoes'].append({'chave': key, 'valor': value})

            results.append(result)
        os.chdir(path_main)
        json_file = f"{path_results}/results.json"
        # print("JSON PATHHH: ", json_file )
        with open(json_file, 'w') as file:
            json.dump(results, file, indent=4)
    
        print(f"Os resultados foram salvos no diretorio {json_file}.")
        return json_file

    def flush_status_bar_folder(self, path):
        pass
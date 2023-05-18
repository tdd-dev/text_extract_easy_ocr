import os
import json
import re
import easyocr
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import time


class ProcessImageFiles(str):
    def __init__(self, path):
        self.path = path
        
    def get_jpg_files(self,path):
        directory_path = path

        # define extensão
        json_ext = ".jpg"

        # Lista para adicionar nomes dos arquivos json
        file_names = []

        # Loop para buscar por todos os nomes dos files .json do diretorio
        for filename in os.listdir(directory_path):
            # Obtem cada um dos arquivos
            _, ext = os.path.splitext(filename)
            # Se a extensão for json adiciona na lista todos os arquivos
            if ext == json_ext:
                file_names.append(filename)

        file_paths = []

        for name in file_names:
            # Associa nome do arquivo com o path dele
            file_path = os.path.join(directory_path, name)
            # adiciona na lista somente o path
            file_paths.append(file_path)
        
        # Retorna a lista com o paths dos arquivos json
        return file_paths

    #print(get_json_files('../data'))

    def get_png_files(self, path):
        return 0

    def get_text_with_easyocr(self, file_name):
        # Cria o objeto de reconhecimento de texto com detecção automática de idioma
        leitor = easyocr.Reader(['en'])

        # Lê o texto em uma imagem
        resultados = leitor.readtext(file_name)

        # Extrai somente os textos das regiões detectadas
        textos = [resultado[1] for resultado in resultados]

        # Imprime os textos extraídos
        return textos
        

    #Função que retorna elementos de texto e bounds dado um arquivo json de entrada

    def extract_text_from_jpg_list(self,bound_dict):

        new_coordinates_dict = {}
        for image_name, coordinates in bound_dict.items():
            new_coordinates_dict[image_name] = {}
            image_folder = os.path.join(self.path, os.path.splitext(image_name)[0])  # Cria o caminho da pasta da imagem
            os.makedirs(image_folder, exist_ok=True)  # Cria a pasta da imagem se ela não existir
            image_path = os.path.join(self.path, f"{image_name}.jpg")
            img = Image.open(image_path)
            
            for text_id, bounds in coordinates.items():
                x1, y1, x2, y2 = bounds
                
                # Escalonamento
                x3 = (x1 / 1440) * img.size[0]
                y3 = (y1 / 2560) * img.size[1]
                x4 = (x2 / 1440) * img.size[0]
                y4 = (y2 / 2560) * img.size[1]
                
                # Crop da imagem usando bounds
                cropped_img = img.crop((x3, y3, x4, y4))
                
                # Mostrar a nova imagem
                #cropped_img.show()
                
                # Salvar a nova imagem
                new_image_path = os.path.join(image_folder, f"new_{os.path.splitext(image_name)[0]}_{text_id}.jpg")
                cropped_img.save(new_image_path)
                
                # Processar a imagem e obter a lista de textos detectados
                text_list_ocr = self.get_text_with_easyocr(new_image_path)
                new_coordinates_dict[image_name][text_id] = text_list_ocr
        
        return new_coordinates_dict

    def get_text_dict_in_words(self, bound_list):
        processed_dict = {}
        input_dict = self.extract_text_from_jpg_list(bound_list)
        for key, value in input_dict.items():
            processed_value = {}
            for subkey, subvalue in value.items():
                # Coloca todas as letras em minúsculas
                subvalue = str(subvalue).lower()
                # Remove os caracteres especiais
                subvalue = re.sub(r'[^a-zA-Z0-9]', ' ', subvalue)
                # Separa as palavras
                words = re.findall(r'\w+', subvalue)
                processed_value[subkey] = words
            processed_dict[key] = processed_value
        return processed_dict


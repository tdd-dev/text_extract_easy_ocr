import os
import json
import re

class ProcessUiObjectsFiles(str):
    
    def __init__(self, path):
        self.path = path
        self.texts_from_json={}
        self.bounds_from_json={}
        
    def get_json_files(self,path):
        directory_path = path

        # define extensão
        json_ext = ".json"

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

    def get_xml_files(self, path):
        return 0
    
    def get_bound_list(self):
        return self.bounds_from_json
    
    def get_text_list(self):
        return self.texts_from_json

    #Função que retorna elementos de texto e bounds dado um arquivo json de entrada
    def extract_info_from_json(self,data):
        text_elements = []
        stack = [data]
        
        while stack:
            current = stack.pop()
            
            if isinstance(current, dict):
                if 'text' in current:
                    text_element = {'text': current.get('text', ''), 'bounds': current.get('bounds', []), 'visible': current.get('visible-to-user', '')}
                    if text_element['visible']:
                        text_elements.append(text_element)
                
                stack.extend(current.values())
            
            elif isinstance(current, list):
                stack.extend(current)
        
        return text_elements

    # def extract_text_elements(self,data):
        text_elements = []
        stack = [data]
        
        while stack:
            current = stack.pop()
            
            if isinstance(current, dict):
                if 'text' in current:
                    text_element = {'text': current.get('text', ''), 'bounds': current.get('bounds', []), 'visible': current.get('visible-to-user', '')}
                    if text_element['visible']:
                        text_elements.append(text_element)
                
                stack.extend(current.values())
            
            elif isinstance(current, list):
                stack.extend(current)
        
        return text_elements


    # Extrai todos os textos de uma lista de json
    def extract_text_from_json_list(self):
        file_path_list = self.get_json_files(self)

        
        result = {}  # Dicionário para armazenar todos os dicionários enumerados

        # Percorre todos os arquivos no diretório
        for file_name in file_path_list:
                #texts_list = []
                text_list_per_file = []                
                # Lê o conteúdo do arquivo JSON
                with open(file_name) as f:
                    data = json.load(f)
                text_elements = self.extract_info_from_json(data)
                # Cria um dicionário enumerado com os elementos do arquivo JSON
                
                for text in text_elements:
                # se não for valor vazio ele adiciona setando somente a propriedade de text
                    if text["text"] != "":
                        text_list_per_file.append(text["text"])
                #texts_list.append(text_list_per_file)

                #Enumera dicionario de textos
                dict_texts = {index: value for index, value in enumerate(text_list_per_file)}
                
                file = os.path.basename(file_name)  # Obtém o nome do arquivo com a extensão
                id = os.path.splitext(file)[0]
                # Armazena o dicionário enumerado no dicionário principal
                result[id] = dict_texts
                self.texts_from_json = result

        # # Imprime a saída com todos os elementos enumerados
        # for nome_arquivo, elementos in resultado.items():
        #     print(f"Arquivo: {nome_arquivo}")
        #     for indice, valor in elementos.items():
        #         print(f"{indice}: {valor}")
        #     print()

        return result

    def extract_bounds_from_json_list(self):
        file_path_list = self.get_json_files(self)
        result = {}  # Dicionário para armazenar todos os dicionários enumerados

        # Percorre todos os arquivos no diretório
        for file_name in file_path_list:
                #texts_list = []
                bound_list_per_file = []                
                # Lê o conteúdo do arquivo JSON
                with open(file_name) as f:
                    data = json.load(f)
                text_elements = self.extract_info_from_json(data)
                # Cria um dicionário enumerado com os elementos do arquivo JSON
                
                for text in text_elements:
                # se não for valor vazio ele adiciona setando somente a propriedade de text
                    if text["text"] != "":
                        bound_list_per_file.append(text["bounds"])
                #texts_list.append(text_list_per_file)

                #Enumera dicionario de textos
                dict_texts = {index: value for index, value in enumerate(bound_list_per_file)}
                
                file = os.path.basename(file_name)  # Obtém o nome do arquivo com a extensão
                id = os.path.splitext(file)[0]
                # Armazena o dicionário enumerado no dicionário principal
                result[id] = dict_texts
                self.bounds_from_json = result

        # # Imprime a saída com todos os elementos enumerados
        # for nome_arquivo, elementos in resultado.items():
        #     print(f"Arquivo: {nome_arquivo}")
        #     for indice, valor in elementos.items():
        #         print(f"{indice}: {valor}")
        #     print()

        return result


    def get_text_dict_in_words(self):
        processed_dict = {}
        input_dict = self.extract_text_from_json_list()
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


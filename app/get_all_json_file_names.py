import os
import json
import re

class ProcessTextFromJsonFiles(str):
    def __init__(self, path):
        self.path = path
        
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
            

    def extract_text_elements(self,data):
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


    def extract_text_from_all_json_files(self):
        texts_list = []
        file_path_list = self.get_json_files(self)
        # loop para percorrer toda a lista de nomes de arquivos
        for path in file_path_list:
            text_list_per_file = []
            # insere o path a partir do nome para obter o arquivo correspondente
            with open(path) as f:
                data = json.load(f)
            # executa o metodo para extrair os textos e bounds de cada um dos arquivos json da lista
            text_elements = self.extract_text_elements(data)
            # adiciona o texto encontrado em cada arquivo json ao vetor de texto
            for text in text_elements:
                # se não for valor vazio ele adiciona setando somente a propriedade de text
                if text["text"] != "":
                    text_list_per_file.append(text["text"])
            texts_list.append(text_list_per_file)
        # pega a lista de textos de cada json e enumera para servir como rotulo
        text_dict = {i: item for i, item in enumerate(texts_list)}
        return text_dict
        

    def extract_bounds_from_all_json_files(self):
        bounds_list = []
        file_path_list = self.get_json_files(self)
        # loop para percorrer toda a lista de nomes de arquivos
        for path in file_path_list:
            bounds_list_per_file = []
            # insere o path a partir do nome para obter o arquivo correspondente
            with open(path) as f:
                data = json.load(f)
            # executa o metodo para extrair os textos e bounds de cada um dos arquivos json da lista
            text_elements = self.extract_text_elements(data)
            # adiciona o bound encontrado em cada arquivo json ao vetor de bound
            for bound in text_elements:
                # se não for valor vazio ele adiciona setando somente a propriedade de text
                if bound["text"] != "":
                    bounds_list_per_file.append(bound["bounds"])
            bounds_list.append(bounds_list_per_file)
        return bounds_list


    def process_text_dict(self):
        processed_dict = {}
        text_dict = self.extract_text_from_all_json_files()
        for key, value in text_dict.items():
            if isinstance(value, list):
                # mantem cada palavra da frase dentro da mesma lista
                value = ' '.join(value)
            # Coloca todas as letras em minúsculas
            value = str(value).lower()
            # Separa as palavras
            words = re.findall(r'\w+', value)
            # Remove os caracteres especiais
            processed_words = [re.sub(r'[^a-zA-Z0-9]', '', word) for word in words]
            # Remove as palavras vazias
            processed_words = [word for word in processed_words if word]
            processed_dict[key] = processed_words
        return processed_dict


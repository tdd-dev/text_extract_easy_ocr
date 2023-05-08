import os
import json
import re
def get_json_files(path):
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
        

def extract_text_elements(data):
    """
    Função que extrai elementos de texto e seus bounds de um arquivo JSON
    :param data: Dicionário contendo a hierarquia de elementos do arquivo JSON
    :return: Lista de dicionários contendo as propriedades de "text" e "bounds" dos elementos de texto
    """
    text_elements = []
    
    # Verifica se a hierarquia de elementos é uma lista
    if isinstance(data, list):
        for item in data:
            text_elements += extract_text_elements(item)
            
    # Verifica se a hierarquia de elementos é um dicionário
    elif isinstance(data, dict):
        # Verifica se o elemento é de texto
        if 'text' in data:
            # Adiciona as propriedades de "text" e "bounds" a lista de resultados
            text_element = {'text': data.get('text', ''), 'bounds': data.get('bounds', []),'visible': data.get('visible-to-user','')}
            if text_element["visible"]:
              text_elements.append(text_element)
        
        # Chama a função recursivamente para continuar a busca por elementos de texto na hierarquia
        for key, value in data.items():
            text_elements += extract_text_elements(value)
    
    return text_elements

def extract_text_from_all_json_files(file_path_list):
    texts_list = []
    # loop para percorrer toda a lista de nomes de arquivos
    for path in file_path_list:
        text_list_per_file = []
        # insere o path a partir do nome para obter o arquivo correspondente
        with open(path) as f:
            data = json.load(f)
        # executa o metodo para extrair os textos e bounds de cada um dos arquivos json da lista
        text_elements = extract_text_elements(data)
        # adiciona o texto encontrado em cada arquivo json ao vetor de texto
        for text in text_elements:
            # se não for valor vazio ele adiciona setando somente a propriedade de text
            if text["text"] != "":
                text_list_per_file.append(text["text"])
        texts_list.append(text_list_per_file)
    # pega a lista de textos de cada json e enumera para servir como rotulo
    text_dict = {i: item for i, item in enumerate(texts_list)}
    return text_dict
    

#print(extract_text_from_all_json_files(get_json_files('data')))

def extract_bounds_from_all_json_files(file_path_list):
    bounds_list = []
    # loop para percorrer toda a lista de nomes de arquivos
    for path in file_path_list:
        bounds_list_per_file = []
        # insere o path a partir do nome para obter o arquivo correspondente
        with open(path) as f:
            data = json.load(f)
        # executa o metodo para extrair os textos e bounds de cada um dos arquivos json da lista
        text_elements = extract_text_elements(data)
        # adiciona o bound encontrado em cada arquivo json ao vetor de bound
        for bound in text_elements:
            # se não for valor vazio ele adiciona setando somente a propriedade de text
            if bound["text"] != "":
                bounds_list_per_file.append(bound["bounds"])
        bounds_list.append(bounds_list_per_file)
    return bounds_list

#print(extract_bounds_from_all_json_files(get_json_files('data')))


def process_text_dict(text_dict):
    processed_dict = {}
    for key, value in text_dict.items():
        if isinstance(value, list):
            # Join the list elements into a single string
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

print(process_text_dict(extract_text_from_all_json_files(get_json_files('data'))))
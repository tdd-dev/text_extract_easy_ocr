import os
import json
import re
import shutil

class ProcessTesting(str):
    
    def __init__(self, path):
        self.path = path
        self.words_results = {}
    
    def get_test_results_by_image_name(self):
        processed_dict = {}

        for key, value in self.words_results.items():
            if all(val == "PASS" for val in value.values()):
                processed_dict[key] = "PASS"
            else:
                processed_dict[key] = "FAIL"

        return processed_dict

    def get_test_results_by_words(self, uiobjects_dict, ocr_dict):
        result = {}

        for key1, value1 in uiobjects_dict.items():
            if key1 in ocr_dict:
                result[key1] = {}
                for key2, value2 in value1.items():
                    if key2 in ocr_dict[key1]:
                        set1 = set(value2)
                        set2 = set(ocr_dict[key1][key2])
                        if set1.issubset(set2):
                            result[key1][key2] = "PASS"
                        else:
                            result[key1][key2] = "FAIL"
                    else:
                        result[key1][key2] = "FAIL"
            else:
                result[key1] = {key2: "FAIL" for key2 in value1}
            
        self.words_results = result
        return result

    def get_elements_with_fail(self):
        elements_with_fail = {}

        for key, value in self.words_results.items():
            if "FAIL" in value.values():
                elements_with_fail[key] = {}

                for subkey, subvalue in value.items():
                    if subvalue == "FAIL":
                        elements_with_fail[key][subkey] = subvalue

        return elements_with_fail
    
    def organize_images(self):
        test_results_path = os.path.join(self.path, "Test Results")

        # Verifica se a pasta "Test Results" já existe
        if not os.path.exists(test_results_path):
            os.makedirs(test_results_path)

        for folder, inner_dict in self.words_results.items():
            folder_path = os.path.join(test_results_path, folder)
            pass_folder = os.path.join(folder_path, "PASS")
            fail_folder = os.path.join(folder_path, "FAIL")

            # Verifica se a pasta "PASS" já existe
            if not os.path.exists(pass_folder):
                os.makedirs(pass_folder)

            # Verifica se a pasta "FAIL" já existe
            if not os.path.exists(fail_folder):
                os.makedirs(fail_folder)

            # Copia a imagem "mãe" para as pastas "PASS" e "FAIL"
            original_image = f"{folder}.jpg"
            shutil.copy2(os.path.join(self.path, original_image), pass_folder)
            shutil.copy2(os.path.join(self.path, original_image), fail_folder)

            for key, value in inner_dict.items():
                image_name = f"new_{folder}_{key}.jpg"
                source_path = os.path.join(self.path, folder, image_name)

                if value == "PASS":
                    destination_path = os.path.join(pass_folder, image_name)
                elif value == "FAIL":
                    destination_path = os.path.join(fail_folder, image_name)
                else:
                    continue

                shutil.move(source_path, destination_path)
        for folder, inner_dict in self.words_results.items():
            folder_path = os.path.join(self.path, folder)
            shutil.rmtree(folder_path)



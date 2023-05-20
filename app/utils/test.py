import os
import json
import re

class ProcessTesting():
    
    def __init__(self):
        self.words_results = {}
    
        '''
        {
                
                "13":
                        {
                        "0": "PASS"
                        "1": "FAIL"
                        "2": "PASS"
                        }
                "17":
                        {
                        "0": "PASS"
                        "1": "FAIL"
                        "2": "PASS"
                        }

        }
        '''

    # def get_test_results_by_text(self):
    #     return 0

        '''
        {
                
                "13":
                        {
                        "This is a test": "PASS"
                        "This is a element from RICO": "FAIL"
                        "Sei la": "PASS"
                        }
                "17":
                        {
                        "Top demais": "PASS"
                        "Luiz Felipe": "FAIL"
                        "Lucas Santos": "PASS"
                        }
        }
        '''

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



        '''
            {
                
                "13":
                        {
                        "0": ["This", "is", "a", "test"]
                        "1": ["This", "is", "a", "element"]
                        "2": ["Luiz", "Eduardo"]
                        }
                "17":
                        {
                        "0": ["isso", "é", "um", "texto"]
                        "1": ["ia", "é", "top"]
                        "2": ["easy","ocr","é", "bom"]
                        }
            }


            {
                
                "13":
                        {
                        "0": ["adad", This", "is", "a", "test","hd"]
                        "1": ["This", "adsa", "is", "a", "element"]
                        "2": ["Luiz", "Eduardo", "asbhdja"]
                        }
                "17":
                        {
                        "0": ["xxx", "isso", "ddd", "é", "um", "texto"]
                        "1": ["ia", "sfls", "é", "top", "daa"]
                        "2": ["easy","dsa", "ocr","é", "bom"]
                        }
            }
        '''
    
import os 
import cv2

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
    
    # def moving_files(self):

    
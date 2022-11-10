import cv2
import os
from statistics import mode

# For streams:
#   cap = cv2.VideoCapture('rtsp://url.to.stream/media.amqp')
# Or e.g. most common ID for webcams:
#   cap = cv2.VideoCapture(0)
def gerador_df():
    count = 0

    path = "/home/lucas/Documentos/temp/VolusomDasa"
    dirs = os.listdir( path )
    print(dirs)

    # This would print all the files and directories
    aux = 0
    for file in dirs:
        file = path + "/"+file
        print(file)
        cap = cv2.VideoCapture(file)
        count = 0
        

        while cap.isOpened():
            ret, frame = cap.read()

            if ret:
                cv2.imwrite('{0}/VolusomDasa{1}_{2}.jpg'.format(path,aux,count), frame)
                count += 60 # i.e. at 30 fps, this advances one second
                cap.set(cv2.CAP_PROP_POS_FRAMES, count)
                
            else:
                cap.release()
                break
        aux = aux + 1


def pause():
    programPause = input("Press the <ENTER> key to continue...")
    return

def treinar_yolo():
    '''
    Este código foi feito com objetivo de automatizar a criação e organizaçao de data trains, para o YOLOV5, para utilizar basta mudar o diretorio da pastar contento as pastas com as imagens anotadas, com isso o script separa as imagens de forma aleatoria, em trainamento e validação.
    '''
    print("=============================================")
    print("===BEM VINDO A CONFIGURAÇÃO DE TREINAMENTO===")
    print("=============================================\n\n\n")
    pause()
    count = 0
    path = "/home/lucas/Documentos/ModeloModos/"
    dirs = os.listdir(path)


    #Criação das pastas do df
    print("Criandos pastas do data train...\n\n")

    path_df = path+"train_data" 
    path_df_images = path_df+"/image"
    path_images_train = path_df_images+"/train"
    path_images_val = path_df_images+"/val"

    path_df_labels = path_df+"/labels"
    path_labels_train = path_df_labels+"/train"
    path_labels_val = path_df_labels+"/val"

    try:
        os.mkdir(path_df)
        os.mkdir(path_df_images)
        os.mkdir(path_images_train)
        os.mkdir(path_images_val)

        os.mkdir(path_df_labels)
        os.mkdir(path_labels_train)
        os.mkdir(path_labels_val)
        print("Diretorios criados!")
    except Exception as e:
        print("Ja encontramos o diretorio!!")

    print("\n\nIniciando separação das imagens e labels...")    

    for paste in dirs:
        if paste != "train_data" and paste != "coco128.yaml":
            path_paste = path+paste
            dirs_paste = os.listdir(path_paste)
            aux = round(len(dirs_paste) * 0.3)
            print(aux)
            count = 0

            for file in dirs_paste:
                ext = file[-4:]
                file_ext = file[:-4]

                if count < aux and ext == ".jpg":
                    new_file = paste+"_"+file_ext+"_val"+ext
                    txt_file = paste+"_"+file_ext+"_val.txt"
                    print(new_file)
                    os.rename(path_paste+"/"+file, path_images_val+"/"+new_file)
                    os.rename(path_paste+"/"+file_ext+".txt", path_labels_val+"/"+txt_file)

                if count > aux and ext == ".jpg":
                    new_file = paste+"_"+file_ext+"_train"+ext
                    txt_file = paste+"_"+file_ext+"_train.txt"
                    os.rename(path_paste+"/"+file, path_images_train+"/"+new_file)
                    os.rename(path_paste+"/"+file_ext+".txt", path_labels_train+"/"+txt_file)



                count = count + 1




    #Prepara o arquivo de configuração
    
    labels = []
    while True:
        print("Digite os nomes das Label em ordem! Quando acabar digite 0.")
        x = input("Label: ")
        print(x)
        if x == "0":
            break
        else:
            labels.append(x)
    
    txt_names = "names: \n"
    aux = 0
    for i in labels:
        txt_names = txt_names+"  "+str(aux)+": "+i+"\n"
    
    print("Gerando arquivo de configuração: "+path_df)

    txt_yaml = "path: "+ path_df +"\ntrain: "+path_images_train+"\nval: "+path_images_val + "\ntest: \n\n\n"+txt_names


    nome_arquivo = path+"coco128.yaml"
    arquivo = open(nome_arquivo, 'w')
    arquivo.writelines(txt_yaml)
    arquivo.close()


    peso = input("Nome do peso a ser utilizado: .\n0 para usar um peso padrão (yolov5l.pt). \nObs o peso deve estar na pasta do YoloV5")
    if(peso == "0"):
        peso = "yolov5l.pt"

    yolo_train = "python3 train.py --img 256 --batch 8 --epochs 40 --data "+nome_arquivo+"--weights "+peso+" --cache"

    os.system(yolo_train)

gerador_df()
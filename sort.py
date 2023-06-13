import os
import sys
import shutil


baza_for_filtr = {
'images': ('JPEG', 'PNG', 'JPG', 'SVG'),
'video': ('AVI', 'MP4', 'MOV', 'MKV'),
'documents': ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
'audio': ('MP3', 'OGG', 'WAV', 'AMR', 'M4A'),
'archives': ('ZIP', 'GZ', 'TAR', 'RAR'),
}


# main_path = r'C:\Users\LeonShell\Desktop\test_2dz – копія – копія'


baz_fold = []
baz_file = []


# !!! Для транслітерації
def normalize(name):
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ @#$%^&(),"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_")
    TRANS = {}
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    name = name.translate(TRANS)
    
    return name



# Створюю нові папки необхідні для сортування
def create_folders_from_list(folder_path, folder_names):
    new_folders_list = []
    for folder in folder_names:
        new_folders_list.append(f'{folder_path}\\{folder}')
        if not os.path.exists(f'{folder_path}\\{folder}'):
            os.mkdir(f'{folder_path}\\{folder}')

    return new_folders_list




def get_Folder_list(folders_paths, excluz):
    pathess = os.scandir(folders_paths)
    for path in pathess:
        if path.path not in excluz:
            if path.is_file():
                baz_file.append(path.path)
            if path.is_dir():
                baz_fold.append(path.path)
                sub_path = os.scandir(path)
                get_Folder_list(path.path, excluz)
    
    return  baz_file, baz_fold



def get_rename_files(files):
    new_list_files = []
    exe_list_in_baza = list(baza_for_filtr.items()) 
    for f in files:
        for name in f:
            if '.' in name:
                name_ = name.split('\\')[-1]
                name_path = name.split(name_)[-2]
                new_name = name_path  + normalize(name_)
                os.rename(name, new_name)
                new_list_files.append(new_name) 
    return new_list_files



def get_move_files(files):
    a = get_Folder_list(main_path, create_folders_from_list(main_path, baza_for_filtr))
    exe_list_in_baza = list(baza_for_filtr.items())
    adrenal = 0
    for name in files:
        name_exe = name.split('.')[-1]
        name_ = name.split('\\')[-1]
        name_path = name.split(name_)[-2]
        for dict_key_int in range(len(exe_list_in_baza)):
            if name_exe.upper() in exe_list_in_baza[dict_key_int][1]:
                new_name = main_path + f"\{exe_list_in_baza[dict_key_int][0]}\\" + name_
                try:    
                    shutil.move(f'{name_path}\{name_}', f'{main_path}\{exe_list_in_baza[dict_key_int][0]}\{name_}')
                except:
                    if FileNotFoundError:
                        adrenal = 1
                        continue
                        
                    if RecursionError:
                        adrenal = 1
                        continue
                        
    return adrenal



# Видаляю порожні папки
def remove_empty_folders(baz_files):
    for f in baz_files:
        for fold in f:
            if '.' not in fold:
                try:
                    fold_name = fold.split('\\')[-1]
                    if not os.listdir(fold):
                        print('Видалено порожню папку:', fold.split('\\')[-1], '\n')
                        os.rmdir(fold)
                        remove_empty_folders(baz_files)
                except: FileNotFoundError
    
       
        
# Розпакування архівів
def unpack_archives(catalog):
    for arch_name in catalog:
        if arch_name.split('\\')[-1] == 'archives':
            arch_list  = os.scandir(arch_name)
            for arch in arch_list:
                arch_name = arch.path
                arch_name = str(arch_name)
                arch_name = arch_name.replace("['", '')
                arch_name = arch_name.replace("']", '')
                direct = arch_name.split('\\')[-2]
                name_for_move = arch_name.split('\\')[-1]
                folder_for_unpack = arch_name.split('\\')[-1]
                folder_for_unpack = folder_for_unpack.split('.')[-2]
                shutil.unpack_archive(arch_name, rf'{main_path}\{direct}\{folder_for_unpack}')
                os.rename(arch_name, f'{main_path}\{direct}\{folder_for_unpack}\{name_for_move}')
                return print('Ok!')
            


# Пеейменування папок
def get_rename_folders(folder_path):
    rename_list =[]
    for data in folder_path:
        for folder in data:
            if '.' not in folder:
                if folder not in rename_list:
                    rename_list.append(folder)
        rename_list.reverse()
        for folder in rename_list:
            name_folder = folder.split('\\')[-1]
            print(name_folder)
            patch_folder = folder.split(name_folder)[-2]
            print(patch_folder)
            os.rename(folder, f'{patch_folder}{normalize(name_folder)}')



def get_sort(folder_path):
    excluz = create_folders_from_list(folder_path, baza_for_filtr)
    baz_files = get_Folder_list(folder_path, excluz)
    new_baz_file = get_rename_files(baz_files)
    adrenal = get_move_files(new_baz_file)
    if adrenal >= 1:
        adrenal = get_move_files(new_baz_file)
    remove_empty_folders(baz_files)
    unpack_archives(excluz)
    get_rename_folders(baz_files)




#main_path = input('Введіть адресу папки дя сортування файлів: ')
main_path = sys.argv[1]
get_sort(main_path)
print()
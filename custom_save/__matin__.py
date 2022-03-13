"""
Ce script permet d'enregistrer les fichiers importants (donnés dans 'list_dir_to_screen')
dans un disque dur.
Si aucun disque dur n'est connecté, une exception est retournée.
Le script ne fait que créer un nouveau fichier avec comme nom la date courante, et copie colle
bêtement tous les fichiers présents dans la liste 'list_dir_to_screen'.

Une amélioration future sera d'enregistrer uniquement les gros fichiers (musique, photos etc).
Il faudra pour cela comparer fichiers déjà enregitrés et à enregistrer.

"""


import os
import datetime
import shutil
import errno

CURRENT_PATH = os.getcwd()
DESKTOP_PATH = r"C:\Users\User1\Desktop"
# Desktop = os.path.join(CURRENT_PATH, "Desktop")
hard_disk_path = r"G:zScreenshots"

list_dir_to_screen = [
    "Le Dossier/Comptes",
    "Le dossier/Informations privées",
    "Moi et le sport",
    "Ma psychologie ou vie"
]

def hardDiskDetected(hard_disk_path):
    if os.path.isdir(hard_disk_path) == True:
        print("Detected")
        return True
    else:
        print("No disk detected")
        return False
    
def dirToScreenDetected(PATH_TO_DIR, list_dir_to_screen):
    for file in list_dir_to_screen:
        path_to_check = os.path.join(PATH_TO_DIR, file)
        if os.path.isdir(path_to_check) == False:
            print("Fichier non trouvé : ", file)
            return False
    return True
    
def screenOfTheDay(DESKTOP_PATH, list_dir_to_screen, hard_disk_path):
    path_screen_day = create_dir_day_screen(hard_disk_path)
    if path_screen_day == False:
        raise Exception
    for directory in list_dir_to_screen:
        path_from = os.path.join(DESKTOP_PATH, directory)
        path_to = os.path.join(path_screen_day, directory)
        createSubDirs(path_screen_day, directory)
        copy(path_from, path_to)
    print("Copy done")
    
def create_dir_day_screen(hard_disk_path):
    date = datetime.date.today()
    name_screen = "Screenshot_python_" + str(date)
    path_screen_day = os.path.join(hard_disk_path, name_screen)
    try:
        shutil.rmtree(path_screen_day)
    except FileNotFoundError:
        pass
    os.mkdir(path_screen_day)
        
    if os.path.isdir(path_screen_day):
        return path_screen_day
    else:
        print("Le dossier contenant le screen n'a pu être créé")
        return False

def createSubDirs(path_screen_day, directory):
    sub_dirs = directory.split("/")
    sub_dirs.pop()
    dir_to_create = path_screen_day
    for dir in sub_dirs:
        dir_to_create = os.path.join(dir_to_create, dir)
        try:
            os.mkdir(dir_to_create)
        except FileExistsError:
            pass
        except Exception:
            print("sub_dirs : Impossible de créer le fichier : ", dir_to_create)
            return False
    return True
    
def copy(path_from, path_to):
    try:
        shutil.copytree(path_from, path_to)
    except OSError as e:
        # If the error was caused because the source wasn't a directory or was still open
        if e.errno == errno.ENOTDIR:
            shutil.copy(path_from, path_to)
        else:
            print('Directory not copied. Error: %s' % e)
            
            
    
if hardDiskDetected(hard_disk_path) == False:
    raise Exception
if dirToScreenDetected(DESKTOP_PATH, list_dir_to_screen) == False:
    raise Exception
if screenOfTheDay(DESKTOP_PATH, list_dir_to_screen, hard_disk_path) == False:
    raise Exception


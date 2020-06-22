import os
import eyed3

class Change_Album_Name():
    def __init__(self):
        print("Hi! To modify your .mp3 files, i need to know the location of the \n",
            "PATH of the directory that contains the .mp3, and the \n",
            "NAME of the album that you want to give \n")
        #self.NAME_ALBUM = input("Name album (none=realtive) = ")

    def main(self):
        self.ask_path_directory()
        os.chdir(self.PATH_DIRECTORY)
        self.ask_album_name()
        list_mp3 = self.get_list_mp3()
        for name_mp3 in list_mp3:
            self.modify_album_tag(name_mp3)
        print("The operation is a success!")
    
    def modify_album_tag(self, name_mp3):
        print(name_mp3)
        audiofile = eyed3.load(name_mp3)
        audiofile.tag.album = self.NAME_ALBUM
        audiofile.tag.save()

    def get_list_mp3(self):
        list_files = os.listdir(self.PATH_DIRECTORY)
        list_mp3 = []
        for file_name in list_files:
            if ".mp3" in file_name:
                list_mp3.append(file_name)
        return list_mp3

    def ask_path_directory(self):
        bool_satisfied = False
        while bool_satisfied != True:
            path_dir = str(input("Directory path (none=realtive) = "))
            if path_dir == "":
                path_dir = "./"
            bool_satisfied = self.check_path_directory(path_dir)
        self.PATH_DIRECTORY = path_dir
        
    def check_path_directory(self, path_to_check):
        if os.path.isdir(path_to_check) == True:
            list_files = os.listdir(path_to_check) #Checking that one .mp3 is present in the directory
            for file_name in list_files:
                if ".mp3" in file_name:
                    return True
            else:
                print("The directory given does not contains .mp3 file")
                for file_name in list_files:
                    print(file_name)
        return False
    
    def ask_album_name(self):
        bool_satisfied = False
        while bool_satisfied != True:
            name_album = str(input("Name ablum = "))
            if name_album != "":
                bool_satisfied = True
        self.NAME_ALBUM = name_album
            
        
lole = Change_Album_Name()
lole.main()


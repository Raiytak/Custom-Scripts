# -*- coding: utf-8 -*-

"""
Ce script permet de montrer les anniversaires proches (futurs et passés)
des personnes enregistrées dans les JSONs du dossier Informations privées.

"""


import json
import os
import datetime
import unicodedata

INFO_PATH = r"C:\Users\User1\Desktop\Le Dossier\Informations privées"
LIST_JSON = os.listdir(INFO_PATH)
TODAY = datetime.datetime.now()

birthdays = {}

def strip_accents(text):
    text = str(text)
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


#list all the birthdays
for file in LIST_JSON:
    PATH_TO_OPEN = os.path.join(INFO_PATH,file)
    
    with open(PATH_TO_OPEN, "r", encoding='utf-8') as json_file:
        data = json.load(json_file)
        
        for key in data.keys():
            entity = data[key]
            information = list(entity.keys())
            if ("anniversaire" in information) and (entity["anniversaire"] is not None):
                try:
                    person = entity
                    name = person["prenom"]
                    lastname = person["nom"]
                    birthday = person["anniversaire"]
                    
                    id = strip_accents(name+" "+lastname)
                    if id == " ":
                        pass
                    else:
                        birthdays[id] = birthday
                        
                except (TypeError, KeyError):
                    pass


def convMonth(month):
    CONVERT_MONTH = {"janvier":1,
                "fevrier":2,
                "mars":3,
                "avril":4,
                "mai":5,
                "juin":6,
                "juillet":7,
                "aout":8,
                "septembre":9,
                "octobre":10,
                "novembre":11,
                "decembre":12,
                }
    return CONVERT_MONTH[month]

def convertDateIntoDatetime(birthday):
    day = int(birthday["jour"])
    
    mois_fr = birthday["mois"]
    month_no_acc = strip_accents(mois_fr)
    month = convMonth(month_no_acc)
    
    year = datetime.datetime.now().year
    date = datetime.datetime(year, month, day)
    
    birthday["datetime"] = date


#Convert birthday into datetime
for person, birthday in birthdays.items():
    convertDateIntoDatetime(birthday)

dict_birthdays_datetime = {}
list_birthdays_datetime = []
for person, birthday in birthdays.items():
    dict_birthdays_datetime[person] = birthday["datetime"]
    list_birthdays_datetime.append(birthday["datetime"])
    
list_birthdays_datetime.sort()


#Find the coming and passed birthdays
birthdays_incoming = [birthday for birthday in list_birthdays_datetime if birthday>TODAY]
birthdays_passed = [birthday for birthday in list_birthdays_datetime if birthday<TODAY]

BD_INC = birthdays_incoming[:3]
BD_P = birthdays_passed[-3:]


#Find the persons that have coming birthdays
BD_INC_PP = {name:dict_birthdays_datetime[name]
             for name in dict_birthdays_datetime
             if dict_birthdays_datetime[name]
             in BD_INC}



#Find the persons that have those birthdays
BD_P_PP = {name:dict_birthdays_datetime[name]
             for name in dict_birthdays_datetime
             if dict_birthdays_datetime[name]
             in BD_P}


#Print this information
def showBirthdays(BD_PP):
    BD_PP = {k: v for k, v in sorted(BD_PP.items(), key=lambda item: item[1])}
    for name in BD_PP.keys():
        print(name)
        print(BD_PP[name].day, "/", BD_PP[name].month)
    print("\n")

print("---- Birthdays passed : ----")
showBirthdays(BD_P_PP)

print("---- Birthdays incoming : ----")
showBirthdays(BD_INC_PP)
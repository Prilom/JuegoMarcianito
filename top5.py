#-------------------------------------------------------------------------------
# Name:        módulo1
# Purpose:
#
# Author:      prilo
#
# Created:     24/03/2022
# Copyright:   (c) prilo 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import re

class ScoreStore:
    """Guarda en un archivo los mejores 5 resultados obtenidos"""

    def __init__(self):
        self.filename="top_5.txt"

        self.lines=""
        #self.read_file()
        #self.check_value()

    def check_value(self, value):
        save_values_int=[]
        character="\n"
        print(self.lines)
        print(type(self.lines))
        values = [float(values) for values in re.findall(r'-?\d+\.?\d*', self.lines)]
        print(values)
        print(type(values))
        for value in values:
            save_values_int.append(int(value))
        save_values_int.append(self.value)
        print(save_values_int)
        save_values_int.sort(reverse=True)
        print(type(save_values_int))
        new_top5=f"{str(save_values_int[0])}\n{str(save_values_int[1])}\n{str(save_values_int[2])}\n{str(save_values_int[3])}\n{str(save_values_int[4])}"
        print(new_top5)
        self.top_5_score_anadir(new_top5)



    def top_5_score_anadir(self,cadena):
        with open(self.filename,"r+") as file_object:
            for i in cadena:
                file_object.write(str(i))

    def read_file(self):
        with open(self.filename) as file_object:
            self.lines=file_object.read()









"""lista="1000\n10000\n850\n365\n270\n"

prueba= ScoreStore(10001)
#print(prueba.read_file)
#prueba.top_5_score_anadir(lista)
prueba.read_file"""


from django.shortcuts import render
from django.http import HttpResponse
import json


def index(request):
    return render(request, "index.html")


def home(request):
    return render(request, "home.html")


def flujograma(request, ci):
    # se obtiene el flujograma de las materias del estudiante
    file = open('./static/utils/flujograma_carreras.json', )
    flujograma = json.load(file)



    flujogramaDic = [
        {'Matematica General': [1, 'BTTTTT1'], 'Matemática Básica': [1, 'BTTTTT2'], 'Matemáticas I': [1, 'BTTTTT3'],
         'Matemáticas II': [0, 'BTTTTT4'], 'Matemáticas III': [0, 'BTTTTT5'], 'Matemáticas IV': [0, 'BTTTTT6'],
         'Ecuaciones Diferenciales': [0, 'BTTTTT7'], 'Matemáticas V': [0, 'BTTTTT8'],
         'Iniciativa Emprendedora': [0, 'BTTTTT9'], 'Gestion Cadena de Suministros I': [0, 'BTTTTT10'],
         'Gerencia Proyectos TIC': [0, 'BTTTTT11'], 'Proyecto de Ingeniería': [0, 'BTTTTT12']},
        {'Lenguaje y Universalidad': [1, 'BTTTTT13'], 'Comprension de Venezuela': [1, 'BTTTTT14'],
         'FGE I': [1, 'BTTTTT15'],
         'Matemáticas Discretas': [1, 'BTTTTT16'], 'FGE II': [1, 'BTTTTT17'], 'Algebra Lineal': [1, 'BTTTTT18'],
         'FGE III': [0, 'BTTTTT19'], 'Optimizacion I': [0, 'BTTTTT20'],
         'Optimizacion II': [0, 'BTTTTT21'], 'Modelacion Sist. de Redes': [0, 'BTTTTT22'],
         'Seguridad de la Informacion': [0, 'BTTTTT23'], 'Ingeniería Economica': [0, 'BTTTTT24']},
        {'Matematica General': [1, 'BTTTTT25'], 'Matemática Básica': [1, 'BTTTTT26'], 'Matemáticas I': [1, 'BTTTTT27'],
         'Matemáticas II': [1, 'BTTTTT28'], 'Matemáticas III': [0, 'BTTTTT29'], 'Matemáticas IV': [0, 'BTTTTT30'],
         'Ecuaciones Diferenciales': [0, 'BTTTTT31'],
         'Matemáticas V': [0, 'BTTTTT32'], 'Iniciativa Emprendedora': [0, 'BTTTTT33'],
         'Gestion Cadena de Suministros I': [0, 'BTTTTT34'],
         'Gerencia Proyectos TIC': [0, 'BTTTTT35'], 'Proyecto de Ingeniería': [0, 'BTTTTT36']},
        {'Matematica General': [1, 'BTTTTT37'], 'Matemática Básica': [1, 'BTTTTT38'], 'Matemáticas I': [0, 'BTTTTT39'],
         'Matemáticas II': [0, 'BTTTTT40'], 'Matemáticas III': [0, 'BTTTTT41'], 'Matemáticas IV': [0, 'BTTTTT42'],
         'Ecuaciones Diferenciales': [0, 'BTTTTT43'],
         'Matemáticas V': [0, 'BTTTTT44'], 'Iniciativa Emprendedora': [0, 'BTTTTT45'],
         'Gestion Cadena de Suministros I': [0, 'BTTTTT46'],
         'Gerencia Proyectos TIC': [0, 'BTTTTT47'], 'Proyecto de Ingeniería': [0, 'BTTTTT48']},
        {'Matematica General': [1, 'BTTTTT49'], 'Matemática Básica': [1, 'BTTTTT50'], 'Matemáticas I': [0, 'BTTTTT51'],
         'Matemáticas II': [0, 'BTTTTT52'], 'Matemáticas III': [0, 'BTTTTT53'], 'Matemáticas IV': [0, 'BTTTTT54'],
         'Ecuaciones Diferenciales': [0, 'BTTTTT55'], 'Matemáticas V': [0, 'BTTTTT56'],
         'Iniciativa Emprendedora': [0, 'BTTTTT57'],
         'Gestion Cadena de Suministros I': [0, 'BTTTTT58'],
         'Gerencia Proyectos TIC': [0, 'BTTTTT59'], 'Proyecto de Ingeniería': [0, 'BTTTTT60']}
    ]

    return render(request, "flujograma.html", {'flujograma': flujogramaDic})

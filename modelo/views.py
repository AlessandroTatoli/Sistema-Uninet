from django.shortcuts import render
from django.http import HttpResponse
import json
import numpy as np
from keras.models import load_model


def index(request):
    return render(request, "index.html")


def home(request):
    return render(request, "home.html")


def render_flujograma(request, ci):
    # se obtiene el historico del estudiante
    with open('./static/utils/students_validation.json', "r", encoding='utf8') as fileH:
        all_historicos = json.load(fileH)
        try:
            historico = all_historicos[str(ci)]
        except:
            return render(request, "home.html",
                          {'error': 'No se ha encontrado al estudiante en nuestra base de datos.'})
        fileH.close()

    # se obtiene el flujograma de las materias del estudiante
    with open('./static/utils/flujograma_carreras.json', "r", encoding='utf8') as fileF:
        all_flujogramas = json.load(fileF)
        flujograma = all_flujogramas[historico["Plan de Estudios"]]

        # asignar nombre a las materias del flujograma
        with open('./static/utils/code_to_assign.json', "r", encoding='utf8') as fileN:
            all_nombres = json.load(fileN)
            for materia in flujograma.keys():
                for codigo in all_nombres.keys():
                    if 'FGE0000' in materia:
                        flujograma[materia].append('FGE')
                        break

                    if materia == codigo:
                        flujograma[materia].append(all_nombres[codigo])
                        break
            fileN.close()

        carrera = historico["Plan de Estudios"]

        # materias BPELI (idiomas modernos)
        mat_IM = {
            'BPELI41': [
                0, 'ALEMAN I'
            ],
            'BPELI31': [
                0, 'FRANCES I'
            ],
            'BPELI42': [
                0, 'ALEMAN II'
            ],
            'BPELI32': [
                0, 'FRANCES II'
            ],
            'BPELI43': [
                0, 'ALEMÁN III'
            ],
            'BPELI33': [
                0, 'FRANCES III'
            ],
            'BPELI44': [
                0, 'ALEMAN IV'
            ],
            'BPELI34': [
                0, 'FRANCES IV'
            ],
            'BPELI45': [
                0, 'ALEMAN V'
            ],
            'BPELI35': [
                0, 'FRANCES V'
            ],
            'BPELI55': [
                0, 'ITALIANO V'
            ],
            'BPELI46': [
                0, 'ALEMAN VI'
            ],
            'BPELI36': [
                0, 'FRANCES VI'
            ],
            'BPELI56': [
                0, 'ITALIANO VI'
            ],
            'BPELI47': [
                0, 'ALEMAN VII'
            ],
            'BPELI37': [
                0, 'FRANCES VII'
            ],
            'BPELI48': [
                0, 'ALEMAN VIII'
            ],
            'BPELI38': [
                0, 'FRANCES VIII'
            ],
            'BPELI58': [
                0, 'ITALIANO VIII'
            ],
        }

        # verificar materias que cursó el estudiante
        for materiaF in flujograma.keys():
            for trimestre in historico["Historico"]:
                salto = False
                for n, materiaH in enumerate(trimestre):
                    # validacion para electivas
                    if materiaH != 1903 and 'FGE0000' in materiaF and 'FGE0000' in materiaH:
                        if materiaH.split('_')[1] == 'Good' or materiaH.split('_')[1] == 'Excellent':
                            trimestre[n] = 1903
                            flujograma[materiaF][0] = 1
                            salto = True
                            break

                    # validacion para materias regulares
                    if materiaH != 1903 and materiaF == materiaH.split('_')[0]:
                        if materiaH.split('_')[1] == 'Good' or materiaH.split('_')[1] == 'Excellent':
                            flujograma[materiaF][0] = 1
                            salto = True
                            break

                    # validacion para servicio comunitario
                    if materiaH != 1903 and materiaF == 'BPTDI01' and 'BPTDI01-1' in materiaH:
                        if materiaH.split('_')[1] == 'Good':
                            flujograma[materiaF][0] = 1
                            trimestre[n] = 1903
                            break

                    if materiaH != 1903 and materiaF == 'BPTDI01' and 'BPTDI01-2' in materiaH:
                        if materiaH.split('_')[1] == 'Good':
                            trimestre[n] = 1903
                            flujograma[materiaF][0] = 2
                            salto = True
                            break

                    # validacion idiomas modernos
                    if carrera == 'IDIOMAS MODERNOS' and materiaH != 1903 and 'BPELI' in materiaF and 'BPELI' in materiaH:
                        if materiaH.split('_')[1] == 'Good' or materiaH.split('_')[1] == 'Excellent':
                            trimestre[n] = 1903
                            flujograma[materiaF][0] = 1
                            mat_IM[materiaH.split('_')[0]][0] = 1
                            flujograma[materiaF].append(mat_IM[materiaH.split('_')[0]][1])
                            salto = True
                            break

                if salto:
                    break

    fileF.close()

    if carrera == 'IDIOMAS MODERNOS':
        return render(request, "flujograma.html",
                      {'flujograma': flujograma, 'carrera': carrera, 'ci': ci, 'materias_op': mat_IM})

    return render(request, "flujograma.html", {'flujograma': flujograma, 'carrera': carrera, 'ci': ci})


def predecir(request, ci):
    # validaciones iniciales
    if request.method != 'POST':
        return render(request, "home.html", {'error': 'Ha ocurrido un error inesperado (0).'})

    grupo_materias = []
    hay_materias = False
    for i in range(3):
        grupo_materias.append(request.POST.getlist('materias[' + str(i) + '][]'))
        if len(request.POST.getlist('materias[' + str(i) + '][]')) != 0:
            hay_materias = True

    if not hay_materias:
        return render(request, "home.html", {'error': 'No se han introducido materias a predecir (1).'})

    with open('./static/utils/students_validation.json', "r", encoding='utf8') as fileH:
        all_historicos = json.load(fileH)
        try:
            historico = all_historicos[str(ci)]["Historico"]
        except:
            return render(request, "home.html",
                          {'error': 'No se ha encontrado al estudiante en nuestra base de datos. (2)'})
        fileH.close()

    with open('./static/utils/vocab_to_int.json', "r", encoding='utf8') as fileHI:
        vocab_to_int = json.load(fileHI)
        fileHI.close()

    # crear input historico con sus respectivos indices numericos
    historico_int = np.zeros((1, 24, 21), dtype=int)
    array_1903 = [1903, 1903, 1903, 1903, 1903, 1903, 1903, 1903, 1903, 1903, 1903, 1903, 1903, 1903, 1903, 1903, 1903,
                  1903, 1903, 1903, 1903]

    for i in range(24):
        if i <= (len(historico) - 1):
            for materia in range(0, len(historico[i])):
                if historico[i][materia] != 1903:
                    historico[i][materia] = vocab_to_int[historico[i][materia]]
            historico_int[0][i] = historico[i]
        else:
            historico_int[0][i] = array_1903

    # crear input target con sus respectivos indices numericos
    with open('./static/utils/target_to_int.json', "r", encoding='utf8') as fileII:
        target_to_int = json.load(fileII)
        fileII.close()

    print('Historico del estudiante')
    print(historico_int)

    # cargar el modelo predictivo en el sistema
    model = load_model('./static/utils/model.h5')

    for n, grupo in enumerate(grupo_materias):
        if (len(grupo) != 0):
            target_int = np.zeros((1, 21), dtype=int)
            for i in range(21):
                if i <= (len(grupo) - 1):
                    target_int[0][i] = target_to_int[grupo[i]]
                else:
                    target_int[0][i] = 0
            print('Target del estudiante ' + str(n))
            print(target_int)

            prediccion = model.predict([historico_int, target_int])
            print(prediccion)

    return render(request, "home.html")


def resultados(request):
    return render(request, "resultados.html")

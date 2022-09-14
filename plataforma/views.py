
from email import message
import re
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import FormPaciente, Pacientes, DadosPaciente, Opcao, Refeicao
from django.contrib.messages import constants
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='/auth/login/')
def pacientes(request):
    if request.method == 'GET':
        list_pacient = Pacientes.objects.filter(nutri=request.user)
        form = FormPaciente()
        return render(request, 'pacientes.html', {'form':form, 'list_pacient': list_pacient})

    elif request.method == "POST":
        nome = request.POST.get('nome')
        sexo = request.POST.get('sexo')
        idade = request.POST.get('idade')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')

        if (len(nome.strip()) == 0) or (len(sexo.strip()) == 0) or (len(idade.strip()) == 0) or (len(email.strip()) == 0) or (len(telefone.strip()) == 0):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/pacientes/')

        if len(telefone) < 10:
            messages.add_message(request, constants.ERROR, 'Insira um telefone válido.')
            return redirect('/pacientes/')

        if not idade.isnumeric():
            messages.add_message(request, constants.ERROR, 'Digite uma idade válida.')
            return redirect('/pacientes/')

        
        if not telefone.isnumeric():
            messages.add_message(request, constants.ERROR, 'Digite um telefone válido.')
            return redirect('/pacientes/')

        pacientes = Pacientes.objects.filter(email=email)

        if len(pacientes) > 0:
            messages.add_message(request, constants.ERROR, 'Já existe um paciente com esse E-mail')
            return redirect('/pacientes/')

        else:

            try:
                form = FormPaciente(request.POST, request.FILES)
                form.save()
                messages.add_message(request, constants.SUCCESS, 'Paciente cadastrado com sucesso.')
                return redirect('pacientes')

            except:
                messages.add_message(request, constants.ERROR, 'Erro interno do sistema. Tente novamente mais tarde.')
                return redirect('/pacientes/')


@login_required(login_url='/auth/logar/')
def dados_paciente_listar(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'dados_paciente_listar.html', {'pacientes': pacientes})


@login_required(login_url='/auth/logar/')
def dados_paciente(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    dados = DadosPaciente.objects.filter(paciente_id=paciente.id)

    if paciente.nutri != request.user:
        messages.add_message(request, constants.ERROR, 'Este paciente não pertence a sua lista de pacientes.')
        return redirect('pacientes')

    if request.method == 'GET':

       
        return render(request, 'dados_paciente.html', {'paciente':paciente, 'dados': dados})

    
    if request.method == 'POST':
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        gordura = request.POST.get('gordura')
        musculo = request.POST.get('musculo')
        hdl = request.POST.get('hdl')
        ldl = request.POST.get('ldl')
        colesterol_total = request.POST.get('colesterol_total')
        trigliceridios = request.POST.get('trigliceridios')

        if len(peso.strip()) == 0 or len(altura.strip()) == 0 or len(gordura.strip()) == 0 or \
            len(musculo.strip()) == 0 or len(hdl.strip()) == 0 or len(ldl.strip()) == 0 or \
            len(colesterol_total.strip()) == 0 or len(trigliceridios.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos.')
            return redirect(f'http://127.0.0.1:8000/dados_paciente/{id}')

        if not peso.isnumeric() or not altura.isnumeric() or not gordura.isnumeric() or not musculo.isnumeric()\
            or not hdl.isnumeric() or not ldl.isnumeric() or not colesterol_total.isnumeric() or not trigliceridios.isnumeric():
            messages.add_message(request, constants.ERROR, 'Digite dados válidos.')
            return redirect(f'http://127.0.0.1:8000/dados_paciente/{id}')

        try:
            dados = DadosPaciente(
                peso=peso,
                altura =altura,
                gordura=gordura,
                musculo=musculo,
                hdl=hdl,
                ldl=ldl,
                colesterol_total=colesterol_total,
                trigliceridios=trigliceridios,
                paciente=paciente
            )

            dados.save()
            messages.add_message(request, constants.SUCCESS, 'Os dados foram cadastrados com sucesso.')
            return redirect(f'http://127.0.0.1:8000/dados_paciente/{id}')

        except Exception as e:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema. Tente o cadastro de dados novamente')
            return redirect(f'http://127.0.0.1:8000/dados_paciente/{id}')




@login_required(login_url='/auth/logar/')
@csrf_exempt
def grafico_peso(request, id):
    paciente = Pacientes.objects.get(id=id)
    dados = DadosPaciente.objects.filter(paciente_id=paciente.id).order_by("data")
    
    pesos = [dado.peso for dado in dados]
    labels = list(range(len(pesos)))
    data = {'peso': pesos,
            'labels': labels}
    return JsonResponse(data)


def plano_alimentar_listar(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'plano_alimentar_listar.html', {'pacientes': pacientes})


def plano_alimentar(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    refeicao = Refeicao.objects.filter(paciente_id = paciente.id).order_by('horario')


 
    if paciente.nutri != request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não pertence a sua lista de pacientes.')
        return redirect('plano_alimentar_listar')
    else:
        if request.method == "GET":
            opcoes = Opcao.objects.all()
            return render(request, 'plano_alimentar.html', {'paciente': paciente, 'refeicao': refeicao, 'opcoes': opcoes})


def refeicao(request, id_paciente):
    paciente = get_object_or_404(Pacientes, id=id_paciente)
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/dados_paciente/')

    if request.method == "POST":
        titulo = request.POST.get('titulo')
        horario = request.POST.get('horario')
        carboidratos = request.POST.get('carboidratos')
        proteinas = request.POST.get('proteinas')
        gorduras = request.POST.get('gorduras')

        try:
            r1 = Refeicao(paciente_id=paciente.id,
                        titulo=titulo,
                        horario=horario,
                        carboidratos=carboidratos,
                        proteinas=proteinas,
                        gorduras=gorduras)

            r1.save()
            messages.add_message(request, constants.SUCCESS, 'Refeição cadastrada com sucesso.')
            return redirect(f'/plano_alimentar/{id_paciente}')
        
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect(f'http://127.0.0.1:8000/dados_paciente/{id}')

def opcao(request, id_paciente):
    if request.method == "POST":
        id_refeicao = request.POST.get('refeicao')
        imagem = request.FILES.get('imagem')
        descricao = request.POST.get("descricao")

        o1 = Opcao(refeicao_id=id_refeicao,
                   imagem=imagem,
                   descricao=descricao)

        o1.save()

        messages.add_message(request, constants.SUCCESS, 'Opcao cadastrada')
        return redirect(f'/plano_alimentar/{id_paciente}')


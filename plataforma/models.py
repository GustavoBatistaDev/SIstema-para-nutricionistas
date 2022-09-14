from django.db import models
from django.contrib.auth.models import User
from django import forms
from datetime import datetime


class Pacientes(models.Model):
    choices_sexo = (('F', 'Feminino'),
                    ('M', 'Maculino'))
    nome = models.CharField(max_length=50)
    foto = models.ImageField(upload_to='fotos/%Y/%m')
    sexo = models.CharField(max_length=1, choices=choices_sexo)
    idade = models.IntegerField()
    email = models.EmailField()
    telefone = models.IntegerField()
    nutri = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class FormPaciente(forms.ModelForm):
    class Meta:
        model = Pacientes
        exclude = ()

class DadosPaciente(models.Model):
    data = models.DateTimeField(default=datetime.now)
    peso = models.IntegerField()
    altura = models.IntegerField()
    gordura = models.IntegerField()
    musculo = models.IntegerField()
    hdl = models.FloatField()
    ldl = models.FloatField()
    colesterol_total = models.FloatField()
    trigliceridios = models.FloatField()
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)


    def __str__(self):
        return f'DadosPaciente: obj {self.paciente}'


class Refeicao(models.Model):
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=50)
    horario = models.TimeField()
    carboidratos = models.IntegerField()
    proteinas = models.IntegerField()
    gorduras = models.IntegerField()

    def __str__(self):
        return self.titulo



class Opcao(models.Model):
    refeicao = models.ForeignKey(Refeicao, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to="opcao")
    descricao = models.TextField()

    def __str__(self):
        return self.descricao
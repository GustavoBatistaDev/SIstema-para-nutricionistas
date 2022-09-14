from django.contrib import admin
from .models import Pacientes, DadosPaciente, Refeicao, Opcao


admin.site.register(Refeicao)
admin.site.register(Opcao)


@admin.register(DadosPaciente)
class DadosAdmin(admin.ModelAdmin):
    pass



@admin.register(Pacientes)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')

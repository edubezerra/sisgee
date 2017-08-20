from django.shortcuts import render


def index(request):
    return render(request, 'estagio/registro_termo_estagio.html')


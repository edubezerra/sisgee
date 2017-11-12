from io import TextIOWrapper
import csv
import logging
import datetime

from django.shortcuts import render

from .forms import ImportForm
from .models import Pessoa, Curso, Campus, Aluno


def index(request):
    return render(request, 'estagio/registro_termo_estagio.html')


def create(request):
    if request.method == "POST":
        form = ImportForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'estagio/registro-aluno.html', {'form': form})

        try:
            handle_files(request)
        except:
            return render(request, 'estagio/registro-aluno.html', {'form': form, 'error': True})
        return render(request, 'estagio/registro-aluno.html', {'form': form, 'success': True})
    return render(request, 'estagio/registro-aluno.html', {'form': ImportForm()})


def handle_files(request):
    # Lê o arquivo com os dados dos alunos e gera um dicionário do Python com eles.
    f = TextIOWrapper(request.FILES['file'].file, encoding=request.encoding)
    line_reader = csv.DictReader(f, delimiter=';', restkey='RESTANTE_DA_LINHA')

    mensagemDoLog = "os registros abaixo não foram inseridos no banco de dados pelos motivos listados:\n"

    # Lê cada linha do dicionário contendo os dados dos alunos. O que corresponde aos dados de um
    # aluno em específico.
    for row in line_reader:

        if registroPossuiErro(row):
            # Insere o motivo da não inclusão do registro no banco e o próprio registro, além de pulá-lo.
            mensagemDoLog += registroPossuiErro(row)
            continue

            # Altera a formatação da data de nascimento do aluno em questão. O SQL só aceita no formato ano-mês-dia.
        data_nascimento_aluno = changeDateFormat(row['CPF'], row['DT_NASCIMENTO'])

        # Verifica se já existe no banco os dados pessoais de determinado aluno com o cpf indicado e guarda o id
        # desse aluno. Caso não exista, o id recebe o valor None.
        try:
            objPessoa, pessoaWasCreated = Pessoa.objects.update_or_create(
                cpf=row['CPF'],
                defaults={'nome': row['NOME_ALUNO'],
                          'dt_nasc': data_nascimento_aluno,
                          'tipo_endereco': row['TIPO_LOGRADOURO'],
                          'endereco': row['LOGRADOURO'],
                          'numero': row['NUMERO'],
                          'complemento': row['COMPLEMENTO'],
                          'bairro': row['BAIRRO'],
                          'cep': row['CEP'],
                          'distrito': row['DISTRITO'],
                          'cidade': row['MUNICIPIO'],
                          'estado': row['UF'],
                          'pais': row['PAIS'],
                          'email': row['E_MAIL'],
                          'ddi_residencial': not_changed_to_none(row['DDI_RESIDENCIAL']),
                          'ddd_residencial': not_changed_to_none(row['DDD_RESIDENCIAL']),
                          'fone_residencial': row['FONE_RESIDENCIAL'],
                          'ddi_comercial': not_changed_to_none(row['DDI_COMERCIAL']),
                          'ddd_comercial': not_changed_to_none(row['DDD_COMERCIAL']),
                          'fone_comercial': row['FONE_COMERCIAL'],
                          'ddi_celular': not_changed_to_none(row['DDI_CELULAR']),
                          'ddd_celular': not_changed_to_none(row['DDD_CELULAR']),
                          'fone_celular': row['FONE_CELULAR']},
            )
        except Exception as e:
            print(e)
            continue

        # Verifica se a unidade (ou campus) existe no banco de dados, e cria-a (o objeto) e salva-a se não existir.
        objCampus, campusWasCreated = Campus.objects.get_or_create(
            nome_do_campus=row['UNIDADE'],
        )

        # Verifica se o curso existe no banco de dados, e cria-o se não existir.
        objCurso, cursoWasCreated = Curso.objects.get_or_create(
            cod_curso=row['COD_CURSO'],
            defaults={'nome_curso': row['CURSO'],
                      'id_campus': objCampus},
        )

        try:
            # Verifica se a matrícula (o aluno) já existe no banco de dados através do uso da chave primária, e
            # guarda-o se existir. Caso não exista, configura o objeto para None e não salva no banco de dado
            # essas informações.
            objAluno, alunoWasCreated = Aluno.objects.get_or_create(
                id_aluno=objPessoa,
                id_curso=objCurso,
                defaults={'matricula': row['MATRICULA'],
                          'situacao': row['SITUACAO']},
            )
        except Exception as e3:
            print(e3)
            continue

    # Os registros não inclusos no banco de dados são gravados num arquivo de log, caso exista algum.
    if len(mensagemDoLog) > 82:
        logging.getLogger("bd log").warning(mensagemDoLog)

    # Dando tudo certo, retorna o valor True.
    return True


def registroPossuiErro(linha, mensagem_de_log='', separador='\t'):
    motivo_do_log = "Registro "
    registro_para_log = ""

    if linha['CPF'] == '':
        motivo_do_log += "sem CPF"

    if ('/' in linha['DT_NASCIMENTO']) and (int(linha['DT_NASCIMENTO'][-4:]) <= datetime.datetime.now().year - 90)\
            and len(motivo_do_log) == 9:
        motivo_do_log += "com idade maior que 90 anos"
    elif ('/' in linha['DT_NASCIMENTO']) and (int(linha['DT_NASCIMENTO'][-4:]) <= datetime.datetime.now().year - 90)\
            and len(motivo_do_log) > 9:
        motivo_do_log += ", com idade maior que 90 anos"

    if (not '/' in linha['DT_NASCIMENTO']) and len(motivo_do_log) == 9:
        motivo_do_log += "com dados deslocados para direita"
    elif (not '/' in linha['DT_NASCIMENTO']) and len(motivo_do_log) > 9:
        motivo_do_log += ", com dados deslocados para direita"

    if len(motivo_do_log) > 9:

        for chave, valor in linha.items():
            registro_para_log += "{0} = {1}{2}".format(chave, valor, separador)

        mensagem_de_log = "{:42}\t{}\n".format(motivo_do_log, registro_para_log)

    return mensagem_de_log


def changeDateFormat(cpf, date):
    # Formata a data apenas se ela não for vazia.
    if date != '':

        # Altera o formato da data para ficar igual ao usado pelo banco de dados.
        try:
            date = date.split("/")
            date = date[2] + "-" + date[1] + "-" + date[0]

        # Caso não consiga por não ser um dado válido, apague-o com o valor None e emita uma mensagem de erro.
        except Exception as e:
            date = ''
            print("Erro ao formatar a Data de Nascimento do cpf: " + cpf + "\n\nEsse campo não possui uma data válida!")

    return date


def not_changed_to_none(value):
    if len(value) == 0:
        return None
    return value

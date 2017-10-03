from io import TextIOWrapper
import csv

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
    reader = csv.DictReader(f)

    # Lê cada linha do dicionário contendo os dados dos alunos. O que corresponde aos dados de um
    # aluno em específico.
    for row in reader:

        # Procura por valores vazios na linha atual do dicionário de alunos, e
        # altera esses valores de NULL para o valor do Python Nome.
        for r in row.keys():
            if row[r] == 'NULL':
                row[r] = None

        # Altera a formatação da data de nascimento do aluno em questão.
        data_nascimento_aluno = is_none(row['DT_NASCIMENTO'])
        if data_nascimento_aluno:

            # Altera o formato da data para ficar igual ao usado pelo banco de dados.
            try:
                data_nascimento_aluno = data_nascimento_aluno.split("/")
                data_nascimento_aluno = data_nascimento_aluno[2] + "-" + data_nascimento_aluno[1] + "-" + \
                                        data_nascimento_aluno[0]

            # Caso não consiga por não ser um dado válido, apague-o com o valor None e emita uma mensagem de erro.
            except Exception as e:
                data_nascimento_aluno = None
                print("Erro ao parsear a Data de Nascimento do cpf: " + is_none(row['CPF']))
                print(e)

        # Verifica se já existe no banco os dados pessoais de determinado aluno com o cpf indicado e guarda o id
        # desse aluno. Caso não exista, o id recebe o valor None.
        try:
            objPessoa = Pessoa.objects.get(cpf=is_none(row['CPF']))
            id = objPessoa.pk
        except:
            id = None

        # Cria um objeto (modelo/registro) Pessoa (que conteria os dados pessoais do aluno).
        obj = Pessoa(cpf=is_none(row['CPF']),
                     nome=is_none(row['NOME_ALUNO']),
                     dt_nasc=data_nascimento_aluno,
                     tipo_endereco=is_none(row['TIPO_LOGRADOURO']),
                     endereco=is_none(row['LOGRADOURO']),
                     numero=is_none(row['NUMERO']),
                     complemento=is_none(row['COMPLEMENTO']),
                     bairro=is_none(row['BAIRRO']),
                     cep=is_none(row['CEP']),
                     # distrito=is_none(row['DISTRITO']),
                     cidade=is_none(row['MUNICIPIO']),
                     estado=is_none(row['UF']),
                     pais=is_none(row['PAIS']),
                     email=is_none(row['E_MAIL']),
                     # ddi_residencial=is_none(row['DDI_RESIDENCIAL']),
                     # ddd_residencial=is_none(row['DDD_RESIDENCIAL']),
                     fone_residencial01=is_none(row['FONE_RESIDENCIAL']),
                     fone_residencial02=None,
                     # ddi_comercial=is_none(row['DDI_COMERCIAL']),
                     # ddd_comercial=is_none(row['DDD_COMERCIAL']),
                     fone_comercial01=is_none(row['FONE_COMERCIAL']),
                     fone_comercial02=None,
                     # ddi_celular=is_none(row['DDI_CELULAR']),
                     # ddd_celular=is_none(row['DDD_CELULAR']),
                     fone_celular01=is_none(row['FONE_CELULAR']),
                     fone_celular02=None)

        # Se o valor de id não for None (os dados pessoais do aluno já existem no banco de dados), acrescenta o id no
        # objeto e atualiza-o no banco de dados. Exibe um erro se não conseguir e pula esse registro do
        # arquivo carregado.
        if id:
            obj.id = id
        try:
            obj.save()
        except Exception as err:
            print(err)
            continue

        # Verifica se o curso existe no banco de dados, e cria-o se não existir.
        try:
            objCurso = Curso.objects.get(cod_curso=is_none(row['COD_CURSO']))
        except:
            objCurso = Curso.objects.create(cod_curso=is_none(row['COD_CURSO']),
                                            nome_curso=is_none(row['CURSO']))

        # Verifica se a unidade (ou campus) existe no banco de dados, e cria-a e salva-a se não existir.
        try:
            objCampus = Campus.objects.get(nome_do_campus=is_none(row['UNIDADE']))
        except:
            objCampus = Campus.objects.create(nome_do_campus=is_none(row['UNIDADE']))

            # Salva os dados do campus.
            try:
                objCampus.save()
            except Exception as err:
                print(err)

        # Verifica se a matrícula (o aluno) já existe no banco de dados através do uso da chave primária, e
        # guarda-o se existir. Caso não exista, configura o objeto para None e não salva no banco de dado
        # essas informações.
        try:
            objAluno = Aluno.objects.filter(id_aluno__pk=obj.pk)
        except:
            objAluno = None

        # Existindo algum aluno (ou vários alunos) com determinada matrícula, separa a chave primária de cada curso
        # numa lista, e ??? Se tiver a chave do curso encontrado no registro atual do aluno, pula esse registro.
        if objAluno:
            lis = list()
            for valueobj in objAluno:
                lis.append(valueobj.nome_curso.pk)
            if objCurso.pk in lis:
                continue

        # Cria o objeto aluno e salva-o no banco de dados.
        obj_ps = Aluno(matricula=is_none(row['MATRICULA']), situacao=is_none(row['SITUACAO']), id_curso=objCurso,
                       id_aluno=obj)
        obj_ps.save()
    return True


def is_none(value):
    if len(value) == 0:
        return None
    return value

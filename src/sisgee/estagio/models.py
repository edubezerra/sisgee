from django.db import models

from .validators import validate_cpf


class Pessoa(models.Model):
    cpf = models.CharField(db_column='cpf', unique=True, max_length=14, validators=[validate_cpf])
    nome = models.CharField(db_column='nome', max_length=100)
    dt_nasc = models.DateField(db_column='dataNascimento')
    tipo_endereco = models.CharField(db_column='tipoEndereco', max_length=100, blank=True, null=True)
    endereco = models.CharField(db_column='endereco', max_length=255, blank=True, null=True)
    numero = models.CharField(db_column='numeroEndereco', max_length=10, blank=True, null=True)
    complemento = models.CharField(db_column='complementoEndereco', max_length=150, blank=True, null=True)
    bairro = models.CharField(db_column='bairroEndereco', max_length=150, blank=True, null=True)
    cep = models.CharField(db_column='cepEndereco', max_length=15, blank=True, null=True)
    distrito = models.CharField(db_column='distritoEndereco', max_length=150, blank=True, null=True)
    cidade = models.CharField(db_column='cidadeEndereco', max_length=150, blank=True, null=True)
    estado = models.CharField(db_column='estadoEndereco', max_length=2, blank=True, null=True)
    pais = models.CharField(db_column='paisEndereco', max_length=100, blank=True, null=True)
    email = models.EmailField(db_column='email', max_length=150, blank=True, null=True)
    ddi_residencial = models.IntegerField(db_column='ddiResidencial', blank=True, null=True)
    ddd_residencial = models.IntegerField(db_column='dddResidencial', blank=True, null=True)
    fone_residencial = models.CharField(db_column='telefoneResidencial', max_length=30, blank=True, null=True)
    ddi_comercial = models.IntegerField(db_column='ddiComercial', blank=True, null=True)
    ddd_comercial = models.IntegerField(db_column='dddComercial', blank=True, null=True)
    fone_comercial = models.CharField(db_column='telefoneComercial', max_length=30, blank=True, null=True)
    ddi_celular = models.IntegerField(db_column='ddiCelular', blank=True, null=True)
    ddd_celular = models.IntegerField(db_column='dddCelular', blank=True, null=True)
    fone_celular = models.CharField(db_column='telefoneCelular', max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'Pessoa'
        verbose_name_plural = 'pessoas'
        verbose_name = 'pessoa'
        ordering = ('nome',)

    def __str__(self):
        return self.nome


class Campus(models.Model):
    nome_do_campus = models.CharField(db_column='nomeCampus', max_length=100)

    class Meta:
        db_table = 'Campus'
        verbose_name_plural = 'campus'
        verbose_name = 'campi'
        ordering = ('nome_do_campus',)

    def __str__(self):
        return self.nome_do_campus


class Curso(models.Model):
    cod_curso = models.CharField(db_column='codigoCurso', max_length=50)
    nome_curso = models.CharField(db_column='nomeCurso', max_length=255)
    id_campus = models.ForeignKey(Campus, db_column='idCampus')

    class Meta:
        db_table = 'Curso'
        verbose_name_plural = 'cursos'
        verbose_name = 'curso'
        ordering = ('nome_curso',)

    def __str__(self):
        return self.nome_curso


class Aluno(models.Model):
    matricula = models.CharField(db_column='matricula', max_length=100)
    situacao = models.CharField(db_column='situacao', max_length=25)
    id_curso = models.ForeignKey(Curso, db_column='idCurso')
    id_aluno = models.ForeignKey(Pessoa, db_column='idPessoa')

    class Meta:
        db_table = 'Aluno'

    def __str__(self):
        return self.matricula

from django.core.exceptions import ValidationError
from pycpfcnpj import cpfcnpj


def validate_formato(value):
    formato = str(value)[-3::]
    if formato != "csv":
        raise ValidationError('Formato Inválido!')


def validate_cpf(value):
    if not cpfcnpj.validate(value):
        raise ValidationError('CPF inválido')
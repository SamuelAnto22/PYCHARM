
{
    'name': "Gestión Instituto",
    'summary': "Gestión de ciclos formativos, módulos, alumnos y profesores",
    'description': "Módulo para la gestión académica de un instituto.",
    'author': "Tu Nombre",
    'category': 'Education',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/instituto_views.xml',
    ],
    'installable': True,
    'application': True,
}
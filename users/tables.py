from django_tables2 import tables, TemplateColumn, Column
from main.models import *

action1 = """
    <a href="{% url 'qrCode' record.pk%}" class="btn btn-success" role="button">QrCode</a>
    <a href="{% url 'userEdit' record.pk%}" class="btn btn-primary" role="button">Edit</a>
    <a href="{% url 'userActivate' record.pk%}" class="btn btn-primary" role="button">Activate</a>
    <a href="{% url 'userDeactivate' record.pk%}" class="btn btn-primary" role="button">Deactivate</a>
    <a href="{% url 'userDelete' record.pk%}" class="btn btn-danger" role="button">Delete</a>
          """

class UsersTable(tables.Table):
    actions = TemplateColumn(action1, verbose_name='')
    office = Column(verbose_name='Affectation')
    job = Column(verbose_name='Job Title')
    class Meta:
        model = User
        fields = ['id','firstname','lastname','job','office','shift','is_active','actions']
        exclude = ['facedata','role']



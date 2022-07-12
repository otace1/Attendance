from django_tables2 import tables, TemplateColumn, Column
from main.models import *

action1 = """
    <button type="button" class="btn btn-success">Edit</button>
    <button type="button" class="btn btn-danger">Delete</button>
          """

class UsersTable(tables.Table):
    actions = TemplateColumn(action1, verbose_name='')
    office = Column(verbose_name='Affectation')
    job = Column(verbose_name='Job Title')
    class Meta:
        model = User
        fields = ['id','firstname','lastname','job','office','shift','actions']
        exclude = ['facedata','role']



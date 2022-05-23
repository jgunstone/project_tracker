# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     formats: py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

from pydantic import BaseModel, Field
from datetime import datetime, date
import typing
import pathlib
import stringcase
import sys

sys.path.append(r'src')
sys.path.append(r'../ipyautoui/src')
sys.path.append(r'../ipyrun/src')

from ipyautoui.custom.fileupload import File

ALLOWED_PROJECT_STATUS = [
    "active", 
    "for-review", 
    "to-be-programmed", 
    "completed-maintained", 
    "completed-not-maintained", 
    "permanently-on-hold", 
    "abandoned"
]

class BaseModel(BaseModel):
    def file(self, path: pathlib.Path, **json_kwargs):
        if 'indent' not in json_kwargs.keys():
            json_kwargs.update({'indent':4})
        path.write_text(self.json(**json_kwargs), encoding='utf-8')
        
    def file_yaml(self, path: pathlib.Path, **json_kwargs):
        if 'indent' not in json_kwargs.keys():
            json_kwargs.update({'indent':4})
        path.write_text(self.json(**json_kwargs), encoding='utf-8')
        
        with open(path, 'w') as file:
            documents = yaml.dump(dict_file, file)

        
    class Config:
        allow_population_by_field_name = True
        alias_generator = stringcase.titlecase

# +
class Brief(BaseModel):
    client_originator: str = Field(None, alias='Client / Originator')
    work_type: str = None
    related_projects: str = None
    brief: str = Field(None, format='markdown')
    background: str = Field(None, format='markdown')
    value_to_practice: str = Field(None, format='markdown')
    description_of_output: str = Field(None, format='markdown')
    #links: typing.List[Link]

class BudgetItem(BaseModel):
    pass

class LinkedFiles(BaseModel):
    name: str
    description: str

class Resource(BaseModel):
    #development_budget: typing.List[BudgetItem]
    development_notes: str = None
    #maintainence_budget: typing.List[BudgetItem]
    maintainence_notes: str = None

class Programme(BaseModel):
    start: date=None #date = 
    draft: date = None
    beta_release: date = None
    sign_off: typing.Optional[date] = None
    distribution: date = None

class Management(BaseModel):
    consultees: str = None #typing.List[str]
    precedents: str = Field(None, description="Precedents on existing projects") 
    issues_challenges: str = Field(None, description="Key issues / challenges / questions / limitations")
    dissemination: str = Field(None, description="Dissemination & Training")

class Outputs(BaseModel):
    description: str = None
    #links: typing.List[LinkedFiles]

class Project(BaseModel):
    # icon: pathlib.Path = None
    # image: pathlib.Path = None
    project_name: str =None
    project_summary: str = None
    current_status: str = Field(None, description="Current Status of Project", enum=ALLOWED_PROJECT_STATUS)
    linked_files: typing.Dict[str, File] = Field(None, autoui="ipyautoui.custom.fileupload.FileUploadToDir", description='linked files')
    # brief: Brief = Brief() 
    # resource: Resource = Resource()
    # programme: Programme = Programme()
    # management: Management = Management()
    brief: Brief = None
    resource: Resource = None
    programme: Programme = None
    management: Management = None
    #links: typing.List[Link]


# -

if __name__ == "__main__":
    from ipyautoui import AutoUi
    display(AutoUi(Project))



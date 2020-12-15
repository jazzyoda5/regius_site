from django.shortcuts import render
from docxtpl import DocxTemplate
from django.http import HttpResponse, HttpResponseRedirect
from projects.models import (Project,
                             Client,
                             ProjectAdress,
                             ProjectContactInfo,
                             Contractor,
                             ProjectAnex)
from .models import DocumentTemplate, ProjectDocument, ProjectContract, ProjectAnexDoc
import os
from regius_site_1.settings import BASE_DIR
from django.core.files import File
from datetime import date
import datetime


def create_project_doc(request, project_id):

    # Get template
    tpl_object = DocumentTemplate.objects.get(title="projektni-list-template")
    tpl_doc = getattr(tpl_object, 'document')

    # Get context to fill in the template
    project = Project.objects.get(id=project_id)
    context = {}
    for field in project._meta.get_fields():
        try:
            field_name = field.name
            field_value = getattr(project, field.attname)
            context[str(field_name)] = str(field_value)

        except AttributeError:
            pass

    client = Client.objects.get(project=project_id)
    context["client"] = str(client)
    for field in client._meta.get_fields():
        try:
            field_name = "client_" + str(field.name)
            field_value = getattr(client, field.attname)
            context[field_name] = str(field_value)

        except AttributeError:
            print('error')
            pass

    project_contact_info = ProjectContactInfo.objects.get(project=project_id)
    for field in project_contact_info._meta.get_fields():
        try:
            field_name = str(field.name)
            field_value = getattr(project_contact_info, field.attname)
            context[field_name] = str(field_value)

        except AttributeError:
            print('error')
            pass

    project_address = ProjectAdress.objects.get(project=project_id)
    for field in project_address._meta.get_fields():
        try:
            field_name = 'pa_' + str(field.name)
            field_value = getattr(project_address, field.attname)
            context[field_name] = str(field_value)

        except AttributeError:
            print('error')
            pass

    # Change date format
    project_start = context['project_start_date']
    temp = datetime.datetime.strptime(project_start, '%Y-%m-%d')
    context['project_start_date'] = temp.strftime("%d.%m.%Y")
    project_end = context['project_end_date']
    temp = datetime.datetime.strptime(project_end, '%Y-%m-%d')
    context['project_end_date'] = temp.strftime("%d.%m.%Y")
    
    # open the template and create doc, then save to autofill_templates

    doc = DocxTemplate(tpl_doc)
    doc.render(context)
    doc.save(os.path.join(BASE_DIR, 'media_cdn/media/', 'temp_doc.docx'))

    # Open the doc that has to be saved
    f = open(os.path.join(BASE_DIR, 'media_cdn/media/', 'temp_doc.docx'), 'rb')

    # Save to db
    project_document = project.projectdocument_set.create(
        title=str(project), project=project)
    file_field = project_document.project_doc
    file_field.save(str(project) + '.docx', f, save=True)

    os.remove(os.path.join(BASE_DIR, 'media_cdn/media/', 'temp_doc.docx'))

    return HttpResponseRedirect('/projekti/' + str(project_id) + '/dokumenti/')


def create_contract_doc(request, project_id):

    # Get template
    tpl_object = DocumentTemplate.objects.get(title="contract-template")
    tpl_doc = getattr(tpl_object, 'document')

    # Get context to fill in the template
    project = Project.objects.get(id=project_id)
    context = {}
    for field in project._meta.get_fields():
        try:
            field_name = field.name
            field_value = getattr(project, field.attname)
            context[str(field_name)] = str(field_value)

        except AttributeError:
            pass

    client = Client.objects.get(project=project_id)
    context["client"] = str(client)
    for field in client._meta.get_fields():
        try:
            field_name = "client_" + str(field.name)
            field_value = getattr(client, field.attname)
            context[field_name] = str(field_value)

        except AttributeError:
            print('error')
            pass

    project_contact_info = ProjectContactInfo.objects.get(project=project_id)
    for field in project_contact_info._meta.get_fields():
        try:
            field_name = str(field.name)
            field_value = getattr(project_contact_info, field.attname)
            context[field_name] = str(field_value)

        except AttributeError:
            print('error')
            pass

    project_address = ProjectAdress.objects.get(project=project_id)
    for field in project_address._meta.get_fields():
        try:
            field_name = 'pa_' + str(field.name)
            field_value = getattr(project_address, field.attname)
            context[field_name] = str(field_value)

        except AttributeError:
            print('error')
            pass
    
    # Izvajalec
    contractor = Contractor.objects.get(name=project.contractor)
    context['contractor'] = contractor
    contractor_tax_num = contractor.slo_tax_num
    context['contractor_tax_num'] = contractor_tax_num

    # Datum 
    project_start = context['project_start_date']
    temp = datetime.datetime.strptime(project_start, '%Y-%m-%d')
    context['project_start_date'] = temp.strftime("%d.%m.%Y")
    project_end = context['project_end_date']
    temp = datetime.datetime.strptime(project_end, '%Y-%m-%d')
    context['project_end_date'] = temp.strftime("%d.%m.%Y")

    todays_date = date.today().strftime("%d.%m.%Y")
    context['date'] = todays_date

    # open the template and create doc, then save to autofill_templates

    doc = DocxTemplate(tpl_doc)
    doc.render(context)
    doc.save(os.path.join(BASE_DIR, 'media_cdn/media/', 'temp_doc.docx'))

    # Open the doc that has to be saved
    f = open(os.path.join(BASE_DIR, 'media_cdn/media/', 'temp_doc.docx'), 'rb')

    # Save to db
    contract = project.projectcontract_set.create(
        title=str(project), project=project)
    file_field = contract.contract
    file_field.save(str(project) + '.docx', f, save=True)

    os.remove(os.path.join(BASE_DIR, 'media_cdn/media/', 'temp_doc.docx'))

    return HttpResponseRedirect('/projekti/' + str(project_id) + '/dokumenti/')


def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(
                fh.read(), content_type="application/adminupload")
            response['Content-Disposition'] = 'inline;filename=' + \
                os.path.basename(file_path)
            return response
    return HttpResponse("Nope")


def delete_project_doc(request, document_id):
    document = ProjectDocument.objects.get(id=document_id)
    project = document.project
    document.delete()
    return HttpResponseRedirect('/projekti/' + str(project.id) + '/dokumenti/')


def delete_contract_doc(request, document_id):
    document = ProjectContract.objects.get(id=document_id)
    project = document.project
    document.delete()
    return HttpResponseRedirect('/projekti/' + str(project.id) + '/dokumenti/')


def create_anex(request, project_id, anex_id):

    # Get template
    tpl_object = DocumentTemplate.objects.get(title="anex-template")
    tpl_doc = getattr(tpl_object, 'document')

    # Get context to fill in the template
    project = Project.objects.get(id=project_id)
    context = {}
    for field in project._meta.get_fields():
        try:
            field_name = field.name
            field_value = getattr(project, field.attname)
            context[str(field_name)] = str(field_value)

        except AttributeError:
            pass

    client = Client.objects.get(project=project_id)
    context["client"] = str(client)
    for field in client._meta.get_fields():
        try:
            field_name = "client_" + str(field.name)
            field_value = getattr(client, field.attname)
            context[field_name] = str(field_value)

        except AttributeError:
            pass
    try:
        project_address = ProjectAdress.objects.get(project=project_id)
    except ProjectAdress.DoesNotExist:
        return HttpResponseRedirect('/projekti/' + str(2) + '/dodajnaslov/')

    for field in project_address._meta.get_fields():
        try:
            field_name = 'pa_' + str(field.name)
            field_value = getattr(project_address, field.attname)
            context[field_name] = str(field_value)

        except AttributeError:
            pass

    anex_data = ProjectAnex.objects.get(project=project, id=anex_id)
    for field in anex_data._meta.get_fields():
        try:
            field_name = 'anex_' + str(field.name)
            field_value = getattr(anex_data, field.attname)
            context[field_name] = str(field_value)

        except AttributeError:
            pass
    
    # Change date formats
    anex_start = context['anex_start']
    temp = datetime.datetime.strptime(anex_start, '%Y-%m-%d')
    context['anex_start'] = temp.strftime("%d.%m.%Y")
    anex_end = context['anex_end']
    temp = datetime.datetime.strptime(anex_end, '%Y-%m-%d')
    context['anex_end'] = temp.strftime("%d.%m.%Y")
    project_start = context['project_start_date']
    temp = datetime.datetime.strptime(project_start, '%Y-%m-%d')
    context['project_start_date'] = temp.strftime("%d.%m.%Y")
    project_end = context['project_end_date']
    temp = datetime.datetime.strptime(project_end, '%Y-%m-%d')
    context['project_end_date'] = temp.strftime("%d.%m.%Y")


    # Izvajalec
    context['contractor'] = project.contractor
    contractor = Contractor.objects.get(name=project.contractor)
    context['contractor_tax_num'] = contractor.slo_tax_num

    # Datum 
    todays_date = date.today().strftime("%d.%m.%Y")
    context['date'] = todays_date

    for i in context:
        print('key: {}, val: {}'.format(i, context[i]))


    # open the template and create doc, then save to autofill_templates

    doc = DocxTemplate(tpl_doc)
    doc.render(context)
    doc.save(os.path.join(BASE_DIR, 'media_cdn/media/', 'temp_doc.docx'))

    # Open the doc that has to be saved
    f = open(os.path.join(BASE_DIR, 'media_cdn/media/', 'temp_doc.docx'), 'rb')

    # Save to db
    project_anex = project.projectanexdoc_set.create(
        title=str(project), anex_data=anex_data, project=project)
    file_field = project_anex.anex_doc
    file_field.save('aneks_st_' + str(anex_data.anex_num) + '_' + str(project) + '.docx', f, save=True)

    os.remove(os.path.join(BASE_DIR, 'media_cdn/media/', 'temp_doc.docx'))

    return HttpResponseRedirect('/projekti/' + str(project_id) + '/dokumenti/')


def delete_anex_doc(request, anex_doc_id):
    anex_doc = ProjectAnexDoc.objects.get(id=anex_doc_id)
    project = anex_doc.project
    anex_doc.delete()
    return HttpResponseRedirect('/projekti/' + str(project.id) + '/dokumenti/')

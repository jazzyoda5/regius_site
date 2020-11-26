from django.shortcuts import render
from docxtpl import DocxTemplate
from django.http import HttpResponse, HttpResponseRedirect
from projects.models import Project, Client, ProjectAdress, ProjectContactInfo
from .models import DocumentTemplate, ProjectDocument
import os
from regius_site_1.settings import BASE_DIR
from django.core.files import File


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


    # open the template and create doc, then save to autofill_templates

    doc = DocxTemplate(tpl_doc)
    doc.render(context)
    doc.save(os.path.join(BASE_DIR, 'media_cdn/media/', 'temp_doc.docx'))

    # Open the doc that has to be saved
    f = open(os.path.join(BASE_DIR, 'media_cdn/media/', 'temp_doc.docx'), 'rb')

    # Save to db
    project_document = project.projectdocument_set.create(title=str(project), project=project)
    file_field = project_document.project_doc
    file_field.save(str(project)+ '.docx', f, save=True)

    os.remove(os.path.join(BASE_DIR, 'media_cdn/media/', 'temp_doc.docx'))

    return HttpResponseRedirect('/projekti/' + str(project_id) + '/')


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

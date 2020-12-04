from django.db import models
from projects.models import Contractor, Project
from django.utils.translation import ugettext as _

class Worker(models.Model):
    first_name = models.CharField(_("Ime"), max_length=30)
    last_name = models.CharField(_("Priimek"), max_length=40)
    company_choices = [('Regius', 'Regius'), ('Tantus', 'Tantus'), ('Dapira 1', 'Dapira 1')]
    company = models.CharField(_("Podjetje"), max_length=50, choices=company_choices)
    employed_choices = [('Da', 'Da'), ('Ne', 'Ne')]
    employed = models.CharField(_("Zaposlen"), max_length=5, choices=employed_choices)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class WorkerInfo(models.Model):
    worker = models.OneToOneField(Worker, verbose_name=_("Delavec"), null=True, on_delete=models.CASCADE)
    phone_num = models.CharField(_("Telefon"), null=True, blank=True, max_length=50)
    email = models.EmailField(_("Email"), null=True, blank=True, max_length=254)
    citizenship = models.CharField(_("Državljanstvo"), blank=True, max_length=50)
    living_address = models.CharField(_("Stalno prebivališče"), null=True, blank=True, max_length=100)
    temporary_address = models.CharField(_("Začasno prebivališče"), null=True, max_length=100, blank=True)
    emso = models.CharField(_("EMŠO"), max_length=30, blank=True, null=True)
    tax_num = models.CharField(_("Davčna št."), null=True, blank=True, max_length=50)
    insurance_num = models.CharField(_("Številka zavarovanja"), null=True, blank=True, max_length=50)

    def __str__(self):
        return str(self.worker)

    @classmethod
    def create(cls, worker):
        workerinfo = cls(worker=worker)
        return workerinfo


class AssignedToProject(models.Model):
    worker = models.ForeignKey(Worker, verbose_name=_("Delavec"), on_delete=models.CASCADE)
    project = models.ForeignKey(Project, verbose_name=_("Projekt"), on_delete=models.CASCADE)
    start_date = models.DateField(_("Začetek"), auto_now=False, auto_now_add=False)
    end_date = models.DateField(_("Konec"), auto_now=False, auto_now_add=False)

    def __str__(self):
        return str(self.worker) + " - " + str(self.project)

class WorkerAvailability(models.Model):
    worker = models.OneToOneField(Worker, verbose_name=_("Delavec"), on_delete=models.CASCADE)
    availability_str = models.CharField(_("Zasedenost"), max_length=365)

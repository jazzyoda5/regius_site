from django.db import models
from django.utils.translation import ugettext as _


class Client(models.Model):
    # Ime
    name = models.CharField(_("Ime"), max_length=80)
    # Ulica
    street = models.CharField(_("Ulica"), max_length=80)
    # Mesto
    city = models.CharField(_("Mesto"), max_length=50)
    # Poštna št.
    zip_code = models.CharField(_("Poštna št."), max_length=30)
    # Država
    country = models.CharField(_("Država"), max_length=60)
    # Davčna št.
    tax_num = models.CharField(_("Davčna št."), max_length=50)

    def __str__(self):
        return self.name

class Project(models.Model):
    # Stranka (že vnesena)
    client = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)
    # Status
    status_choices = [('v teku', 'V teku'), ('končano', 'Končano'), ('storno', 'Storno'), ('na čakanju', 'Na čakanju')]
    status = models.CharField(_("status"), max_length=25, choices=status_choices)
    # Ime projekta
    project_name = models.CharField(_("Ime projekta"), max_length=70)
    # Izvajalec
    contractor_choices = [('Regius', 'Regius'), ('Tantus', 'Tantus')]
    contractor = models.CharField(_("izvajalec"), max_length=30, choices=contractor_choices)
    # Aug
    aug = models.BooleanField(_("Aüg"))
    # Številka pogodbe
    contract_num = models.CharField(_("številka pogodbe"), max_length=60)
    # Aneks
    annex = models.BooleanField(_("aneks"))
    # Obdobje
    project_start_date = models.DateField(_("Od"), auto_now=False, auto_now_add=False)
    project_end_date = models.DateField(_("Do"), auto_now=False, auto_now_add=False)
    # Pogodbena vrednost
    contract_value = models.DecimalField(_("pogodbena vrendost"), max_digits=10, decimal_places=2)
    # Urna postavka
    hourly_rate = models.DecimalField(_("urna postavka"), max_digits=5, decimal_places=2)
    # LW
    lw = models.BooleanField(_("LW"))

    def __str__(self):
        return self.project_name


class ProjectAdress(models.Model):
    project = models.OneToOneField(Project, null=True, on_delete=models.CASCADE)
    # Ulica
    street = models.CharField(_("ulica"), null=True, max_length=80)
    # Mesto
    city = models.CharField(_("mesto"), null=True, max_length=50)
    # Poštna št.
    zip_code = models.CharField(_("poštna št."), null=True, max_length=30)
    # Država
    country = models.CharField(_("država"), null=True, max_length=60)

    def __str__(self):
        return str(self.project)


class ProjectContactInfo(models.Model):
    project = models.OneToOneField(Project, null=True, on_delete=models.CASCADE)
    resp_on_site_name = models.CharField(_("Vodja gradbišča s strani izvajalca"), null=True, max_length=50)
    resp_on_site_phone_num = models.CharField(_("Telefon - vodja gradbišča"), null=True, max_length=50)
    resp_on_site_email = models.EmailField(_("Email - vodja gradbišča"), null=True, max_length=254)
    resp_client_name = models.CharField(_("Odgovorna oseba s strani naročnika"), null=True, max_length=80)
    resp_client_phone_num = models.CharField(_("Telefon - naročnik"), null=True, max_length=50)
    resp_client_email = models.EmailField(_("Email - naročnik"), null=True, max_length=254)
    resp_contractor_name = models.CharField(_("Odgovorna oseba s strani izvajalca"), null=True, max_length=50)
    resp_contractor_phone_num = models.CharField(_("Telefon - izvajalec"), null=True, max_length=50)
    resp_contractor_email = models.EmailField(_("Email - izvajalec"), null=True, max_length=254)

    def __str__(self):
        return self.project




    

    








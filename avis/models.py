from datetime import date

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Sezione(models.Model):
    utente = models.ForeignKey(User, on_delete=models.RESTRICT)
    descrizione = models.CharField(max_length=100)
    indirizzo = models.CharField(max_length=255)
    cap = models.CharField(max_length=5)
    comune = models.CharField(max_length=100)
    provincia = models.CharField(max_length=2)
    telefono = models.CharField(max_length=20, blank=True)
    fax = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=100)
    presidente = models.CharField(max_length=100)
    segretario = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Sezioni'

    def __str__(self):
        return self.descrizione


class Sesso(models.Model):
    codice = models.CharField(max_length=1, unique=True)
    descrizione = models.CharField(max_length=20)
    gg_da_sangue_a_sangue = models.IntegerField()
    gg_da_sangue_a_plasma = models.IntegerField()
    gg_da_sangue_a_piastrine = models.IntegerField()
    gg_da_plasma_a_sangue = models.IntegerField()
    gg_da_plasma_a_plasma = models.IntegerField()
    gg_da_plasma_a_piastrine = models.IntegerField()
    gg_da_piastrine_a_sangue = models.IntegerField()
    gg_da_piastrine_a_plasma = models.IntegerField()
    gg_da_piastrine_a_piastrine = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Sessi'

    def __str__(self):
        return self.descrizione


class StatoDonatore(models.Model):
    sezione = models.ForeignKey(
        Sezione, blank=True, null=True, on_delete=models.CASCADE
    )
    codice = models.CharField(max_length=20)
    descrizione = models.CharField(max_length=100, blank=True)
    is_attivo = models.BooleanField(default=True, verbose_name='Attivo')

    class Meta:
        verbose_name = 'Stato donatore'
        verbose_name_plural = 'Stati donatore'
        unique_together = (
            'sezione',
            'codice',
        )

    def __str__(self):
        return self.descrizione


class Donatore(models.Model):
    sezione = models.ForeignKey(
        Sezione, related_name='donatori', on_delete=models.RESTRICT
    )
    num_tessera = models.CharField(max_length=255)
    cognome = models.CharField(max_length=255)
    nome = models.CharField(max_length=255)
    sesso = models.ForeignKey(Sesso, on_delete=models.RESTRICT)
    stato_donatore = models.ForeignKey(
        StatoDonatore, on_delete=models.RESTRICT
    )
    num_tessera_cartacea = models.CharField(max_length=255, blank=True)
    data_rilascio_tessera = models.DateField(null=True, blank=True)
    codice_fiscale = models.CharField(max_length=255, blank=True)
    data_nascita = models.DateField(null=True, blank=True)
    data_iscrizione = models.DateField(null=True, blank=True)
    gruppo_sanguigno = models.CharField(max_length=10, blank=True)
    rh = models.CharField(max_length=10, blank=True)
    fenotipo = models.CharField(max_length=10, blank=True)
    kell = models.CharField(max_length=10, blank=True)
    indirizzo = models.CharField(max_length=255, blank=True)
    frazione = models.CharField(max_length=255, blank=True)
    cap = models.CharField(max_length=10, blank=True)
    comune = models.CharField(max_length=255, blank=True)
    provincia = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=255, blank=True)
    telefono_lavoro = models.CharField(max_length=255, blank=True)
    cellulare = models.CharField(max_length=255, blank=True)
    fax = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    fermo_per_malattia = models.BooleanField(default=False)
    donazioni_pregresse = models.IntegerField(default=0)
    num_benemerenze = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Donatori'
        unique_together = (
            'sezione',
            'num_tessera',
        )

    def __str__(self):
        return '{} - {} {}'.format(self.num_tessera, self.cognome, self.nome)


class Donazione(models.Model):
    class TipoDonazione(models.IntegerChoices):
        SANGUE_INTERO = 1, 'Sangue intero'
        PLASMA = 2, 'Plasma'
        PIASTRINE = 3, 'Piastrine'
        __empty__ = 'Non specificato'

    donatore = models.ForeignKey(
        Donatore, related_name='donazioni', on_delete=models.CASCADE
    )
    tipo_donazione = models.IntegerField(
        null=True,
        choices=TipoDonazione.choices,
        default=TipoDonazione.__empty__,
        blank=True,
    )
    data_donazione = models.DateField(default=date.today)

    class Meta:
        verbose_name_plural = 'Donazioni'
        unique_together = (
            'donatore',
            'data_donazione',
        )

    def __str__(self):
        return '{} - {} {}'.format(
            self.data_donazione, self.donatore.cognome, self.donatore.nome
        )

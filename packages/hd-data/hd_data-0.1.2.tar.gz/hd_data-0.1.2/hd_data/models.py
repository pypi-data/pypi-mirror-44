from django.db import models
from djangoldp.models import Model

class Faq (Model):
    question = models.TextField(verbose_name="Question")
    answer = models.TextField(verbose_name="Réponse")
    category = models.CharField(max_length=50, blank=True, null=True, verbose_name="Catégorie de question")
    def __str__(self):
        return self.question
    
class Collective (Model):
    name = models.CharField(max_length=50, verbose_name="Nom")
    email = models.CharField(max_length=50, verbose_name="Mail")
    website = models.CharField(max_length=50, blank=True, null=True, verbose_name="Site web")
    facebook = models.CharField(max_length=50, blank=True, null=True, verbose_name="Lien Facebook")
    twitter = models.CharField(max_length=50, blank=True, null=True, verbose_name="Lien Twitter")
    
    def __str__(self):
        return self.name
        
class Testimony (Model):
    name = models.CharField(max_length=50, verbose_name="Nom de l'indépendant")
    statut = models.CharField(max_length=50, verbose_name="Statut")
    porteur =  models.BooleanField(default=False, verbose_name="Porteur de cellule")
    img = models.ImageField(blank=True, null=True, verbose_name="Photo")
    
    def __str__(self):
        return self.name
        
class Event (Model):
    name = models.CharField(max_length=50, verbose_name="Nom de l'évènement")
    city = models.CharField(max_length=50, verbose_name="Ville")
    type = models.CharField(max_length=10, choices=(('apero', 'Apéro'), ('coworking', 'Coworking'),('coliving', 'Coliving'),('other', 'Autre') ), verbose_name="Type d'évènement")
    startdate =  models.DateTimeField(verbose_name="Date et heure de début")
    enddate =  models.DateTimeField(verbose_name="Date et heure de fin")
    img = models.ImageField(blank=True, null=True, verbose_name="Illustration de l'évènement")
    address = models.CharField(max_length=225, blank=True, null=True, verbose_name="Adresse") 
    description = models.TextField(verbose_name="Description")
    link = models.CharField(max_length=50, blank=True, null=True, verbose_name="Lien internet")
    facebook = models.CharField(max_length=50, blank=True, null=True, verbose_name="Lien Facebook")
    
    def __str__(self):
        return self.name
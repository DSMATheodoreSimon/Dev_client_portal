from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.timezone import localtime

class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

class Commentaire(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    auteur = models.CharField(max_length=100)
    texte = models.TextField()
    date_commentaire = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire par {self.auteur} sur {self.article}"

class Formulaire(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    groupes = models.ManyToManyField(Group, through='FormulaireGroupe', related_name='formulaires')

class ChampFormulaire(models.Model):
    TYPE_DE_CHAMP_CHOICES = [
        ('texte', 'Texte'),
        ('fichier', 'Fichier'),
        # Ajoute d'autres types de champs si nécessaire
    ]

    formulaire = models.ForeignKey(Formulaire, related_name='champs', on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    type_de_champ = models.CharField(max_length=50, choices=TYPE_DE_CHAMP_CHOICES)
    obligatoire = models.BooleanField(default=True)

    def is_file_field(self):
        return self.type_de_champ == 'fichier'

    def __str__(self):
        return f"{self.label} ({self.get_type_de_champ_display()})"

class ReponseFormulaire(models.Model):
    formulaire = models.ForeignKey(Formulaire, on_delete=models.CASCADE, related_name='reponses')
    date_soumission = models.DateTimeField(auto_now_add=True)
    fichier = models.FileField(upload_to='reponses/', null=True, blank=True)  # Pour le fichier uploadé
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, default="2")

    def __str__(self):
        return f"Réponse au formulaire {self.formulaire.titre} soumis par : {self.utilisateur.username} le {self.date_soumission.strftime('%Y-%m-%d %H:%M')}"

class ReponseChamp(models.Model):
    reponse_formulaire = models.ForeignKey(ReponseFormulaire, related_name='reponses', on_delete=models.CASCADE)
    champ = models.ForeignKey(ChampFormulaire, related_name='reponses', on_delete=models.CASCADE)
    valeur = models.TextField()  # ou un autre type de champ adapté à tes besoins
    def __str__(self):
        return f"Réponse au champ {self.champ.label}"
    
class FormulaireGroupe(models.Model):
    formulaire = models.ForeignKey(Formulaire, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Group, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('formulaire', 'groupe')

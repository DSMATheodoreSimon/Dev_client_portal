from django.views.generic import ListView, DetailView
from .forms import DynamicForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Formulaire, ReponseFormulaire, ReponseChamp
from django.contrib.auth.decorators import login_required  
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class HomePageView(ListView):
    model = Article
    template_name = 'home.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            group_ids = self.request.user.groups.values_list('id', flat=True)
            context['formulaires'] = Formulaire.objects.filter(formulairegroupe__groupe__id__in=group_ids).distinct()
            context['username'] = self.request.user.username
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'detail_article.html'
    context_object_name = 'article'

@login_required 
def afficher_formulaire(request, pk):
    formulaire = get_object_or_404(Formulaire, pk=pk)
    champs = formulaire.champs.all()
    form = DynamicForm(request.POST or None, request.FILES or None, champs=champs)

    if request.method == 'POST' and form.is_valid():
        reponse_formulaire = ReponseFormulaire(formulaire=formulaire, utilisateur=request.user)
        #reponse_formulaire.utilisateur = request.user
        fichier = request.FILES.get('File')  
        if fichier:
            reponse_formulaire.fichier = fichier
        reponse_formulaire.save()

        # Gérer les autres champs
        for champ in champs:
            valeur = form.cleaned_data.get(champ.label)
            ReponseChamp.objects.create(reponse_formulaire=reponse_formulaire, champ=champ, valeur=valeur)

        return redirect('soumission_reussie', pk=reponse_formulaire.pk)

    return render(request, 'formulaire.html', {'form': form})

def soumission_reussie(request, pk):
    # Récupère l'objet réponse en fonction de la clé primaire
    reponse = get_object_or_404(ReponseFormulaire, pk=pk)
    return render(request, 'soumission_reussie.html', {'reponse': reponse})

class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Redirige vers la page de connexion après l'inscription
    template_name = 'registration/register.html'  # Assure-toi de créer ce template
from django.forms import ModelForm
from podcast.models import Show, Episode

class ShowForm(ModelForm):
    class Meta:
        model = Show
        exclude = ('slug', 'webmaster', 'author')

class EpisodeForm(ModelForm):
    class Meta:
        model = Episode
        exclude = ('show', 'slug')

from django.forms import ModelForm
from podcast.models import Show, Episode, Enclosure

class ShowForm(ModelForm):
    class Meta:
        model = Show
        exclude = ('slug', 'webmaster', 'author')

class EpisodeForm(ModelForm):
    class Meta:
        model = Episode
        exclude = ('show', 'slug')

class EnclosureForm(ModelForm):
    class Meta:
        model = Enclosure
        exclude = ('episode','slug')

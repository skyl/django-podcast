from django.forms import ModelForm
from podcast.models import Show

class ShowForm(ModelForm):
    class Meta:
        model = Show
        exclude = ('slug', 'webmaster', 'author')

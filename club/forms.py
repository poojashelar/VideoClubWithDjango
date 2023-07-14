from .models import Video
from django import forms

class VideoForm(forms.ModelForm):
    '''Components to display on Video form'''
    class Meta:
        model = Video
        fields = ['url']
        labels = {'url': 'Youtube URL'}


class SearchForm(forms.Form):
    '''Components to display on Search form'''
    search_term = forms.CharField(max_length=255, label='Search for Videos:')

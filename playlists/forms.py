from .models import *
from django import forms

class PlayListForm(forms.ModelForm):
    
    
    
    class Meta:
        model=PlayList
        fields=('author','title','description','detail','main_image','tag')
        
class CardForm(forms.ModelForm):

    
    class Meta:
        model=Card
        fields=('photo','text')
        
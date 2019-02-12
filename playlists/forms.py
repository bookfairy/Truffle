from .models import *
from multiupload.fields import MultiImageField
from django import forms
from django.forms import modelformset_factory

# class PhotoForm(forms.ModelForm):
#     class Meta:
#         model=Photo
#         fields=('image')
#         widgets={
#             'image':
#         }
# class CardForm(forms.ModelForm):
#     class Meta:
#         model=Card
#         fields=('photo','text')

# class AddCardForm(forms.ModelForm):
#     photos=MultiImageField(min_num=1, max_num=10)
    
#     class Meta:
#         model=Card
#         fields=('photos','text')
    
        
#     def save(self,commit=True):
#         photos=self.cleaned_data.pop('photos')
#         instance=super(AddCardForm,self).save()
#         for each in photos:
#             photo=Photo(image=each,card=instance)
#             photo.save()
#         return instance

# class CardModelForm(forms.ModelForm):
#     class Meta:
#         model=Card
#         fields=('text',)
#         widgets={
#             'text':forms.TextInput(attrs={
#                 'class':form-control,
#                 'placeholder':'사진에 대해 설명해주세요'
#             })
#         }
        
# PhotoFormSet=modelformset_factory(
#     Photo,
#     fields=('image',),
#     extra = 1,
#     widgets={
#         'image':forms.FileInput(
#         attrs={
#             'class':'form-control',
#             'placeholder':'사진을 추가해주세요'
#         })
#     },
# )
# class AddPlaylistForm(forms.ModelForm):
#     pass
    
# class PlayListForm(forms.ModelForm):
    
    
    
#     class Meta:
#         model=PlayList
#         fields=('author','title','description','detail','main_image','tag')
#         widgets={
#             'author':,
#             'title':forms.TextInput(attrs={'class':'form-control','placeholder':'제목'}),
#             'description':forms.TextInput(attrs={'class':'form-control','placeholder':'요약'}),
#             'detail':forms.TextInput(attrs={'class':'form-control','placeholder':'상세설명'}),
            
#         }
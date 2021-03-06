from .models import *

from django import forms
from django.forms import modelformset_factory
from django.forms.models import BaseInlineFormSet, inlineformset_factory


class PlayListModelForm(forms.ModelForm):
    title=forms.CharField(widget=forms.Textarea(attrs={'cols':100,'rows':1,'placehodlder':'제목을 입력해주세요'}))
    description=forms.CharField(widget=forms.Textarea(attrs={'cols':100,'rows':2,'placeholder':'여행 일정에 대해 요약해주세요'}))
    detail=forms.CharField(widget=forms.Textarea(attrs={
        'cols':100,
        'rows':5,
        'placeholder':'여행에 대해서 자세하게 써주세요'
    }))
    main_image=forms.ImageField(widget=forms.FileInput())
    cost=forms.CharField(widget=forms.Textarea(attrs={'cols':50,'rows':1,'placeholder':'여행 경비를 숫자로 입력해주세요'},))
    tag_string = forms.CharField(label='태그', widget=forms.TextInput(attrs={'placeholder':'태그 앞에 꼭 #을 붙여서 작성해주세요'}))

    class Meta:
        model=PlayList
        fields=('title','description','detail','main_image','cost')

class CardModelForm(forms.ModelForm):
    text=forms.CharField(widget=forms.Textarea(attrs={'cols': 40, 'rows': 10,'placeholder':'사진에 대해 설명해주세요'}))
    location=forms.CharField(widget=forms.Textarea(attrs={'cols': 10, 'rows': 10,'placeholder':'장소에 대해 설명해주세요'}))
    class Meta:
        model=Card
        fields=('location','text',)

class PhotoModelForm(forms.ModelForm):
    image=forms.ImageField(widget=forms.FileInput(attrs={'multiple':True}))
    class Meta:
        model=Photo
        fields=('image',)
        
class CommentForm(forms.ModelForm):
    comment=forms.CharField(widget=forms.Textarea(attrs={'placeholder':'댓글달기'}))
    class Meta:
        model=Comments
        fields=('comment',)
            
from django.forms import ModelForm, CharField, TextInput, DateField, Select, CheckboxSelectMultiple
from bootstrap_datepicker_plus.widgets import DatePickerInput
from tinymce.widgets import TinyMCE
from .models import Tag, Author, Quote


class TagForm(ModelForm):

    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    
    class Meta:
        model = Tag
        fields = ['name']
        

class AuthorForm(ModelForm):
    
    fullname = CharField(max_length=50, 
                         required=True,
                         widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Fullname'}))
    born_date = DateField(required=True, 
                          widget=DatePickerInput(attrs={'class': 'form-control', 'placeholder': 'Born date:'}))
    born_location = CharField(max_length=150, 
                              required=True, 
                              widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Born location'}))
    description = CharField(required=True, 
                            widget=TinyMCE(attrs={'placeholder': 'Description'}))
    
    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']
        
        
class QuoteForm(ModelForm):
   
    class Meta:
        model = Quote
        fields = ['quote', 'author']
        widgets = {
            'quote': TinyMCE(attrs={'placeholder': 'Enter the quote'}),
            'author': Select(attrs={'class': 'form-select'}),
            'tags': CheckboxSelectMultiple(attrs={'class': 'form-select'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quote'].required = True
        self.fields['author'].required = True
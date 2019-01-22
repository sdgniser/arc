from django.forms import ModelForm
from main.models import *

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['school', 'prog', 'batch', 'about']
    
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})
        self.fields['about'].widget.attrs.update({'rows': '2'})

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['fl', 'name', 'typ', 'desc']

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            if f != 'fl':
                self.fields[f].widget.attrs.update({'class': 'form-control'})
        self.fields['desc'].widget.attrs.update({'rows': '2'})
        self.fields['fl'].widget.attrs.update({'class': 'form-control-file'})

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name']

class ItrForm(ModelForm):
    class Meta:
        model = Itr
        fields = ['sem', 'year', 'inst']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'rows': '3'})

class CommentReportForm(ModelForm):
    class Meta:
        model = CommentReport
        fields = ['typ', 'desc']

from django.forms import ModelForm
from main.models import *

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['fl', 'name', 'typ', 'desc']

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['desc'].widget.attrs.update({'rows': '3'})
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

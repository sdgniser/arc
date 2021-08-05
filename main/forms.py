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
        fields = ['fl', 'name', 'desc']
        help_texts = {
            'fl': 'The file must be of one of these types: pdf, odt, odp, doc, docx, ppt, pptx, jpg, png, txt',
            'name': '''
                The name describes what exactly the file contains. For example, 'Quiz 1' or 'Mid Term' or 'Slides on Decidability', etc.
                ''',
            'desc': '''
                The description contains any other information about the file that cannot be conveyed in the name. For example, 'Correction in Q2: inequality should be strict.' or 'These notes are from the extra class held on Diwali'
            '''
        }

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
        help_texts = {
            'sem': '''
               'Fall': Jul. - Dec. (aka. Odd semester) 
               ◦ 'Spring': Jan. - May. (aka. Even semester) 
               ◦ 'Summer': May - Jul. (for repeat courses) 
               ◦ 'Winter': Dec.
            ''',
            'inst': '''
                Avoid using titles like 'Dr.' or 'Prof.'.
                If there are more than one instructor, write their names separated by commas.
            '''
        }

    def __init__(self, *args, **kwargs):
        super(ItrForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'form-control'})

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

    def __init__(self, *args, **kwargs):
        super(CommentReportForm, self).__init__(*args, **kwargs)
        self.fields['desc'].widget.attrs.update({'rows': '2'})

class UserReportForm(ModelForm):
    class Meta:
        model = UserReport
        fields = ['typ', 'desc']

    def __init__(self, *args, **kwargs):
        super(UserReportForm, self).__init__(*args, **kwargs)
        self.fields['desc'].widget.attrs.update({'rows': '2'})

class ItemReportForm(ModelForm):
    class Meta:
        model = ItemReport
        fields = ['typ', 'desc']

    def __init__(self, *args, **kwargs):
        super(ItemReportForm, self).__init__(*args, **kwargs)
        self.fields['desc'].widget.attrs.update({'rows': '2'})

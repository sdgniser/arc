from django.forms import ModelForm
from main.models import Item, Course, Itr

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['fl', 'typ', 'num']

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name']

class ItrForm(ModelForm):
    class Meta:
        model = Itr
        fields = ['sem', 'year', 'inst']

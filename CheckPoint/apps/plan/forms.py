
import datetime

from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms import ModelChoiceField, ModelForm

from CheckPoint.apps.subject.models import Subject
from CheckPoint.apps.subject.models import CustomUser

from .models import Lecture, Plan, Week


#a costum ModelChoiceField class so we can get the name of the
#subject in the dropdown menu in CreatePlan form
class SubjectModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.name

# a formclass witch we can use to create a new plan

class CreatePlanForm(ModelForm):
    #creating a textfield for title
    title = forms.CharField(required=True,label='Title',
                    widget=forms.TextInput(attrs={'placeholder': 'title...','class':'form-control'}))
    #creating a dropdown for subjects witch gets all the subjects from the database
    subject = SubjectModelChoiceField(queryset = None,
                    widget=forms.Select(attrs={'class':'form-control'}))
    #creating a textfield for term
    term = forms.CharField(required=True,label='Term:',
                    widget=forms.TextInput(attrs={'placeholder': 'term...','class':'form-control'}))
    #creating a IntegerField for the year, the default is the current year
    year = forms.IntegerField(required=True,label='Year:',initial=datetime.datetime.now().year,
                    widget=forms.NumberInput(attrs={'class':'form-control'}))

    beginning_week =forms.IntegerField(required=False, label='Beginning week:',
                    widget=forms.NumberInput(attrs={'placeholder': 'week number','class':'form-control'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user',None)
        super(CreatePlanForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = user.teachingSubject.all()
    #the model we will use will be the auth User model and the fields are named title, subject, term, year
    class Meta:
        model = Plan
        fields = ('title','subject','term','year')


"""
Form for creating a lecture, excludes foreign key and many to many field and add them in the view.
"""
class CreateLectureForm(ModelForm):
    objectives_form_field = forms.CharField(required=False,label='Learning objectives',
                                            widget=forms.Textarea(attrs={
                                                'placeholder': "Learningobjectives seperated by ';'",'class':'form-control'
                                            }))
    class Meta:
        model = Lecture
        exclude = ['plan','week', 'objectives']
        fields = ['id', 'title', 'comment',]

    def __init__(self, *args, **kwargs):
        super(CreateLectureForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class' : 'form-control'})
        self.fields['comment'].widget.attrs.update({'class' : 'form-control'})



"""
Form for deleting a lecture.
"""
class DeleteLectureForm(ModelForm):
    class Meta:
        model =  Lecture
        fields = []


"""
Form for creating a week. Sets empty permitted to true, which allows the form to be empty.
"""
class CreateWeekForm(ModelForm):
    def __init__(self, *arg, **kwarg):
        super(CreateWeekForm, self).__init__(*arg, **kwarg)
        self.empty_permitted = True

    class Meta:
        model = Week
        exclude = ['plan', 'week_number']
        fields = []


"""
Form for deleting a week.
"""
class DeleteWeekForm(ModelForm):
    class Meta:
        model = Week
        fields = []

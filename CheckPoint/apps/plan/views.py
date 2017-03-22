from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from .models import Plan, Week, Lecture, Objectives
from .forms import CreatePlanForm, CreateLectureForm, DeleteLectureForm,\
    CreateWeekForm, DeleteWeekForm
from django.shortcuts import get_object_or_404


"""
The index view is rendered on main plan page, sends de context for use in html/frontend.
Gets the plan by the plan_id in the query.
"""
def index(request, plan_id):
    plan = Plan.objects.get(id=plan_id)
    weeks = plan.weeks.all()
    lectures = plan.lectures.all()
    subject = plan.subject
    objectives = subject.learning_objectives.all()

    context = {
        'plan': plan,
        'weeks': weeks,
        'lectures': lectures,
        'subject': subject,
        'objectives': objectives,
        'create_or_edit_lecture_form': CreateLectureForm(),
        'delete_lecture_form': DeleteLectureForm(),
        'create_week_form': CreateWeekForm(),
        'delete_week_form': DeleteWeekForm(),

    }
    return render(request, 'plan/plan.html', context)


"""
The create_plan view sends an empty context to html template and checks if we get a POST request.
If it does, it creates a CreatePlanForm with the information it got and if that form is valid
the page gets redirected to the plan that just was created.
If not, the form class with the dictionary to the template.
"""
def create_plan(request):
    #the dictionary we will send to the html template
    context={}
    #if we get a POST request jump into the if statement
    if request.method == 'POST':
        #set for to the POST request we got
        form = CreatePlanForm(request.POST)
        #if the form was valid,save it and redirect us to the site for the new plan
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../'+ str(Plan.objects.latest('id').id))
    else:
        #if we dont get a POST request, send the form class with the dictionary to the template
        form = CreatePlanForm()
        context['form'] = form
    return render(request,'plan/createplan.html',context)

"""
The create_or_edit_lecture view is used to create or edit an lecture. It checks if there is a POST request.
If there is, the hidden fields is saved. If the lecture_id does not exist it creates an empty CreateLectureForm
if it does an CreateLectureForm with the lecture as an instance is created.
The form, if valid, is used to create a lecture, foreign keys/excluded keys is found and added to the lecture, then
the lecture is saved. Many to many field Objectives is added afterwords.

Then the page get reloaded.
"""
def create_or_edit_lecture(request):
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id', None)
        week_id = request.POST.get('week_id', None)
        #Try to get lecture_id from template, if there are none lecture_id will be None
        lecture_id = request.POST.get('lecture_id', None)
        plan = Plan.objects.get(id=plan_id)
        week = Week.objects.get(id=week_id)
        if lecture_id != None:
            lecture_to_edit = get_object_or_404(Lecture, id=lecture_id)
            form = CreateLectureForm(request.POST or None, instance=lecture_to_edit)
        else:
            form = CreateLectureForm(request.POST or None)
        if form.is_valid():
            lecture = form.save(commit=False)
            lecture.plan = plan
            lecture.week = week
            lecture.save()
            objectives = form.cleaned_data.pop('objectives_form_field').split(';')
            lecture_objectives = []
            for objective in objectives:
                lecture_objective, exists = Objectives.objects.get_or_create(learning_objective=objective,
                                                                             subject=plan.subject)
                lecture_objectives.append(lecture_objective)
            lecture.objectives = lecture_objectives
            lecture.save()
        return HttpResponseRedirect(reverse('plan', args=[plan_id]))

"""
The delete_lecture view is used to delete a lecture. When the deletebutton is clicked a POST request is sent.
The view checks if the DeleteLectureForm is valid then deletes the lecture and redirects to the plan.
"""
def delete_lecture(request):
    lecture_id = request.POST.get('lecture_id', None)
    lecture_to_delete = get_object_or_404(Lecture, id=lecture_id)
    plan_id = lecture_to_delete.plan.id

    if request.method == 'POST':
        form = DeleteLectureForm(request.POST, instance=lecture_to_delete)
        if form.is_valid():
            lecture_to_delete.delete()
            return HttpResponseRedirect(reverse('plan', args=[plan_id]))

"""
The create_week view is used to create a week. When request is POST the plan_id and week_number is retrieved. Add 1 to
week_number because the new week have to be the week after the other. Form is created and if form is valid
it is saved without commit, for then to save foreign key plan and week_number to the new object. Site is
redirected to plan.
"""
def create_week(request, plan_id):
    if request.method == 'POST':
        plan = Plan.objects.get(id=plan_id)
        week_number = int(request.POST.get('week_number')) + 1
        form = CreateWeekForm(request.POST or None)

        if form.is_valid():
            week = form.save(commit=False)
            week.plan = plan
            week.week_number = week_number
            week.save()
            return HttpResponseRedirect(reverse('plan', args=[plan_id]))

"""
The delete_week view is used to delete a week. When the deletebutton is clicked a POST request is sent.
The view checks if the DeleteLectureForm is valid then deletes the week and redirects to the plan.
"""
def delete_week(request):
    week_id = request.POST.get('week_id', None)
    week_to_delete = get_object_or_404(Week, id=week_id)
    plan_id = week_to_delete.plan.id

    if request.method == 'POST':
        form = DeleteWeekForm(request.POST, instance=week_to_delete)
        if form.is_valid():
            week_to_delete.delete()
            return HttpResponseRedirect(reverse('plan', args=[plan_id]))
          
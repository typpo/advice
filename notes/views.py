import json

from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect

from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.forms.formsets import formset_factory
from django.template import RequestContext

from notes.forms import InterviewForm
from notes.forms import InterviewEditForm
from notes.forms import QuestionEditForm
from notes.models import Profile
from notes.models import Company
from notes.models import Position
from notes.models import Interview
from notes.models import Question

# Lists top N companies and positions, by things like quantity and 
# recent activity
def index(request):
    return render_to_response('notes/home.html', \
        {
            'companies': Company.objects.all().order_by('-updated')[:10],
        }, context_instance=RequestContext(request))

def search(request):
    return render_to_response('notes/search.html', \
        {
        }, context_instance=RequestContext(request))

# Lists by company and top N positions
def company_index(request):
    order = request.GET.get('order', 'name')
    
    if order == 'name':
        companies = Company.objects.all().order_by('name')
    elif order == 'positions':
        # Sort by # positions
        companies = Company.objects.all().annotate( \
            poscount=Count('positions')).order_by('-poscount')
    elif order == 'interviews':
        # Sort by # interviews
        companies = Company.objects.all().annotate( \
            icount=Count('interview')).order_by('-icount')
    else:
        # order by recent
        companies = Company.objects.all().order_by('-updated')

    return render_to_response('notes/company_index.html', \
        {
            'order': order,
            'companies': companies,
        }, context_instance=RequestContext(request))

# Lists by position and top N companies
def position_index(request):
    order = request.GET.get('order', 'title')
    
    if order == 'title':
        positions = Position.objects.all().order_by('title')
    elif order == 'companies':
        # Sort by # companies
        positions = Position.objects.all().annotate( \
            ccount=Count('company')).order_by('-ccount')
    elif order == 'interviews':
        # Sort by # interviews
        positions = Position.objects.all().annotate( \
            icount=Count('interview')).order_by('-icount')
    else:
        # order by recent
        positions = Position.objects.all().order_by('-updated')

    return render_to_response('notes/position_index.html', \
        {
            'order': order,
            'positions': positions,
        }, context_instance=RequestContext(request))

# positions by company
def company(request, company_id):
    company = Company.objects.get(pk=company_id)
    return render_to_response('notes/company.html', \
        {
            'company': company,
        }, context_instance=RequestContext(request))

def company_by_name(request, company_name):
    try:
        company = Company.objects.get(name=company_name)
    except ObjectDoesNotExist:
        try:
            company = Company.objects.get(name__contains=company_name)
        except ObjectDoesNotExist:
            return -1

    if id < 0:
        raise Http404
    return company(request, company.id)

# companies by position
def position(request, position_id):
    position = Position.objects.get(pk=position_id)
    return render_to_response('notes/position.html', \
        {
            'position': position,
        }, context_instance=RequestContext(request))

def position_by_title(request, position_title):
    try:
        position = Position.objects.get(title=position_title)
    except ObjectDoesNotExist:
        try:
            position = Company.objects.get(name__contains=position_title)
        except ObjectDoesNotExist:
            return -1

    if id < 0:
        raise Http404
    return position(request, position.id)

# Lists by position, company, or both, by id
def interviews(request):
    args = request.GET
    kwargs = {}
    if 'company' in args:
        kwargs['company__id'] = args['company']
    if 'position' in args:
        kwargs['position__id'] = args['position']

    if len(kwargs) < 1:
        raise Http404

    interviews = Interview.objects.filter(**kwargs).order_by('-position', 'date')
    if len(interviews) < 1:
        raise Http404

    return render_to_response('notes/interviews.html', \
        {
            'interviews': interviews,
            'loggedin': not request.user.is_anonymous(),
            # TODO logged in users get error here if there is no profile for them (ie. admin).
            'profile': None if request.user.is_anonymous() else request.user.get_profile(),
        }, context_instance=RequestContext(request))

# Submit interview
def add(request):
    failed = False
    addednew = False
    formerror = None

    if request.POST:
        custom_fields = [f for f in request.POST \
            if f.startswith('id_answer') or f.startswith('id_question')]

        attrs = dict((field, forms.CharField(max_length=100, required=False)) \
            for field in custom_fields)
        DynamicForm = type("DynamicForm", (InterviewForm,), attrs)

        f = DynamicForm(request.POST)
        # blank description can be valid w/ question and answer
        if f.is_valid():
            d = f.cleaned_data

            input_company = d['company']
            input_position = d['position']

            input_date = d.get('date', None)
            input_description = d.get('description', None)
            input_question = d.get('question', None)
            input_answer = d.get('answer', '')

            # find position
            try:
                position = Position.objects.get(title=input_position)
            except ObjectDoesNotExist:
                position = Position()
                position.title = input_position
                position.save()

            # find company
            try:
                company = Company.objects.get(name=input_company)
            except ObjectDoesNotExist:
                company = Company()
                company.name = input_company
                company.save()
                company.positions.add(position)
                company.save()

            position.company_set.add(company)
            position.save()
                
            i = Interview()
            # add profile if logged in
            i.profile = None if request.user.is_anonymous() else request.user.get_profile()
            # other interview details
            i.company = company
            i.position = position
            i.description = input_description
            i.date = input_date
            i.save()

            # questions
            if input_question:
                def saveQandA(interview, question, answer):
                    addme = Question()
                    addme.interview = interview;
                    addme.question = question
                    addme.answer = answer
                    addme.save()

                saveQandA(i, input_question, input_answer)
                c = 2
                while 1:
                    q = 'id_question'+str(c)
                    a = 'id_answer'+str(c)
                    if q in d:
                        saveQandA(i, d[q], d.get(a, ''))
                        c += 1
                    else:
                        break

            addednew = True
        else:
            formerror = f.errors
            failed = True

    return render_to_response('notes/add.html', \
        {
            'form': InterviewForm(),
            'addednew': addednew,
            'failed': failed,
            'formerror': formerror,
            'loggedin': not request.user.is_anonymous(),
        }, context_instance=RequestContext(request))

# Edit interview
@login_required
def edit_interview(request, id):
    interview = get_object_or_404(Interview, pk=id)
    if request.user.get_profile() != interview.profile:
        # no good
        return HttpResponse("Not your interview - maybe you need to login or change accounts.")

    formerror = None
    success = False

    if request.POST:
        f = InterviewEditForm(request.POST, instance=interview)
        if f.is_valid():
            f.save()
            success = True
        else:
            formerror = f.errors
            success = False

    return render_to_response('notes/edit.html', \
        {
            'form': InterviewEditForm(instance=interview),
            'interview': interview,
            'formerror': formerror,
            'success': success,
        }, context_instance=RequestContext(request))

# Edit question
@login_required
def edit_question(request, id):
    question = get_object_or_404(Question, pk=id)
    if request.user.get_profile() != question.interview.profile:
        return HttpResponse("Not your question- maybe you need to login or change accounts.")

    question = get_object_or_404(Question, pk=id)
    if request.user.get_profile() != question.interview.profile:
        # no good
        return HttpResponse("Not your interview - maybe you need to login or change accounts.")

    formerror = None
    success = False

    if request.POST:
        f = QuestionEditForm(request.POST, instance=question)
        if f.is_valid():
            f.save()
            success = True
        else:
            formerror = f.errors
            success = False

    return render_to_response('notes/edit_question.html', \
        {
            'form': QuestionEditForm(instance=question),
            'question': question,
            'formerror': formerror,
            'success': success,
        }, context_instance=RequestContext(request))

# Typeahead completion for entering a company name
def companytags(request):
    if 'term' in request.GET:
        companies = Company.objects.filter(name__contains=request.GET['term'])
        resp = json.dumps([company.name for company in companies])
        return HttpResponse(resp)
    else:
        return HttpResponse('[]')

# Typeahead completion for entering a position title
def positiontags(request):
    if 'term' in request.GET:
        positions = Position.objects.filter(title__contains=request.GET['term'])
        resp = json.dumps([position.title for position in positions])
        return HttpResponse(resp)
    else:
        return HttpResponse('[]')


# User sign up
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/notes/")
    else:
        form = UserCreationForm()

    return render_to_response("registration/signup.html", {
        'form': form,
    }, context_instance=RequestContext(request))

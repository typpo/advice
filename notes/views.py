from django.shortcuts import render_to_response
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.contrib.auth.models import AnonymousUser
from notes.forms import InterviewForm
from notes.models import Profile
from notes.models import Company
from notes.models import Position
from notes.models import Interview
from notes.models import Question

# Lists top N companies and positions, by things like quantity and 
# recent activity
def index(request):
    raise Http404

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
        })

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
        })

# positions by company
def company(request, company_id):
    company = Company.objects.get(id=company_id)
    return render_to_response('notes/company.html', \
        {
            'company': company,
        })

def company_by_name(request, company_name):
    id = get_company_id(company_name)
    if id < 0:
        raise Http404
    return company(request, id)

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
        })

# Find closest match to company by name
def get_company_id(company_name):
    try:
        company = Company.objects.get(name=company_name)
    except ObjectDoesNotExist:
        try:
            company = Company.objects.get(name__contains=company_name)
        except ObjectDoesNotExist:
            return -1
    return company.id

# Submit interview
def add(request):
    failed = False
    addednew = False

    if request.POST:
        f = InterviewForm(request.POST)
        # TODO blank question, answer can be valid
        # blank description can be valid w/ question and answer
        if f.is_valid():
            d = f.cleaned_data
            input_company = d['company']
            input_position = d['position']

            input_date = d.get('date', None)
            input_description = d.get('description', None)
            input_question = d.get('question', None)
            input_answer = d.get('answer', '')

            # TODO add profile?

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
                
            i = Interview()
            i.company = company
            i.position = position
            i.description = input_description
            i.date = input_date
            i.save()

            # questions
            def saveQandA(interview, question, answer):
                q= Question()
                q.interview = interview;
                q.question = question
                q.answer = answer
                q.save()
            
            if input_question:
                saveQandA(i, input_question, input_answer)
                c = 1
                while 1:
                    q = 'id_question'+str(c)
                    a = 'id_answer'+str(c)
                    if q in d:
                        saveQAndA(i, d[q], d.get(a, ''))
                        c += 1
                    else:
                        break

            addednew = True
        else:
            failed = True

    return render_to_response('notes/add.html', \
        {
            'form': InterviewForm(),
            'addednew': addednew,
            'failed': failed,
        })

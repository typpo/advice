from django.shortcuts import render_to_response
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from notes.forms import InterviewForm
from notes.models import Profile
from notes.models import Company
from notes.models import Position
from notes.models import Interview

# Lists top N companies and positions, by things like quantity and 
# recent activity
def index(request):
    pass    

# Lists by company and top N positions
def company_index(request):
    companies = Company.objects.all()
    return render_to_response('notes/company_index.html', \
        {
            'companies': companies,
        })

# Lists by position and top N companies
def position_index(request):
    positions = Position.objects.all()
    return render_to_response('notes/position_index.html', \
        {
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

    interviews = Interview.objects.filter(**kwargs)
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
        if f.is_valid():
            new_interview = f.save()
            new_interview.save()
            addednew = True
        else:
            failed = True

    return render_to_response('notes/add.html', \
        {
            'form': InterviewForm(),
            'addednew': addednew,
            'failed': failed,
        })

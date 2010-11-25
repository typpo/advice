from django.shortcuts import render_to_response
from notes.models import Profile
from notes.models import Company
from notes.models import Position
from notes.models import Interview

# Lists by company and top N positions
def company_index(request):
    companies = Company.objects.all()
    return render_to_response('notes/company_index.html'. \
        {
            'companies': companies,
        })

# Lists by position and top N companies
def position_index(request):
    positions = Position.objects.all()
    return render_to_response('notes/position_index.html'. \
        {
            'positions': positions,
        })
    
# Lists all positions
def company(request, company_id):
    company = Company.objects.get(id=company_id)
    return render_to_response('notes/company.html'. \
        {
            'company': company,
        })

def company_by_name(request, company_name):
    return company(request, get_company_id(company_name))

# Lists by position, company, or both
def interviews(request, company, position):
    interviews = Interview.objects.filter(company__name=company, \
        position__title=position)
    return render_to_response('notes/interviews.html'. \
        {
            'interviews': interviews,
        })

# Find closest match to company by name
def get_company_id(company_name):
    company = Company.objects.get(name=company_name)
    return company.id

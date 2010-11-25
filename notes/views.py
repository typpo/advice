from django.shortcuts import render_to_response
from notes.models import Profile
from notes.models import Company
from notes.models import Position
from notes.models import Interview

# Lists by company and top N positions
def index(request):
    pass
    

# Lists all positions
def company(request, company_id):
    company = Company.objects.get(id=company_id)

def company_by_name(request, company_name):
    return company(request, get_company_id(company_name))

# Lists by position, company, or both
def interviews(request, company, position):
   pass 

# Find closest match to company by name
def get_company_id(company_name):
    pass

from datetime import timedelta
from sqlite3 import IntegrityError
from unittest import result
from xmlrpc.client import DateTime
from dateutil.relativedelta import relativedelta
from typing import Counter
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.db import IntegrityError
from .functions import *
from .forms import *
from .models import *
# from .forms import *

# fuc

def initialize_Forms(result,value):
    temp = {
        "patentForm":PatentForm(),
        "installmentForm":InstallmentForm(),
        "teamForm":TeamForm(),
        "copyrightForm":CopyrightForm(),
        "trademarkForm":TrademarkForm(),
        "projectForm":ProjectForm(),
        "revenueForm":ProjectRevenueForm(),
        "internForm":ProjectInternForm(),
        "employmentForm":ProjectEmploymentForm(),
        "awardsForm":ProjectAwardsForm(),
        "productForm":ProjectProductForm(),
    }
    for i in temp.keys():
        if not i == value:
            result[i] = temp[i]
    return result

# Create your views here.
def login_user(request):    
    if datetime.date.today().month >= 3:
        for i in range(datetime.date.today().year,datetime.date.today().year+1):
            try:
                FinancialYear.objects.create(financialYear = str(i)+'-'+str(i+1))
            except:
                pass
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        
        report = {
            "1":[], "2":[], "3":[], "4":[], "5":[],
            "6":[], "7":[], "8":[], "9":[], "10":[], "11":[],
        }
        
        # 1
        report['1'].append(Incubatee.objects.all().count())
        report['1'].append(Company.objects.all().filter(graduationType = "Live").values("incubatee_ID").distinct().count())
        report['1'].append(Incubatee.objects.all().exclude(alumini = None).count())
        
        # 2
        report['2'].append(Project.objects.filter(status = "Discontinued").count())
        date = datetime.datetime.today() -datetime.timedelta(days=365*2)
        report['2'].append(Project.objects.filter(status = "Discontinued",dropoutDate__range = [date,datetime.datetime.today()]).count())
        report['2'].append(Project.objects.filter(status = "Discontinued").exclude(dropoutDate__range = [date,datetime.datetime.today()]).values('incubatee').distinct().count())
        
        # 3
        report['3'].append(aggregate_Amount(Project.objects.filter(fund_type = "Loan").values('amount'),['amount'])[0])
        report['3'].append(aggregate_Amount(Project.objects.filter(fund_type = "Grant").values('amount'),['amount'])[0])
        report['3'].append(Project.objects.filter(Q(fund_type = "Grant") | Q(fund_type = "Loan")).values('incubatee').distinct().count())
        
        
        # 4
        report['4'].append(getNumberAsWord(aggregate_Amount(FundLog.objects.all().values('sanctionedAmt'),['sanctionedAmt'])[0]))
        
        # 5
        report['5'].append(Project.objects.filter(Q(projectStatus = "Product")|Q(projectStatus = "Commercialised")).count())
        report['5'].append(Project.objects.exclude(Q(projectStatus = "Product")|Q(projectStatus = "Commercialised")).count())
        
        # 6
        report['6'].append(ProjectAwards.objects.all().count())
        
        # 7
        report['7'].append(ProjectEmployment.objects.all().aggregate(Sum('employment'))['employment__sum'])
        report['7'].append(ProjectIntern.objects.all().count())
        
        # 8
        report['8'].append(Events.objects.all().count())
        sum = 0
        sum += Events.objects.all().values_list('inKECstudents').aggregate(Sum('inKECstudents'))['inKECstudents__sum']
        sum += Events.objects.all().values_list('outstudents').aggregate(Sum('outstudents'))['outstudents__sum']
        sum += Events.objects.all().values_list('inKECstaffs').aggregate(Sum('inKECstaffs'))['inKECstaffs__sum']
        sum += Events.objects.all().values_list('outstaffs').aggregate(Sum('outstaffs'))['outstaffs__sum']
        sum += Events.objects.all().values_list('inKECOrganizaions').aggregate(Sum('inKECOrganizaions'))['inKECOrganizaions__sum']
        sum += Events.objects.all().values_list('outOrganizaions').aggregate(Sum('outOrganizaions'))['outOrganizaions__sum']
        report['8'].append(sum)

            
            
        
        # 9
        report['9'].append(Patents.objects.all().filter(status__contains = "Filed").count())
        report['9'].append(Patents.objects.all().filter(status__contains = "Granted").count())
        report['9'].append(Copyright.objects.all().filter(status__contains = "Filed").count())
        report['9'].append(Copyright.objects.all().filter(status__contains = "Granted").count())
        report['9'].append(Trademark.objects.all().count())
        
        return render(request, 'dashboard.html', {
            "user":user,
            "report":report,
        })
    else:
        return render(request, 'login.html', {})

# home
@login_required(login_url='/login/')
def home(request):
    return login_user(request)
    
#gallery
@login_required(login_url='/login/')
def galleryVisitors(request):
    result = getFiles('Visitors/')
    result['active'] = 'visitors'
    return render(request, 'gallery.html', result)

@login_required(login_url='/login/')
def galleryEvents(request):
    result = getFiles('Events/')
    result['active'] = 'events'
    return render(request, 'gallery.html', result)

@login_required(login_url='/login/')
def galleryIncubatees(request):
    result = getFiles('Incubatees/Profile Pics/')
    result['active'] = 'profilePic'
    return render(request, 'gallery.html', result)

@login_required(login_url='/login/')
def galleryTeam(request):
    result = getFiles('Company/Team/')
    result['active'] = 'TeamProfilePics'
    return render(request, 'gallery.html', result)

@login_required(login_url='/login/')
def galleryCompanyLogo(request):
    result = getFiles('Company/Logo/')
    result['active'] = 'companyLogo'
    return render(request, 'gallery.html', result)

@login_required(login_url='/login/')
def galleryIncorporations(request):
    result = getFiles('Company/Incorporation/')
    result['active'] = 'CompanyIncorporation'
    return render(request, 'gallery.html', result)

@login_required(login_url='/login/')
def galleryEntities(request):
    result = getFiles('Company/Entity/')
    result['active'] = 'entity_Certificate'
    return render(request, 'gallery.html', result)

@login_required(login_url='/login/')
def galleryClosureReports(request):
    result = getFiles('Project/Closure Report/')
    result['active'] = 'closureReport_Certificate'
    return render(request, 'gallery.html', result)

@login_required(login_url='/login/')
def galleryUCReports(request):
    result = getFiles('Project/UC Report/')
    result['active'] = 'UCReport_Certificate'
    return render(request, 'gallery.html', result)

@login_required(login_url='/login/')
def galleryInstallments(request):
    result = getFiles('Projects/UC/')
    result['active'] = 'Installment_UC_Certificate'
    return render(request, 'gallery.html', result)

@login_required(login_url='/login/')
def galleryInstallmentProgress(request):
    result = getFiles('Projects/Progress/')
    result['active'] = 'Installment_Progress_Certificate'
    return render(request, 'gallery.html', result)

@login_required(login_url='/login/')
def galleryProducts(request):
    result = getFiles('Projects/Product/')
    result['active'] = 'Product_Photo'
    return render(request, 'gallery.html', result)

@login_required(login_url='/login/')
def galleryTrademarks(request):
    result = getFiles('Projects/Trademark/')
    result['active'] = 'Trademark_Photo'
    return render(request, 'gallery.html', result)

@login_required(login_url='/login/')
def galleryAwards(request):
    result = getFiles('Projects/Awards/')
    result['active'] = 'Awards_Photo'
    return render(request, 'gallery.html', result)

#visitors
@login_required(login_url='/login/')
def visitors(request):
    visitorForm = VisitorForm()
    visitorImageForm = VisitorImagesForm()
    ErrorForm = -1
    toast = []
    if request.method == 'POST':
        if 'addVisitor' in request.POST:
            visitorForm = CheckValidAndSave(request,VisitorForm)
            if visitorForm.non_field_errors():
                visitorForm.add_error('date',"")
                visitorForm.add_error('guestName',"")
                visitorForm.add_error('name',"Visitors with this Date of visit, Guest Name and Name of Organisation/ Institute already exists.")
            if len(visitorForm.errors) > 0:
                ErrorForm = 1
            else:
                toast = ["success","Visitors were Recorded."]
        elif 'addVisitorImage' in request.POST:
            visitorImageForm = VisitorImagesForm(request.POST,request.FILES)
            if visitorImageForm.is_valid():
                # print(visitorImageForm.save())
                visitorImageForm.save()
                toast = ["success","Visitor Images were Uploaded."]
            else:
                ErrorForm = 2
                
    visitor = Visitors.objects.all().values().order_by('-date')
    for i in visitor:
        i['images'] = VisitorImages.objects.filter(visitor__id = i['id']) 
    return render(request, 'visitors.html', {
        "visitors":visitor,
        "visitorForm":visitorForm,
        "visitorImageForm":visitorImageForm,
        "ErrorForm":ErrorForm,
        "toast":toast,
    })
    
#events
@login_required(login_url='/login/')
def events(request):
    ErrorForm = -1
    toast = []
    
    eventForm = EventForm()
    eventPhotoForm = EventImagesForm()
    eventReportForm = EventReportsForm()
    eventSponserForm = EventSponserForm()
    if request.method == 'POST':
        if 'addEvent' in request.POST:
            eventForm = CheckValidAndSave(request, EventForm)
            if len(eventForm.errors) == 0:
                toast = ["success","Event was Recorded Successfully"]
            else:
                ErrorForm = 1
        elif 'addEventImage' in request.POST:
            eventPhotoForm = CheckValidAndSave(request, EventImagesForm)
            if len(eventPhotoForm.errors) == 0:
                toast = ["success","Event Photos was uploaded Successfully"]                
            else:
                ErrorForm = 2
        elif 'addEventReports' in request.POST:
            eventReportForm = CheckValidAndSave(request, EventReportsForm)
            if len(eventReportForm.errors) == 0:
                toast = ["success","Event Reports was uploaded Successfully"]
            else:
                ErrorForm = 3
        elif 'addEventSponser' in request.POST:
            eventSponserForm = CheckValidAndSave(request, EventSponserForm)
            if len(eventSponserForm.errors) == 0:
                toast = ["success","Event Sponsers were recorded Successfully"]
            else:
                ErrorForm = 4
    events = Events.objects.all().values().order_by('-fromdate')
    for i in events:
        i['sponsers'] = EventSponsors.objects.filter(eventSponser__id = i['id']).all()
        i['images'] = EventImages.objects.filter(event__id = i['id']).all()
        i['reports'] = EventReports.objects.filter(events__id = i['id']).all()
    
    return render(request, 'events.html', {
        "ErrorForm":ErrorForm,
        "toast":toast,
        'eventForm':eventForm,
        'eventPhotoForm':eventPhotoForm,
        'eventReportForm':eventReportForm,
        'eventSponserForm':eventSponserForm,
        'events':events,
    })
    
#settings
@login_required(login_url='/login/')
def settings(request):
    toast = []
    entityForm = EntityForm()
    schemeForm = SchemeForm()
    fundtypeForm = FundingForm()
    ErrorForm = -1
    # Incubatee.objects.all().delete
    if request.method == 'POST':
        if 'addScheme' in request.POST:
            schemeForm = CheckValidAndSave(request,SchemeForm)
            if len(schemeForm.errors) > 0:
                ErrorForm = 1
            else:
                toast = ["success","Scheme Added Successfully"]
        elif 'toggleScheme' in request.POST:
            scheme = Schemes.objects.get(schemeName = request.POST['toggleScheme'])
            toast = ["error","Scheme status was Changed."]
            if scheme.status == True:
                scheme.status = False
            else:
                scheme.status = True
            scheme.save()
        elif 'addFundType' in request.POST:
            fundtypeForm = CheckValidAndSave(request,FundingForm)
            if len(fundtypeForm.errors) > 0:
                ErrorForm = 2
            else:
                toast = ["success","Fund Type Added Successfully"]
        elif 'deleteFundType' in request.POST:
            FundingType.objects.filter(fundType = request.POST['deleteFundType']).delete()
            toast = ["error","Fund Type was deleted."]
        elif 'addEntity' in request.POST:
            entityForm = CheckValidAndSave(request,EntityForm)
            if len(entityForm.errors) > 0:
                ErrorForm = 3
            else:
                toast = ["success","Entity Added Successfully"]
        elif 'deleteEntity' in request.POST:
            Entity.objects.filter(entityName = request.POST['deleteEntity']).delete()
            toast = ["error","Entity was deleted."]
        else:
            pass 
    Scheme = Schemes.objects.all()
    FundType = FundingType.objects.all()
    Entities = Entity.objects.all()

    return render(request, 'settings.html', {
        "Scheme":Scheme,
        "FundType":FundType,
        "Entities":Entities,
        "EntityForm":entityForm,
        "SchemeForm":schemeForm,
        "fundtypeForm":fundtypeForm,
        "toast":toast,
        "ErrorForm":ErrorForm,
    })

#fundflow
@login_required(login_url='/login/')
def fundflow(request):
    fundLogForm = FundLogForm()
    toast = []
    ErrorForm = -1
    if request.method == "POST":
        fundLogForm = CheckValidAndSave(request,FundLogForm)
        if len(fundLogForm.errors) > 0:
            ErrorForm = 1
        else:
            toast = ["success","Fund was added Successfully."]
    schemes = Schemes.objects.all().values()
    for i in schemes:
        dateList = []
        i['incubatees'] = Project.objects.filter(scheme_id = i['schemeName']).values('incubatee').distinct().count()
        fundDisbursement = FundDisbursement.objects.filter(scheme_id = i['schemeName']).values()
        fundUtilization = FundUtilization.objects.filter(scheme_id = i['schemeName']).values()
        funds = aggregate_Amount(fundDisbursement,['prototypeGrant','operationExpenditure','fabLab'])
        i['disbursed'] = currencySeparator(sum([ getAmount(j) for j in funds ]))
        funds = aggregate_Amount(fundUtilization,['prototypeGrant','operationExpenditure','fabLab'])
        i['utilized'] = currencySeparator(sum([ getAmount(j['amount']) for j in Project.objects.filter(scheme_id = i['schemeName']).values('amount') ]))
        i['returned'] = currencySeparator(sum([ getAmount(j) for j in aggregate_Amount(fundUtilization,['returnedAmt']) ]))
        i['interest'] = currencySeparator(sum([ getAmount(j) for j in aggregate_Amount(fundUtilization,['interestAmt']) ]))
        try:            
            dateList.append(fundUtilization.order_by('-updateOn').values('updateOn')[0]['updateOn'])
        except:
            try:
                dateList.append(fundDisbursement.order_by('-updateOn').values('updateOn')[0]['updateOn'])
            except:
                pass
        i['balance'] = currencySeparator(getAmount(i['disbursed']) - getAmount(i['utilized']) + getAmount(i['returned']) + getAmount(i['interest']))
        if getAmount(i['balance']) < 0:
            i['balance'] = currencySeparator(getAmount(i['amount']))
            
        i['lastUpdate'] = getRecentDate(dateList)
        
    return render(request, 'fundflow.html', {
        "fundLogForm":fundLogForm,
        "ErrorForm":ErrorForm,
        "toast":toast,
        "schemes":schemes,
    })
#fund Flow Years
@login_required(login_url='/login/')
def scheme(request,name,pagination):
            
    years = FinancialYear.objects.all().order_by('-financialYear').values()
    pagination_list = [i for i in range(1,(len(years)//10)+2)]
    if pagination == 1:
        years = years[:10]
    else:
        start = (pagination-1) * 10
        years = years[start:start+10]
    openBalance = 0
    for i in years[::-1]:
        dateList = []
        i['sanctioned'] = is_Empty(FundLog.objects.filter(financialYear = i['financialYear'], schemeName = name).values('sanctionedAmt'),'sanctionedAmt')
        i['total'] = Project.objects.filter(financialYear_id = i['financialYear'], scheme_id = name).values('incubatee').distinct().count()
        i['openingBalance'] = openBalance
        fundDisbursement = FundDisbursement.objects.filter(scheme_id = name,financialYear_id = i['financialYear']).values()
        fundUtilization = FundUtilization.objects.filter(scheme_id = name,financialYear_id = i['financialYear']).values()
        try:            
            dateList.append(fundUtilization.order_by('-updateOn').values('updateOn')[0]['updateOn'])
        except:
            try:
                dateList.append(fundDisbursement.order_by('-updateOn').values('updateOn')[0]['updateOn'])
            except:
                pass
        funds = aggregate_Amount(fundDisbursement,['prototypeGrant','operationExpenditure','fabLab'])
        i['disbursed'] = currencySeparator(sum([ getAmount(j) for j in funds ]))
        funds = aggregate_Amount(fundUtilization,['prototypeGrant','operationExpenditure','fabLab'])
        i['utilized'] = currencySeparator(sum([ getAmount(j) for j in funds ]))
        i['returned'] = currencySeparator(sum([ getAmount(j) for j in aggregate_Amount(fundUtilization,['returnedAmt']) ]))
        i['interest'] = currencySeparator(sum([ getAmount(j) for j in aggregate_Amount(fundUtilization,['interestAmt']) ]))
        if i['openingBalance'] != 0:
            i['balance'] = currencySeparator(getAmount(openBalance) - getAmount(i['disbursed']) - getAmount(i['utilized']) - getAmount(i['returned']) - getAmount(i['interest']))
        else:
            i['balance'] = currencySeparator(getAmount(i['disbursed']) - getAmount(i['utilized']) - getAmount(i['returned']) - getAmount(i['interest']))
            
        openBalance = i['balance']
        i['lastUpdate'] = getRecentDate(dateList)
        
    # disbursement
    fund = []
    toast = []
    ErrorForm = -1
    scheme_Obj = Schemes.objects.get(schemeName = name)
    fundDisbursement = FundDisbursement.objects.filter(scheme = name) 
    openBalance = getOpeningBalance(fundDisbursement.values().order_by('-disbursedOn'),FundLog.objects.filter( schemeName = name).values().order_by('-id'),['closingBalance','sanctionedAmt'])
    print(openBalance)
    if request.POST:
        if 'addDisbursement' in request.POST:
            disbursedForm = DisbursementForm(request.POST)
            if disbursedForm.is_valid():
                disbursedForm = disbursedForm.save(commit=False)
                disbursedForm.scheme = scheme_Obj
                disbursedForm.save()
                toast = ["success","Fund Disbursement was added Successfully."]
                disbursedForm = DisbursementForm(initial = {"openingBalance":openBalance,})
            
            else:
                ErrorForm = 1
    openBalance = getOpeningBalance(fundDisbursement.values().order_by('-disbursedOn'),FundLog.objects.filter(schemeName = name).values().order_by('-id'),['closingBalance','sanctionedAmt'])
    disbursedForm = DisbursementForm(initial = {"openingBalance":openBalance,})
            
    disbursements = fundDisbursement.values()
    for i in disbursements:
        i['total'] = currencySeparator(getAmount(i['prototypeGrant']) + getAmount(i['operationExpenditure']) + getAmount(i['fabLab']))

    # sanction table
    fund = fund + aggregate_Amount(disbursements,['prototypeGrant','operationExpenditure','fabLab'])
    fund.append(getSum(fund))
    fund.append(is_Empty(FundLog.objects.filter(schemeName = name).values('sanctionedAmt'),'sanctionedAmt'))


# utilization
    fund1 = []
    ErrorForm = -1
    fundUtilization = FundUtilization.objects.filter(scheme = name).values()
    scheme_Obj = Schemes.objects.get(schemeName = name)
    fundDisbursement = FundDisbursement.objects.filter(scheme_id = name).values()
    
    openBalance = getAmount(aggregate_Amount(fundUtilization,['prototypeGrant']))
    openBalance += getAmount(fund[1]) + getAmount(fund[2])
    if getAmount(openBalance) < getAmount(fund[3]):
        openBalance = currencySeparator(getAmount(fund[3]) - openBalance)
        
    # from and to date:
    try:
        fromDate = fundUtilization.order_by('-toDate')[0]['toDate'] + timedelta(days=1)
    except:
        fromDate = fundDisbursement.values('disbursedOn')[0]['disbursedOn']
    toDate = datetime.date.today()
    # prototype grant amount
    project = Project.objects.filter(scheme_id = name).values('id')
    amount = Installment.objects.filter(project__in = project,disbursedOn__range = [fromDate,toDate]).values('disbursedAmt')
    amount = aggregate_Amount(amount,['disbursedAmt'])
    
    utilizedForm = UtilizatedForm(initial = {
        "openingBalance":openBalance,
        "fromDate":fromDate,
        "toDate":toDate,
        "prototypeGrant":amount[0],
        "closingBalance": currencySeparator(getAmount(openBalance) - getAmount(amount[0]))
    })
    if request.POST:
        if 'addUtilization' in request.POST:
            utilizedForm = UtilizatedForm(request.POST)
            if utilizedForm.is_valid():
                utilizedForm = utilizedForm.save(commit=False)
                utilizedForm.financialYear = FinancialYear.objects.get(financialYear = years)
                utilizedForm.scheme = scheme_Obj
                utilizedForm.save()
                toast = ["success","Fund Utilization was added Successfully."]
                utilizedForm = UtilizatedForm(initial = {"openingBalance":openBalance,})
            
            else:
                ErrorForm = 1
            
    utilization = fundUtilization
    openBal = closeBal = 0
    for i in utilization:
        i['total'] = currencySeparator(
            getAmount(i['prototypeGrant']) + 
            getAmount(i['operationExpenditure']) + 
            getAmount(i['fabLab']) 
        )
        if openBal < getAmount(i['openingBalance']):
            i['addingBalance'] = currencySeparator(getAmount(i['openingBalance']) - openBal)
            i['openingBalance'] = currencySeparator(openBal)
        else:
            i['addingBalance'] = 0
            
        openBal = getAmount(i['closingBalance'])
        print(openBal,getAmount(i['openingBalance']))
    # sanction table
    fund1 = fund1 + aggregate_Amount(utilization,['prototypeGrant'])
    fund1 = fund1 + aggregate_Amount(fundDisbursement,['operationExpenditure','fabLab'])
    fund1 = fund1 + aggregate_Amount(utilization,['interestAmt' , 'returnedAmt'])
    fund1.append(getSum(fund1))
    fund1.append(is_Empty(FundLog.objects.filter(schemeName = name).values('sanctionedAmt'),'sanctionedAmt'))
    
    # return render(request, 'fund_Utilization.html', {
    #     "schemeName":name,
    #     "year":years,
    #     "toast":toast,
    #     "ErrorForm":ErrorForm,
    # })
    return render(request, 'scheme.html', {
        "fund1":fund1,
        "utilizations":utilization,
        "utilizedForm":utilizedForm,
        "fund":fund,
        "disbursements":disbursements,
        "disbursedForm":disbursedForm,
        "toast":toast,
        "ErrorForm":ErrorForm,
        "years":years,
        "schemeName":name,
        "pagination":pagination_list,
        "active_page":pagination,
    })
@login_required(login_url='/login/')
def scheme1(request,name,pagination):
            
    years = FinancialYear.objects.all().order_by('-financialYear').values()
    pagination_list = [i for i in range(1,(len(years)//10)+2)]
    if pagination == 1:
        years = years[:10]
    else:
        start = (pagination-1) * 10
        years = years[start:start+10]
        
    for i in years:
        dateList = []
        i['sanctioned'] = is_Empty(FundLog.objects.filter(financialYear = i['financialYear'], schemeName = name).values('sanctionedAmt'),'sanctionedAmt')
        i['total'] = Project.objects.filter(financialYear_id = i['financialYear'], scheme_id = name).values('incubatee').distinct().count()
        fundDisbursement = FundDisbursement.objects.filter(scheme_id = name,financialYear_id = i['financialYear']).values()
        fundUtilization = FundUtilization.objects.filter(scheme_id = name,financialYear_id = i['financialYear']).values()
        try:            
            dateList.append(fundUtilization.order_by('-updateOn').values('updateOn')[0]['updateOn'])
        except:
            try:
                dateList.append(fundDisbursement.order_by('-updateOn').values('updateOn')[0]['updateOn'])
            except:
                pass
        funds = aggregate_Amount(fundDisbursement,['prototypeGrant','operationExpenditure','fabLab'])
        i['disbursed'] = currencySeparator(sum([ getAmount(j) for j in funds ]))
        funds = aggregate_Amount(fundUtilization,['prototypeGrant','operationExpenditure','fabLab'])
        i['utilized'] = currencySeparator(sum([ getAmount(j) for j in funds ]))
        i['returned'] = currencySeparator(sum([ getAmount(j) for j in aggregate_Amount(fundUtilization,['returnedAmt']) ]))
        i['interest'] = currencySeparator(sum([ getAmount(j) for j in aggregate_Amount(fundUtilization,['interestAmt']) ]))
        i['balance'] = currencySeparator(getAmount(i['disbursed']) - getAmount(i['utilized']) - getAmount(i['returned']) - getAmount(i['interest']))
        i['lastUpdate'] = getRecentDate(dateList)
    return render(request, 'fundflow_schemes.html', {
        "years":years,
        "schemeName":name,
        "pagination":pagination_list,
        "active_page":pagination,
    })
#Fund Flow Analysis - Disbursement 
@login_required(login_url='/login/')
def disbursement_Analysis(request,name,pagination = 1):        
    years = list(FinancialYear.objects.all().order_by('financialYear').values())
    pagination_list = [i for i in range(1,(len(years)//8)+2)]
        
    opening = 0
    for i in years:
        fundDisbursement = FundDisbursement.objects.filter(financialYear = i['financialYear'],scheme = name).values() 
        fund = aggregate_Amount(fundDisbursement,['prototypeGrant','operationExpenditure','fabLab'])
        
        i['opening'] = opening
        i['sanctioned'] = is_Empty(FundLog.objects.filter(financialYear = i['financialYear'], schemeName = name).values('sanctionedAmt'),'sanctionedAmt')
        i['pg'] = fund[0]
        i['oe'] = fund[1]
        i['fab'] = fund[2]
        i['total'] = getSum(fund)
        i['closing'] = currencySeparator(getAmount(i['opening']) + getAmount(i['sanctioned']) - getAmount(i['total']))
        opening = i['closing']
        
    years = sorted(years, key= lambda i:i['financialYear'],reverse=True)
    
    if pagination == 1:
        years = years[:8]
    else:
        start = (pagination-1) * 8
        years = years[start:start+8]
    
    return render(request, 'disbursement_Analysis.html', {
        "years":years,
        "schemeName":name,
        "pagination":pagination_list,
        "active_page":pagination,
    })
@login_required(login_url='/login/')
def utilization_Analysis(request,name,pagination = 1):        
    years = list(FinancialYear.objects.all().order_by('financialYear').values())
    pagination_list = [i for i in range(1,(len(years)//8)+2)]
        
    opening = 0
    for i in years:
        fundUtilization = FundUtilization.objects.filter(financialYear = i['financialYear'],scheme = name).values() 
        fund = aggregate_Amount(fundUtilization,['prototypeGrant','operationExpenditure','fabLab','returnedAmt','interestAmt'])
        
        i['opening'] = opening
        i['sanctioned'] = is_Empty(FundLog.objects.filter(financialYear = i['financialYear'], schemeName = name).values('sanctionedAmt'),'sanctionedAmt')
        i['pg'] = fund[0]
        i['oe'] = fund[1]
        i['fab'] = fund[2]
        i['returned'] = fund[3]
        i['interest'] = fund[4]
        i['total'] = getSum(fund)
        i['closing'] = currencySeparator(getAmount(i['opening']) + getAmount(i['sanctioned']) - getAmount(i['total']))
        opening = i['closing']
        
    years = sorted(years, key= lambda i:i['financialYear'],reverse=True)
    
    if pagination == 1:
        years = years[:8]
    else:
        start = (pagination-1) * 8
        years = years[start:start+8]
    
    return render(request, 'utilization_Analysis.html', {
        "years":years,
        "schemeName":name,
        "pagination":pagination_list,
        "active_page":pagination,
    })
#Fund Flow Disbursement 
@login_required(login_url='/login/')
def fund_Disbursement(request,name,years=None):
    fund = []
    toast = []
    ErrorForm = -1
    scheme_Obj = Schemes.objects.get(schemeName = name)
    fundDisbursement = FundDisbursement.objects.filter(financialYear = years,scheme = name) 
    openBalance = getOpeningBalance(fundDisbursement.values(),FundLog.objects.filter(financialYear = years, schemeName = name).values().order_by('-id'),['closingBalance','sanctionedAmt'])
    if request.POST:
        if 'addDisbursement' in request.POST:
            disbursedForm = DisbursementForm(request.POST)
            if disbursedForm.is_valid():
                disbursedForm = disbursedForm.save(commit=False)
                disbursedForm.scheme = scheme_Obj
                disbursedForm.save()
                toast = ["success","Fund Disbursement was added Successfully."]
                disbursedForm = DisbursementForm(initial = {"openingBalance":openBalance,})
            
            else:
                ErrorForm = 1
    openBalance = getOpeningBalance(fundDisbursement.values(),FundLog.objects.filter(financialYear = years, schemeName = name).values().order_by('-id'),['closingBalance','sanctionedAmt'])
    disbursedForm = DisbursementForm(initial = {"openingBalance":openBalance,})
            
    disbursements = fundDisbursement.values()
    for i in disbursements:
        i['total'] = currencySeparator(getAmount(i['prototypeGrant']) + getAmount(i['operationExpenditure']) + getAmount(i['fabLab']))

    # sanction table
    fund.append(years)
    fund = fund + aggregate_Amount(disbursements,['prototypeGrant','operationExpenditure','fabLab'])
    fund.append(getSum(fund[1:]))
    fund.append(is_Empty(FundLog.objects.filter(financialYear = years, schemeName = name).values('sanctionedAmt'),'sanctionedAmt'))
    
    return render(request, 'fund_Disbursement.html', {
        "fund":fund,
        "schemeName":name,
        "year":years,
        "disbursements":disbursements,
        "disbursedForm":disbursedForm,
        "toast":toast,
        "ErrorForm":ErrorForm,
    })
#Fund Flow Disbursement 
@login_required(login_url='/login/')
def fund_Utilization(request,name,years=None):
    fund = []
    toast = []
    ErrorForm = -1
    fundUtilization = FundUtilization.objects.filter(scheme = name).values()
    scheme_Obj = Schemes.objects.get(schemeName = name)
    fundDisbursement = FundDisbursement.objects.filter( scheme_id = name).values()
    openBalance = getAmount(FundLog.objects.filter( schemeName = name).values()[0]['sanctionedAmt']) - getAmount(fundDisbursement.order_by('-id')[0]['closingBalance'])
    openBalance = currencySeparator(getOpeningBalance(fundUtilization,[{"closingBalance":openBalance}],['closingBalance','closingBalance']))
    
    # from and to date:
    try:
        fromDate = fundUtilization.order_by('-toDate')[0]['toDate'] - timedelta(days=1)
    except:
        fromDate = fundDisbursement.values('disbursedOn')[0]['disbursedOn']
    toDate = datetime.date.today()
    # prototype grant amount
    project = Project.objects.filter(scheme_id = name).values('id')
    amount = Installment.objects.filter(project__in = project,disbursedOn__range = [fromDate,toDate]).values('disbursedAmt')
    amount = aggregate_Amount(amount,['disbursedAmt'])
    
    utilizedForm = UtilizatedForm(initial = {
        "openingBalance":openBalance,
        "fromDate":fromDate,
        "toDate":toDate,
        "prototypeGrant":amount[0],
        "closingBalance": currencySeparator(getAmount(openBalance) - getAmount(amount[0]))
    })
    if request.POST:
        if 'addUtilization' in request.POST:
            utilizedForm = UtilizatedForm(request.POST)
            if utilizedForm.is_valid():
                utilizedForm = utilizedForm.save(commit=False)
                utilizedForm.scheme = scheme_Obj
                utilizedForm.save()
                toast = ["success","Fund Utilization was added Successfully."]
                utilizedForm = UtilizatedForm(initial = {"openingBalance":openBalance,})
            
            else:
                ErrorForm = 1
            
    utilization = fundUtilization
    for i in utilization:
        i['total'] = currencySeparator(
            getAmount(i['prototypeGrant']) + 
            getAmount(i['operationExpenditure']) + 
            getAmount(i['fabLab']) + 
            getAmount(i['returnedAmt']) + 
            getAmount(i['interestAmt'])
        )

    # sanction table
    fund = fund + aggregate_Amount(utilization,['prototypeGrant','operationExpenditure','fabLab', 'interestAmt' , 'returnedAmt'])
    fund.append(getSum(fund))
    fund.append(is_Empty(FundLog.objects.filter(schemeName = name).values('sanctionedAmt'),'sanctionedAmt'))
    
    return render(request, 'fund_Utilization.html', {
        "fund":fund,
        "schemeName":name,
        "year":years,
        "utilizations":utilization,
        "utilizedForm":utilizedForm,
        "toast":toast,
        "ErrorForm":ErrorForm,
    })

# incubatees
@login_required(login_url='/login/')
def incubatees(request,pagination = 1):
    incubateeForm = IncubateeForm()
    companyForm = CompanyForm()
    projectForm = ProjectForm()
    Error = False
    success = False
    schemes_excluded = [ i['schemeName'] for i in Schemes.objects.all().values()]
    financialYears_excluded = [ i['financialYear'] for i in FinancialYear.objects.all().values()]
    
    if request.method == 'POST':
        if 'financialYears' in request.POST:
            for i in request.POST.getlist('financialYears'):
                if i in financialYears_excluded:
                    financialYears_excluded.remove(i)
        if 'schemes' in request.POST:
            for i in request.POST.getlist('schemes'):
                if i in schemes_excluded:
                    schemes_excluded.remove(i)
        if 'addIncubatee' in request.POST:
            incubateeForm = IncubateeForm(request.POST,request.FILES)
            companyForm = CompanyForm(request.POST,request.FILES)
            projectForm = ProjectForm(request.POST,request.FILES)
            valid = 0
            if incubateeForm.is_valid():
                valid = 1
            if companyForm.is_valid():
                valid += 1
            if projectForm.is_valid():
                valid += 1
            if valid == 3:
                id = "TBI@" + str(datetime.date.today().year) + f"{Incubatee.objects.all().count()+1:03d}"
                if incubateeForm.is_valid():
                    incubateeForm = incubateeForm.save(commit=False)
                    incubateeForm.incubatee_ID = id
                    try:
                        incubateeForm.financialYear = FinancialYear.objects.get(financialYear = str(datetime.date.today().year)+"-"+str(datetime.date.today().year+1))
                    except:
                        incubateeForm.financialYear = FinancialYear.objects.get(financialYear = str(datetime.date.today().year-1)+"-"+str(datetime.date.today().year))
                    incubateeForm.save()
                if companyForm.is_valid():
                    companyForm = companyForm.save(commit=False)
                    companyForm.incubatee_ID = Incubatee.objects.get(incubatee_ID = id)
                    companyForm.save()
                if projectForm.is_valid():
                    projectForm = projectForm.save(commit=False)
                    projectForm.incubatee = Incubatee.objects.get(incubatee_ID = id)
                    try:
                        projectForm.save()
                    except:
                        valid = 2
                        Company.objects.get(incubatee_ID = id).delete()
                        Incubatee.objects.get(incubatee_ID = id).delete()
                if valid == 3:
                    incubateeForm = IncubateeForm()
                    companyForm = CompanyForm()
                    projectForm = ProjectForm()
                    success = True
                else:
                    incubateeForm = IncubateeForm(request.POST,request.FILES)
                    companyForm = CompanyForm(request.POST,request.FILES)
                    projectForm = ProjectForm(request.POST)
                    projectForm.add_error('scheme','The selected scheme has No Fund / Not Active.')
                    Error = True
                    
            else:
                Error = True
        incubatees = Incubatee.objects.all().values()
        if len(request.POST.getlist('financialYears')) >= 1:
            incubatees = incubatees.values().exclude(financialYear__in = financialYears_excluded)
            # incubatee_list = [j['incubatee'] for j in Project.objects.exclude(scheme__in = schemes_excluded).values('incubatee')]
            # incubatees = incubatees.filter(incubatee_ID__in = incubatee_list)
            
        if len(request.POST.getlist('schemes')) >= 1:
            incubatee_list = [j['incubatee'] for j in Project.objects.exclude(scheme__in = schemes_excluded).values('incubatee')]
            incubatees = incubatees.values().filter(incubatee_ID__in = incubatee_list)           
        # else:
            # incubatees = Incubatee.objects.all().values().filter(financialYear__in = financialYears_excluded)
            
    else:
        incubatees = Incubatee.objects.all().values().filter(financialYear__in = financialYears_excluded)
        
    for i in incubatees:
        project = Project.objects.filter(incubatee = i['incubatee_ID'])
        company = Company.objects.filter(incubatee_ID = i['incubatee_ID'])
        i['company'] = company.values()
        i['project'] = project.values()
        i['schemes'] = project.values('scheme').distinct().count()
        dateList = []
        dateList.append(i['updateOn'])
        for j in project.values():
            dateList.append(j['updateOn'])
        dateList.append(company.values()[0]['updateOn'])
        dateList.append(i['updateOn'])
        i['last_update'] = getRecentDate(dateList)
        
    pagination_list = [i for i in range(1,(len(incubatees)//8)+2)]
    if pagination == 1:
        incubatees = incubatees[:8]
    else:
        start = (pagination-1) * 8
        incubatees = incubatees[start:start+8]   
        
    
    schemes = [ i['schemeName'] for i in Schemes.objects.all().values()]
    financialYears = [ i['financialYear'] for i in FinancialYear.objects.all().values()]
    return render(request, 'incubatees.html', {
        "schemes":schemes,
        "financialYears":financialYears,
        "active_schemes":schemes_excluded,
        "active_financialYears":financialYears_excluded,
        "incubateeForm":incubateeForm,
        "projectForm":projectForm,
        "companyForm":companyForm,
        "Error":Error,
        "success":success,
        "incubatees":incubatees,
        "pagination_list":pagination_list,
        "active_page":pagination,
    })
      
      
def incubateeData(incubateeID,page,success=None,project_ID=None):
    incubatee = Incubatee.objects.get(incubatee_ID = incubateeID)
    company = Company.objects.filter(incubatee_ID = incubateeID).values()[0]
    projects = Project.objects.filter(incubatee = incubateeID).values()
    members = IncubateeTeam.objects.filter(incubatee_ID = incubateeID).values()
    installment = Installment.objects.filter(project_id = project_ID).values()
    patent = Patents.objects.filter(project_id = project_ID).values()
    copyright = Copyright.objects.filter(project_id = project_ID).values()
    trademark = Trademark.objects.filter(project_id = project_ID).values()
    
    revenue = ProjectRevenue.objects.filter(project_id = project_ID).values()
    employment = ProjectEmployment.objects.filter(project_id = project_ID).values()
    awards = ProjectAwards.objects.filter(project_id = project_ID).values()
    intern = ProjectIntern.objects.filter(project_id = project_ID).values()
    product = ProjectProduct.objects.filter(project_id = project_ID).values()
    if project_ID != None:
        project = Project.objects.get(id = project_ID)
    else:
        project = None
    return {
        "incubateeID":incubateeID,
        "page":page,
        "projectID":project_ID,
        "success":success,
        # data
        "installments":installment,
        "patents":patent,
        "copyrights":copyright,
        "trademarks":trademark,
        "incubatee":incubatee,
        "company":company,
        "members":members,
        "projects":projects,
        "selectedProject":project,    
        "revenue":revenue,    
        "employment":employment,    
        "awards":awards,    
        "intern":intern,    
        "product":product,    
    }
    

# incubatees
@login_required(login_url='/login/')
def incubatee(request,incubateeID,page,form=None,success=None,formType = None,project = None):
    selectedProject = None
    project_ID = None
    if request.method == "POST":
        if "title" in request.POST:
            selectedProject = Project.objects.filter(incubatee = incubateeID,title = request.POST['title']).values()[0]
            project_ID = selectedProject['id']
    result = incubateeData(incubateeID = incubateeID,page = page,project_ID=project_ID)
    result = initialize_Forms(result,"")
    result['project_active'] = "overview"
    return render(request, 'incubatee_profile.html', result)

# team
@login_required(login_url='/login/')
def addMember(request,incubateeID):
    success = False
    form = TeamForm()
    if request.method == 'POST':
        form = TeamForm(request.POST,request.FILES)
        # form = form.is_valid()
        if form.is_valid():
            try:
                form = form.save(commit=False)
                form.incubatee_ID = Incubatee.objects.get(incubatee_ID = incubateeID)
                form.save()
                form = TeamForm()
                success = "Team Created"
            except:
                form = TeamForm(request.POST,request.FILES)
                form.add_error('aadhaar',"Same aadhaar was already added as a member with this Incubatee.")
                form.add_error('pan',"Same pan was already added as a member with this Incubatee.")
                success = "TeamError"
    
    result = incubateeData(incubateeID = incubateeID,page = "team",)
    result = initialize_Forms(result,"teamForm")
    result['teamForm'] = form
    result['success'] = success
    result['project_active'] = "installment"
    return render(request, 'incubatee_profile.html', result)

# project
@login_required(login_url='/login/')
def addProject(request,incubateeID):
    success = False
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                form = form.save(commit=False)
                form.incubatee = Incubatee.objects.get(incubatee_ID = incubateeID)
                form.save()
                form = ProjectForm()
                success = "Project Created"
            except IntegrityError as e:
                form = ProjectForm(request.POST,request.FILES)
                form.add_error('scheme',"Already this scheme was added to this Incubatee")
                success = "addProject"
            except Exception as e:
                print("----------")
                form = ProjectForm(request.POST,request.FILES)
                form.add_error('scheme',str(e))
                success = "addProject"
                
    result = incubateeData(incubateeID = incubateeID,page = "project",)
    result = initialize_Forms(result,"projectForm")
    result['projectForm'] = form
    result['success'] = success
    return render(request, 'incubatee_profile.html', result)
    
    
# installment
@login_required(login_url='/login/')
def addInstallment(request,incubateeID,project_ID):
    success = False
    form = InstallmentForm()
    if request.method == 'POST':
        form = InstallmentForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                form = form.save(commit=False)
                form.project = Project.objects.get(id = project_ID)
                form.save()
                form = InstallmentForm()
                success = "Installment Added"
            except:
                form = InstallmentForm(request.POST,request.FILES)
                success = "addInstallment"
    result = incubateeData(incubateeID = incubateeID,page = "project",project_ID=project_ID)
    result = initialize_Forms(result,"installmentForm")
    result['installmentForm'] = form
    result['success'] = success
    result['project_active'] = "installment"
    return render(request, 'incubatee_profile.html', result)
    
# installment
@login_required(login_url='/login/')
def editInstallment(request,incubateeID,project_ID):
    success = False
    form = InstallmentForm()
    if request.method == 'POST':
        installment = Installment.objects.get(id = request.POST['addInstallment'])
        success = "Installment Updated"
        form = InstallmentForm(request.POST,request.FILES, instance = installment)
        if form.is_valid():
            try:
                form.save()
                form = InstallmentForm()
            except:
                success = 1
                success = "addInstallment"
    result = incubateeData(incubateeID = incubateeID,page = "project",project_ID=project_ID)
    result = initialize_Forms(result,"installmentForm")
    result['installmentForm'] = form
    result['success'] = success
    result['project_active'] = "installment"
    return render(request, 'incubatee_profile.html', result)
    
# patent
@login_required(login_url='/login/')
def addPatent(request,incubateeID,project_ID):
    success = False
    form = PatentForm()
    if request.method == 'POST':
        form = PatentForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                form = form.save(commit=False)
                form.project = Project.objects.get(id = project_ID)
                form.save()
                form = PatentForm()
                success = "Patent Added"
            except:
                form = PatentForm(request.POST,request.FILES)
                success = 1
    result = incubateeData(incubateeID = incubateeID,page = "project",project_ID=project_ID)
    result = initialize_Forms(result,"patentForm")
    result['patentForm'] = form
    result['success'] = success
    result['project_active'] = "ip"
    return render(request, 'incubatee_profile.html', result)
    
# patent
@login_required(login_url='/login/')
def addCopyright(request,incubateeID,project_ID):
    success = False
    form = CopyrightForm()
    if request.method == 'POST':
        form = CopyrightForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                form = form.save(commit=False)
                form.project = Project.objects.get(id = project_ID)
                form.save()
                form = CopyrightForm()
                success = "Copyright Added"
            except:
                form = CopyrightForm(request.POST,request.FILES)
                success = 1
    result = incubateeData(incubateeID = incubateeID,page = "project",project_ID=project_ID)
    result = initialize_Forms(result,"copyrightForm")
    result['copyrightForm'] = form
    result['success'] = success
    result['project_active'] = "ip"
    return render(request, 'incubatee_profile.html', result)
    
# patent
@login_required(login_url='/login/')
def addTrademark(request,incubateeID,project_ID):
    success = False
    form = TrademarkForm()
    if request.method == 'POST':
        form = TrademarkForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                form = form.save(commit=False)
                form.project = Project.objects.get(id = project_ID)
                form.save()
                form = TrademarkForm()
                success = "Trademark Added"
            except:
                form = TrademarkForm(request.POST,request.FILES)
                success = 1
    result = incubateeData(incubateeID = incubateeID,page = "project",project_ID=project_ID)
    result = initialize_Forms(result,"trademarkForm")
    result['trademarkForm'] = form
    result['success'] = success
    result['project_active'] = "ip"
    return render(request, 'incubatee_profile.html', result)
       
#impact        
@login_required(login_url='/login/')
def addRevenue(request,incubateeID,project_ID):
    success = False
    form = ProjectRevenueForm()
    if request.method == 'POST':
        form = ProjectRevenueForm(request.POST,request.FILES)
        if form.is_valid():
            project = Project.objects.get(id = project_ID)
            form = form.save(commit=False)
            print(form)
            if ProjectRevenue.objects.filter(financialYear=form.financialYear, project=project).exists():
                ProjectRevenue.objects.filter(
                    financialYear=form.financialYear, 
                    project_id=project
                ).update(revenue=form.revenue)
                success = 'Revenue Updated'
            else:
                form.project = project
                form.save()
                success = 'Revenue Added'            
            form = ProjectRevenueForm()
    result = incubateeData(incubateeID = incubateeID,page = "project",project_ID=project_ID)
    result = initialize_Forms(result,"revenueForm")
    result['revenueForm'] = form
    result['success'] = success
    result['project_active'] = "impact"
    result['impact_active'] = "revenue"
    return render(request, 'incubatee_profile.html', result)
        
#impact        
@login_required(login_url='/login/')
def addEmployment(request,incubateeID,project_ID):
    success = False
    form = ProjectEmploymentForm()
    if request.method == 'POST':
        form = ProjectEmploymentForm(request.POST,request.FILES)
        if form.is_valid():
            project = Project.objects.get(id = project_ID)
            form = form.save(commit=False)
            if ProjectEmployment.objects.filter(date=form.date, project=project).exists():
                ProjectEmployment.objects.filter(
                    date=form.date, 
                    project_id=project
                ).update(employment=form.employment)
                success = 'Employment Updated'
            else:
                form.project = project
                form.save()
                success = 'Employment Added'            
            form = ProjectEmploymentForm()
    result = incubateeData(incubateeID = incubateeID,page = "project",project_ID=project_ID)
    result = initialize_Forms(result,"employmentForm")
    result['employmentForm'] = form
    result['success'] = success
    result['project_active'] = "impact"
    result['impact_active'] = "employment"
    return render(request, 'incubatee_profile.html', result)
        
#impact        
@login_required(login_url='/login/')
def addAwards(request,incubateeID,project_ID):
    success = False
    form = ProjectAwardsForm()
    if request.method == 'POST':
        form = ProjectAwardsForm(request.POST,request.FILES)
        if form.is_valid():
            project = Project.objects.get(id = project_ID)
            form = form.save(commit=False)
            if ProjectAwards.objects.filter(
                financialYear=form.financialYear, 
                project=project,
                date = form.date,
                eventName = form.eventName,
                awardTitle = form.awardTitle
            ).exists():
                ProjectAwards.objects.filter(
                    financialYear=form.financialYear, 
                    project=project,
                    date = form.date,
                    eventName = form.eventName,
                    awardTitle = form.awardTitle
                ).update(amount=form.amount, certificate = form.certificate, photo = form.photo)
                success = 'Award Updated'
            else:
                form.project = project
                form.save()
                success = 'Award Added'            
            form = ProjectAwardsForm()
    result = incubateeData(incubateeID = incubateeID,page = "project",project_ID=project_ID)
    result = initialize_Forms(result,"awardsForm")
    result['awardsForm'] = form
    result['success'] = success
    result['project_active'] = "impact"
    result['impact_active'] = "awards"
    return render(request, 'incubatee_profile.html', result)
        
#impact        
@login_required(login_url='/login/')
def addIntern(request,incubateeID,project_ID):
    success = False
    form = ProjectInternForm()
    if request.method == 'POST':
        form = ProjectInternForm(request.POST,request.FILES)
        if form.is_valid():
            project = Project.objects.get(id = project_ID)
            form = form.save(commit=False)
            if ProjectIntern.objects.filter(financialYear=form.financialYear, project=project,rollno= form.rollno).exists():
                ProjectIntern.objects.filter(
                    financialYear=form.financialYear, 
                    project=project,
                    rollno= form.rollno
                ).update(
                    fromdate=form.fromdate,
                    name = form.name,
                    Department = form.Department,
                    title = form.title,
                    todate = form.todate,
                    stipend = form.stipend,
                    amount = form.amount,
                    certificate = form.certificate,
                    )
                success = 'Intern Updated'
            else:
                form.project = project
                form.save()
                success = 'Intern Added'            
            form = ProjectInternForm()
    result = incubateeData(incubateeID = incubateeID,page = "project",project_ID=project_ID)
    result = initialize_Forms(result,"internForm")
    result['internForm'] = form
    result['success'] = success
    result['project_active'] = "impact"
    result['impact_active'] = "intern"
    return render(request, 'incubatee_profile.html', result)
        
#impact        
@login_required(login_url='/login/')
def addProduct(request,incubateeID,project_ID):
    success = False
    form = ProjectProductForm()
    if request.method == 'POST':
        form = ProjectProductForm(request.POST,request.FILES)
        if form.is_valid():
            project = Project.objects.get(id = project_ID)
            form = form.save(commit=False)
            if ProjectProduct.objects.filter(
                financialYear=form.financialYear, 
                project=project,
                product_name = form.product_name
            ).exists():
                ProjectProduct.objects.filter(
                    financialYear=form.financialYear, 
                    project=project,
                    product_name = form.product_name
                ).update(
                    product_image=form.product_image,
                    units_sold= form.units_sold,
                    launchDate = form.launchDate
                )
                success = 'Product Updated'
            else:
                form.project = project
                form.save()
                success = 'Product Added'            
            form = ProjectRevenueForm()
    result = incubateeData(incubateeID = incubateeID,page = "project",project_ID=project_ID)
    result = initialize_Forms(result,"productForm")
    result['productForm'] = form
    result['success'] = success
    result['project_active'] = "impact"
    result['impact_active'] = "product"
    return render(request, 'incubatee_profile.html', result)
        
        
        
        
        
        
# patent
@login_required(login_url='/login/')
def editIncubatee(request,incubateeID):
    success = 1
    form = IncubateeForm(instance = Incubatee.objects.get(incubatee_ID = incubateeID))
    form1 = CompanyEditForm(instance = Company.objects.get(incubatee_ID = incubateeID))
    if request.method == 'POST':
        form = IncubateeForm(request.POST,request.FILES,instance = Incubatee.objects.get(incubatee_ID = incubateeID))
        form1 = CompanyEditForm(request.POST,request.FILES,instance = Company.objects.get(incubatee_ID = incubateeID))
        if form.is_valid():
            try:
                form.save()
                form = IncubateeForm()
                success += 1
            except:
                success = 1
        if form1.is_valid():
            try:
                form1.save(commit= False)
                if form1.startupFormed == "Yes":
                    form1.startupFormedDate = datetime.date.today()
                form1.save()
                form1 = CompanyEditForm()
                success += 1
            except:
                success = 1
        if success == 3:
            result = incubateeData(incubateeID = incubateeID,page = 'company',project_ID=None)
            result = initialize_Forms(result,"")
            result['project_active'] = "overview"
            return render(request, 'incubatee_profile.html', result)
            
    return render(request, 'incubatee_profileEdit.html', {"form":form,"form1":form1,"incubateeID":incubateeID})

# patent
@login_required(login_url='/login/')
def editIncubateeProject(request,incubateeID,project_ID):
    success = 1
    form = ProjectEditForm(instance = Project.objects.get(id = project_ID))
    if request.method == 'POST':
        form = ProjectEditForm(request.POST,request.FILES,instance = Project.objects.get(id = project_ID))
        if form.is_valid():
            try:
                form.save()
                form = ProjectEditForm()
                success += 1
            except:
                success = 1
        if success == 2:
            result = incubateeData(incubateeID = incubateeID,page = 'company',project_ID=None)
            result = initialize_Forms(result,"")
            result['project_active'] = "overview"
            return render(request, 'incubatee_profile.html', result)
    print(project_ID)
    return render(request, 'incubatee_companyEdit.html', {"form":form,"incubateeID":incubateeID,"project_ID":project_ID})

        
# incubatee
@login_required(login_url='/login/')
def editPatent(request,incubateeID,project_ID):
    success = False
    form = PatentForm()
    if request.method == 'POST':
        patent = Patents.objects.get(id = request.POST['addPatent'])
        success = "Patent Updated"
        form = PatentForm(request.POST,request.FILES, instance = patent)
        if form.is_valid():
            try:
                form.save()
                form = PatentForm()
            except:
                success = 1
    result = incubateeData(incubateeID = incubateeID,page = "project",project_ID=project_ID)
    result['teamForm'] = TeamForm()
    result['patentForm'] = ProjectForm()
    result['installmentForm'] = form
    result['success'] = success
    result['project_active'] = "ip"
    return render(request, 'incubatee_profile.html', result)
    
#visitors
@login_required(login_url='/login/')
def reportIncubatee(request):
    report = FinancialYear.objects.all().values().order_by("-financialYear")
    for i in report:
        inc = Incubatee.objects.filter(financialYear_id = i['financialYear'])
        i['community'] = inc.values('community').annotate(communities = Count('community'))
        i['gender'] = inc.values('gender').annotate(genders = Count('gender'))
        i['total'] = inc.count()
        i['sanctionedAmt'] = 0
        for j in Project.objects.all().values():
            if j['amountSanctionedDate'].month > 3:
                if (str(j['amountSanctionedDate'].year) + "-" + str(j['amountSanctionedDate'].year + 1)) == i['financialYear']:
                    i['sanctionedAmt'] += getAmount(j['amount'])
            else:
                if (str(j['amountSanctionedDate'].year - 1) + "-" + str(j['amountSanctionedDate'].year)) == i['financialYear']:
                    i['sanctionedAmt'] += getAmount(j['amount'])
        i['sanctionedAmt'] = currencySeparator(i['sanctionedAmt'])
        i['status'] = Project.objects.filter(incubatee__in = inc).values('status').annotate(statuses = Count('status'))
        total = 0
        for j in Installment.objects.all().values():
            if j['disbursedOn'] > datetime.date((j['disbursedOn']).year,3,31):
                if (str(j['disbursedOn'].year) + "-" + str(j['disbursedOn'].year + 1)) == i['financialYear']:
                    total += getAmount(j['disbursedAmt'])
            else:
                if (str(j['disbursedOn'].year - 1) + "-" + str(j['disbursedOn'].year)) == i['financialYear']:
                    total += getAmount(j['disbursedAmt'])
        i['disbursed'] = currencySeparator(total)
       
    charts = {
        "projectStatus":[
            Project.objects.all().filter(status = "Completed").values('status').count(),
            Project.objects.all().filter(status = "Discontinued").values('status').count(),
            Project.objects.all().filter(status = "In Progress").values('status').count(),
        ],
        "years":[ i['amountSanctionedDate'].strftime("%Y-%m-%dT%H:%M:%S") for i in Project.objects.all().values('amountSanctionedDate').order_by("amountSanctionedDate")],
        "sanctioned":[ getAmount(i['amount']) for i in Project.objects.all().values('amount')],
        "years1":[ i['disbursedOn'] for i in Installment.objects.all().values('disbursedOn')],
        "disbursed":[ getAmount(i['disbursedAmt']) for i in Installment.objects.all().values('disbursedAmt')],
    }    
    return render(request, 'incubateeReport.html', {
        "report":report,
        "charts":charts
    })
    
#visitors
@login_required(login_url='/login/')
def reportAge(request):
    report = FinancialYear.objects.all().values().order_by("-financialYear")
    stepvalue = 5
    fromAge = 0
    toAge = 100
    if request.method == "POST":
        stepvalue =  int(request.POST['step'])
        fromAge =  int(request.POST['startAge'])
        toAge =  int(request.POST['toAge'])
    agerange = {str(i)+"-"+str(i+stepvalue):0 for i in range(fromAge,toAge,stepvalue)}
    for i in report:
        agerange = {str(i)+"-"+str(i+stepvalue):0 for i in range(fromAge,toAge,stepvalue)}
        inc = Incubatee.objects.filter(financialYear_id = i['financialYear'])
        for j in agerange.keys():
            range1 = datetime.datetime.today() - datetime.timedelta(int(j.split('-')[0])*365)
            range2 = datetime.datetime.today() - datetime.timedelta(int(j.split('-')[1])*365)
            agerange[j] = inc.filter(dob__range = [range2,range1]).count()
        incubatee_count = 0
        for j in agerange.keys():
            if agerange[j] != 0:
                i['agerange'] = agerange
                incubatee_count += agerange[j]
        i['total'] = incubatee_count
    agerange1 = {str(i)+"-"+str(i+stepvalue):0 for i in range(fromAge,toAge,stepvalue)}                
    for j in agerange1.keys():
        range1 = datetime.datetime.today() - datetime.timedelta(int(j.split('-')[0])*365)
        range2 = datetime.datetime.today() - datetime.timedelta(int(j.split('-')[1])*365)
        agerange1[j] = Incubatee.objects.filter(dob__range = [range2,range1]).count()
    inc = Incubatee.objects.all().filter(dob__range = [
        datetime.datetime.today() - datetime.timedelta(toAge*365),
        datetime.datetime.today() - datetime.timedelta(fromAge*365)
        ]
    )
    agerange2 = {getAge(i['dob']):i['count'] for i in inc.values('dob').annotate(count = Count('dob'))}
    return render(request, 'ageReport.html', {
        "report":report,
        "range":agerange1,
        "age_range_individual":agerange2,
        "from":fromAge,
        "to":toAge,
        "step":stepvalue,
    })
    
#visitors
@login_required(login_url='/login/')
def reportFund(request):
    report = FinancialYear.objects.all().values().order_by("-financialYear")
    chart = {
        "sanctioned":{},
        "disbursed":{},
        "interest":{},
        "returned":{}
    }
    fromYear =  None
    toYear =  None
    if request.method == "POST":
        fromYear =  int(request.POST['startYear'])
        toYear =  int(request.POST['toYear'])
        years = []
        for i in range(fromYear,toYear):
            try:
                years.append(FinancialYear.objects.get(financialYear = str(i)+"-"+str(i+1)))
            except:
                pass
        report = report.filter(financialYear__in = years)
        
    for i in report:
        i['sanctioned'] = aggregate_Amount(FundLog.objects.filter(financialYear_id = i['financialYear']).values(),["sanctionedAmt"])[0]
        i['disbursed'] = getSum(aggregate_Amount(FundDisbursement.objects.filter(financialYear_id = i['financialYear']).values(),['prototypeGrant','operationExpenditure','fabLab']))
        i['pending'] = currencySeparator(getAmount(i['sanctioned']) - getAmount(i['disbursed']))
        project = Project.objects.filter(financialYear = i['financialYear'])
        i['utilized'] = getSum(aggregate_Amount(Installment.objects.filter(project__in = project).values(),['disbursedAmt']))
        i['balance'] = currencySeparator(getAmount(i['disbursed']) - getAmount(i['utilized']))
        i['returned'] = getSum(aggregate_Amount(FundUtilization.objects.filter(financialYear_id = i['financialYear']).values(),['returnedAmt']))
        i['interest'] = getSum(aggregate_Amount(FundUtilization.objects.filter(financialYear_id = i['financialYear']).values(),['interestAmt']))
        i['incubatees'] = Incubatee.objects.all().filter(financialYear_id = i['financialYear']).count()
    
    def chartAssign(object,value):
        temp = []
        for i in object:
            temp.append(getAmount(i[value])) 
        return temp
    
    chart['sanctioned'] = {"years": [i['financialYear'] for i in report.order_by('-financialYear')],"amount":chartAssign(report,'sanctioned')} 
    chart['disbursed'] = {"years": [i['financialYear'] for i in report.order_by('-financialYear')],"amount":chartAssign(report,'disbursed')} 
    chart['interest'] = {"years": [i['financialYear'] for i in report.order_by('-financialYear')],"amount":chartAssign(report,'interest')} 
    chart['returned'] = {"years": [i['financialYear'] for i in report.order_by('-financialYear')],"amount":chartAssign(report,'returned')} 
    
    return render(request, 'fundReport.html', {
        "report":report,
        "chart":chart,
        "from":fromYear,
        "to":toYear,
    })
    
    
#visitors
@login_required(login_url='/login/')
def reportCompany(request):
    report = FinancialYear.objects.all().values().order_by("-financialYear")
    chart = {
        "sanctioned":{},
        "disbursed":{},
        "interest":{},
        "returned":{}
    }
    fromYear =  None
    toYear =  None
    if request.method == "POST":
        fromYear =  int(request.POST['startYear'])
        toYear =  int(request.POST['toYear'])
        years = []
        for i in range(fromYear,toYear):
            try:
                years.append(FinancialYear.objects.get(financialYear = str(i)+"-"+str(i+1)))
            except:
                pass
        report = report.filter(financialYear__in = years)
        
    for i in report:
        incubatee = Incubatee.objects.filter(financialYear = i['financialYear']).all()
        company = Company.objects.filter(incubatee_ID__in = incubatee)
        i['total'] = company.count()
        temp = company.values('startupFormedDate').exclude(startupFormedDate = None)
        ages = {}
        for j in temp:
            j['age'] = getAge(j['startupFormedDate'])
            try:
                if j['age'] == 0:
                    ages[str(j['age'])+"-"+str(j['age']+2)] += 1
                elif j['age'] % 2 == 1:
                    ages[str(j['age']-1)+"-"+str(j['age']+1)] += 1
                else:
                    ages[str(j['age']-2)+"-"+str(j['age']+2)] += 1                
            except:
                if j['age'] == 0:
                    ages[str(j['age'])+"-"+str(j['age']+2)] = 1
                elif j['age'] % 2 == 1:
                    ages[str(j['age']-1)+"-"+str(j['age']+1)] = 1
                else:
                    ages[str(j['age']-2)+"-"+str(j['age']+2)] = 1
        i['age'] = ages
    # chart
    incubatee = Incubatee.objects.filter(financialYear__in = report).all()
    company = Company.objects.filter(incubatee_ID__in = incubatee)
    temp = company.values('startupFormedDate').exclude(startupFormedDate = None)
    ages = {}
    for j in temp:
        j['age'] = getAge(j['startupFormedDate'])
        try:
            if j['age'] == 0:
                ages[str(j['age'])+"-"+str(j['age']+2)] += 1
            elif j['age'] % 2 == 1:
                ages[str(j['age']-1)+"-"+str(j['age']+1)] += 1
            else:
                ages[str(j['age']-2)+"-"+str(j['age'])] += 1                
        except:
            if j['age'] == 0:
                ages[str(j['age'])+"-"+str(j['age']+2)] = 1
            elif j['age'] % 2 == 1:
                ages[str(j['age']-1)+"-"+str(j['age']+1)] = 1
            else:
                ages[str(j['age']-2)+"-"+str(j['age'])] = 1
    chart = ages
    
    
    return render(request, 'companyReport.html', {
        "report":report,
        "chart":chart,
        "from":fromYear,
        "to":toYear,
    })
    
    
#visitors
@login_required(login_url='/login/')
def reportDomain(request):
    report = FinancialYear.objects.all().values().order_by("-financialYear")
    chart = {}
    fromYear =  None
    toYear =  None
    if request.method == "POST":
        fromYear =  int(request.POST['startYear'])
        toYear =  int(request.POST['toYear'])
        years = []
        for i in range(fromYear,toYear):
            try:
                years.append(FinancialYear.objects.get(financialYear = str(i)+"-"+str(i+1)))
            except:
                pass
        report = report.filter(financialYear__in = years)
        
    for i in report:
        project = Project.objects.filter(financialYear = i['financialYear'])
        i['domains'] = project.values('domain').annotate(count = Count('domain'))
        i['total'] = project.values('incubatee').distinct().count()
    
    chart['column'] = Project.objects.filter(financialYear__in = report).values('domain').distinct().annotate(count = Count('domain'))
    chart['values'] = 0
    
    return render(request, 'domainReport.html', {
        "report":report,
        "chart":chart,
        "from":fromYear,
        "to":toYear,
    })
    
    
#visitors
@login_required(login_url='/login/')
def reportStartup(request):
    report = FinancialYear.objects.all().values().order_by("-financialYear")
    chart = {}
    fromYear =  None
    toYear =  None
    if request.method == "POST":
        fromYear =  int(request.POST['startYear'])
        toYear =  int(request.POST['toYear'])
        years = []
        for i in range(fromYear,toYear):
            try:
                years.append(FinancialYear.objects.get(financialYear = str(i)+"-"+str(i+1)))
            except:
                pass
        report = report.filter(financialYear__in = years)
        
    for i in report:
        incubatee = Incubatee.objects.filter(financialYear = i['financialYear']).all()
        company = Company.objects.filter(incubatee_ID__in = incubatee)
        i['total'] = incubatee.count()
        i['individual'] = company.filter(startupFormed = "No").count()
        i['startupConverted'] = company.filter(startupFormed = "Yes").exclude(startupFormedDate = None).count()
        i['startup'] = company.filter(startupFormed = "Yes",startupFormedDate = None).count()
    
    incubatee = Incubatee.objects.filter(financialYear__in = report).all()
    company = Company.objects.filter(incubatee_ID__in = incubatee)
    chart['individual'] = company.filter(startupFormed = "No").count()
    chart['startup'] = company.filter(startupFormed = "Yes",startupFormedDate = None).count()
    chart['startupConverted'] = company.filter(startupFormed = "Yes").exclude(startupFormedDate = None).count()

    
    
    return render(request, 'startupReport.html', {
        "report":report,
        "chart":chart,
        "from":fromYear,
        "to":toYear,
    })
    
import django
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
import os
from .files import *
from .functions import *


def currencySeparator(value):
    if(value == None):
        return 0
    amt = ''
    try:
        value = str(int(value))
    except:
        value = str(getAmount(value))
    if len(value) > 3:
        temp = len(value)-5
        for i in range(len(value)-4, -1, -1):
            if i == temp:
                amt += value[i] + ','
                temp -= 2
            else:
                amt += value[i]
        amt = amt[::-1] + ',' + value[-3:]
    else:
        amt = str(value)
    return amt[1:] if amt[0] == ',' else amt

@classmethod
def getActiveSchemeList(cls):
    scheme = Schemes.objects.filter(status = True).exclude(amount = '0')
    if scheme is not None:
        return [scheme]
    else:
        return Schemes.objects.filter(status = True).values('schemeName')

# Create your models here.
validators = {
    "minimum": MinValueValidators,
    "maximum": MaxValueValidator(100),
    "text": RegexValidator(
        regex=r'^[a-zA-Z ]*$',
        message='Only alphabetical characters are allowed',
    ),
    "textspecial": RegexValidator(
        regex=r'^[a-zA-Z .,&()]*$',
        message='Only Alphabets, space( ), comma(,), dot(.) are allowed',
    ),
    "Pan": RegexValidator(
        regex=r'^[a-zA-Z0-9]*$',
        message='Only Alphabets and Numbers are allowed',
    ),
    "PhoneNumber": RegexValidator(regex=r'^\+?1?\d{10,10}$', message='Only numbers are allowed'),
    "Number": RegexValidator(regex=r'^[0-9]*$', message='Only numbers are allowed'),
    "numbers": RegexValidator(regex=r'^[0-9,]*$', message='Only numbers are allowed'),
    "Aadhaar": RegexValidator(regex=r'^\+?1?\d{12,12}$', message='Only numbers are allowed'),
    "gender": (
        ('Male', "Male"),
        ('Female', 'Female'),
        ('Others', 'Others')
    ),
    "community": (
        ('General', 'General'),
        ('OBC', 'OBC'),
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('Others', 'Others')
    ),
    "education": (
        ('SSC', 'SSC'),
        ('HSC', 'HSC'),
        ('UG', 'UG'),
        ('PG', 'PG'),
        ('Doctorate', 'Doctorate')
    ),
}


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pc_ID = models.CharField(max_length=30)
    pan = models.CharField(max_length=20)
    approval_on = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

class Schemes(models.Model):
    schemeName = models.CharField(
        max_length=60, 
        primary_key=True,
        validators = [validators['text']],
        verbose_name = "Scheme Name"
    )
    status = models.BooleanField(default=True)
    amount = models.CharField(max_length=20,
        validators = [validators['numbers']],
        verbose_name="Amount",
        default = '0',
    )
    def __str__(self):
        return self.schemeName

    @property
    def fund(self):
        try:
            return int((self.amount).replace(",",""))
        except:
            return 0 


class FundingType(models.Model):
    fundType = models.CharField(
        max_length=60, 
        primary_key=True,
        validators = [validators['text']],
        verbose_name="Fund Type",
    )

    def __str__(self):
        return self.fundType


class ProgramType(models.Model):
    programName = models.CharField(
        max_length=60, 
        primary_key=True,
        validators = [validators['text']],
        verbose_name="Program Type",
    )

    def __str__(self):
        return self.programName

class Entity(models.Model):
    entityName = models.CharField(
        max_length=50, 
        verbose_name='Entity Name',
        primary_key=True,
        validators = [validators['textspecial']],
    )

    def __str__(self):
        return self.entityName

class FinancialYear(models.Model):
    financialYear = models.CharField(
        max_length=12,
        validators=[
            RegexValidator(
                regex='^[0-9-]*$',
                message='Financial Year must be in the format YYYY-YYYY',
                code='invalid_username'
            ),
        ],
        verbose_name='Financial Year',
        primary_key=True,
    )

    def __str__(self):
        return self.financialYear

class Visitors(models.Model):
    date = models.DateField(verbose_name="Date of visit")
    guestName = models.CharField(
        max_length=50, 
        verbose_name="Guest Name",
        validators=[validators['text']],
    )
    name = models.CharField(
        max_length=50, 
        verbose_name="Name of Organisation/ Institute",
        help_text="For Individual, specify Iindividual. Or Others specify that.",
        validators=[validators['text']],        
    )
    count = models.IntegerField(verbose_name="No. of Visitors")
    purpose = models.CharField(max_length=100, verbose_name="Purpose")
    type = models.CharField(
        max_length=50, 
        verbose_name="Visitor Type", 
        choices=(
            ('Individual','Individual'),('Institution','Institution'),('Organization','Organization')
        )
    )
    class Meta:
        unique_together = ("date", "guestName","name")   

    def __str__(self):
        return self.guestName + ' : ' + self.name

class VisitorImages(models.Model):
    visitor = models.ForeignKey(
        Visitors,
        on_delete=models.CASCADE,
    )
    photo = models.ImageField(
        upload_to=visitorPhotos,
    )
    
    def __str__(self):
        return self.visitor.guestName + ' : ' + self.visitor.name
    
class Events(models.Model):
    title = models.CharField(
        max_length=50, 
        verbose_name="Event Name",
        validators=[validators['textspecial']]
    )
    hours = models.IntegerField(
        verbose_name="No. of Hours",
        validators = [validators['minimum']],
    )
    fromdate = models.DateField(verbose_name="Event Start Date")
    todate = models.DateField(verbose_name="Event End Date", null=True, blank=True)
    days = models.IntegerField(
        verbose_name="No. of Days", null=True, blank=True,
        validators = [validators['minimum']],
    )
    inKECstudents = models.IntegerField(
        verbose_name="No. of Students (KEC)",
        validators = [validators['minimum']],
    )
    outstudents = models.IntegerField(
        verbose_name="No. of Students (Other)",
        validators = [validators['minimum']],
    )
    inKECstaffs = models.IntegerField(
        verbose_name="No. of Staffs (KEC)",
        validators = [validators['minimum']],
    )
    outstaffs = models.IntegerField(
        verbose_name="No. of Staffs (Other)",
        validators = [validators['minimum']],
    )
    inKECOrganizaions = models.IntegerField(
        verbose_name="No. of Organizaions (KEC)",
        validators = [validators['minimum']],
    )
    outOrganizaions = models.IntegerField(
        verbose_name="No. of Organizaions (Other)",
        validators = [validators['minimum']],
    )

    class Meta:
        unique_together = ("title", "fromdate","todate")   
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            self.days = (self.todate - self.fromdate).days
        except:
            self.days = 0
        super(Events, self).save(*args, **kwargs)
        
class EventImages(models.Model):
    event = models.ForeignKey(
        Events,
        on_delete=models.CASCADE,
    )
    photo = models.ImageField(
        upload_to=eventPhotos,
    )
    
    def __str__(self):
        return self.event.title

class EventReports(models.Model):
    events = models.ForeignKey(
        Events,
        on_delete=models.CASCADE,
    )
    file = models.FileField(
        upload_to=eventReports,
    )
    
    def __str__(self):
        return self.events.title

class EventSponsors(models.Model):
    eventSponser = models.ForeignKey(Events, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="Sponsor Name")
    amount = models.CharField(max_length=20, verbose_name="Amount")
    
    @property
    def fund(self):
        try:
            return int((self.amount).replace(",",""))
        except:
            return 0 

    def __str__(self):
        return self.eventSponser.title
    

class FundLog(models.Model):
    financialYear = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    schemeName = models.ForeignKey(Schemes, on_delete=models.CASCADE)
    sanctionedAmt = models.CharField(max_length=20,
        validators = [validators['numbers']],
        verbose_name='Sanctioned Amount'
    )
    date = models.DateField(
        verbose_name="Sanctioned Date",
        default=django.utils.timezone.now,
    )
                    
    def __str__(self):
        return self.schemeName.schemeName

    def save(self, *args, **kwargs):
        updateSchemeAmount(self.sanctionedAmt,self.schemeName)            
        super(FundLog, self).save(*args, **kwargs)

def updateSchemeAmount(amount,schemeName):
    scheme = Schemes.objects.get(schemeName = schemeName)
    scheme.amount = currencySeparator(getAmount(scheme.amount) + getAmount(amount))
    scheme.save()
    return True

class FundDisbursement(models.Model):
    financialYear = models.ForeignKey(
        FinancialYear,
        on_delete=models.SET_NULL, null=True,
        verbose_name='Financial Year'
    )
    scheme = models.ForeignKey(
        Schemes,
        on_delete=models.SET_NULL, null=True,
        verbose_name='Scheme'
    )
    disbursedOn = models.DateField(verbose_name='Disbursed On')
    openingBalance = models.CharField(max_length=20,
        validators = [validators['numbers'],validators['minimum']],
        null=True, default="0",
        verbose_name='Opening Balance'
    )
    prototypeGrant = models.CharField(max_length=20,
        validators = [validators['numbers'],validators['minimum']],
        null=False,
        verbose_name='Prototype Grant'
    )
    operationExpenditure = models.CharField(max_length=20,
        validators = [validators['numbers'],validators['minimum']],
        verbose_name='Operational Expenditure'
    )
    fabLab = models.CharField(max_length=20,
        validators = [validators['numbers'],validators['minimum']],
        verbose_name='FAB Lab'
    )
    closingBalance = models.CharField(max_length=20,
        validators = [validators['numbers'],validators['minimum']],
        verbose_name='Closing Balance',null=True, default = "0"
    )
    comment = models.TextField()
    updateOn = models.DateField(default=datetime.date.today)
    
    def __str__(self):
        return str(self.financialYear) + " " + str(self.scheme) + " " + str(self.disbursedOn)

class FundUtilization(models.Model):
    financialYear = models.ForeignKey(
        FinancialYear,
        on_delete=models.SET_NULL, null=True,
        verbose_name='Financial Year'
    )
    scheme = models.ForeignKey(
        Schemes,
        on_delete=models.SET_NULL, null=True,
        verbose_name='Scheme'
    )
    fromDate = models.DateField(verbose_name='From Date')
    toDate = models.DateField(verbose_name='To Date')
    openingBalance = models.CharField(max_length=20,
        validators = [validators['numbers'],validators['minimum']],
        null=True, default="0",
        verbose_name='Opening Balance'
    )
    prototypeGrant = models.CharField(max_length=20,
        validators = [validators['numbers'],validators['minimum']],
        null=False,
        verbose_name='Prototype Grant'
    )
    operationExpenditure = models.CharField(max_length=20,
        validators = [validators['numbers'],validators['minimum']],
        verbose_name='Operational Expenditure'
    )
    fabLab = models.CharField(max_length=20,
        validators = [validators['numbers'],validators['minimum']],
        verbose_name='FAB Lab'
    )
    interestAmt = models.CharField(max_length=20,
        validators = [validators['numbers'],validators['minimum']],
        verbose_name='Interest Amount'
    )
    returnedAmt = models.CharField(max_length=20,
        validators = [validators['numbers'],validators['minimum']],
        verbose_name='Returned Amount'
    )
    closingBalance = models.CharField(max_length=20,
        validators = [validators['numbers'],validators['minimum']],
        verbose_name='Closing Balance',null=True, default = "0"
    )
    updateOn = models.DateField(default=datetime.date.today)
    
    def __str__(self):
        return str(self.financialYear) + " " + str(self.scheme) + " " + str(self.fromDate) + " " + str(self.toDate)


class Incubatee(models.Model):
    incubatee_ID = models.CharField(
        max_length=50,
        primary_key=True,
        verbose_name="Incubatee ID"
    )
    financialYear = models.ForeignKey(
        FinancialYear,
        on_delete=models.CASCADE, null=True,blank=True,
        verbose_name="Financial Year",
        help_text = "Year entered into TBI.."
    )   
    name = models.CharField(
        max_length=50,
        validators=[validators['text']],
        verbose_name="Incubatee Name"
    )
    gender = models.CharField(
        max_length=8,
        choices=validators['gender'],
        verbose_name="Gender"
    )
    dob = models.DateField(verbose_name="Date of Birth")
    community = models.CharField(
        max_length=8,
        choices=validators['community'],
        verbose_name="Community"
    )
    mail = models.EmailField(
        max_length=60,
        verbose_name="Email ID",
    )
    mobile = models.CharField(
        max_length=10,
        validators=[validators["PhoneNumber"]],
        verbose_name="Mobile Number"
    )
    state = models.CharField(
        max_length=30, verbose_name="State"
    )
    city = models.CharField(
        max_length=30, verbose_name="City"
    )
    aadhaar = models.CharField(
        validators=[validators['Aadhaar']],
        max_length=12,
        null=False,
        verbose_name="Aadhaar Card Number",
        unique=True
    )
    pan = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        validators=[validators['Pan']],
        verbose_name="PAN Card Number",
        unique=True
    )
    education = models.CharField(
        max_length=10,
        choices=validators['education'],
        verbose_name="Educational Qualification",
    )
    degree = models.CharField(
        max_length=15,
        default="",
        validators=[validators['textspecial']],
        verbose_name="Degree",
        null=True, blank=True,
        help_text="B.Tech., Civil"
    )
    university = models.CharField(
        max_length=50,
        default="",
        blank=True,null=True,
        validators=[validators['text']],
        verbose_name="University (or) School (or) College"
    )
    profile = models.ImageField(
        upload_to=incubatee_Photos, 
        verbose_name='Profile Picture', 
        null=True, 
        blank=True, 
        default='Front End/Images/user.png'
    )
    alumini = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name = "Alumini of ",
        choices=(
            ("KEC", "KEC"),
            ("KPIT", "KPIT"),
            ("ITI", "ITI"),
            ("Kongu Arts & Science", "Kongu Arts & Science"),
        ),
    )
    year = models.IntegerField(
        verbose_name="Passout Year",
        help_text="Passout Year E.g.. 2022",
        null = True,blank= True,
    )
    updateOn = models.DateField(default=datetime.date.today,null=True,blank=True)
 
    def save(self, *args, **kwargs):
        self.updateOn = datetime.date.today()
        self.pan = self.pan.upper()
        self.mail = self.mail.lower()
        super(Incubatee, self).save(*args, **kwargs) 
    
    def __str__(self):
        return self.incubatee_ID
        
class Company(models.Model):
    incubatee_ID = models.ForeignKey(
        Incubatee, on_delete=models.CASCADE,
        verbose_name= "Incubatee", null=True,
        blank=True
    )
    company_name = models.CharField(
        max_length=50,
        null=True,blank=True,
        verbose_name="Company Name"
    )
    company_status = models.CharField(
        max_length=20,
        choices=(
            ("Registered", "Registered"),
            ("Unregistered", "Unregistered"),
        ),
        default = "Unregistered"
    )
    startupFormed = models.CharField(
        max_length=3,
        choices=(("Yes", "Yes"), ("No", "No")),
        default="No",
        verbose_name="Startup Formed?",
    )
    startupFormedDate = models.DateField(
        null=True, blank=True,
        verbose_name="Startup Formed Date"
    )
    address_state = models.CharField(
        max_length=30, verbose_name="State",
        null=True, blank=True
    )
    address_city = models.CharField(
        max_length=30, verbose_name="City",
        null=True, blank=True
    )
    company_pan = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        validators=[validators['Pan']],
        verbose_name="PAN Card Number",
        unique=True
    )
    url = models.URLField(
        verbose_name="Company Website",
        null=True,blank=True,
    )
    cin = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Company Identification Number (CIN)"
    )
    din = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Director Identification Number (DIN)"
    )
    incorporationDate = models.DateField(
        null=True, blank=True,
        verbose_name="Incorporation Date"
    )
    incorporationCertificate = models.FileField(
        upload_to=incorporation_Certificate, 
        verbose_name='Incorporation Certificate',
        null=True, 
        blank=True, 
    )
    enrollmentDate = models.DateField(
        default=datetime.date.today,
        null=True, blank=True,
        verbose_name="Enrollment Date"
    )
    enrollmentagreementDate = models.DateField(
        default=datetime.date.today,
        null=True, blank=True,
        verbose_name="Enrollment Agreement Date"
    )
    renewalDate = models.DateField(
        null=True, blank=True,
        verbose_name="Next Renewal Date"
    )
    graduationDate = models.DateField(
        null=True, blank=True,
        verbose_name="Graduation Date"
    )
    graduationType = models.CharField(
        max_length=10,
        null=True, blank=True,
        choices=(
            ("Live", "Live"),
            ("Closed", "Closed"),
        ),
        default="Live",
        verbose_name="Type of Granduation",
    )
    survivalDuringIncubation = models.IntegerField(
        verbose_name="Survival During Incubation Period(in days)",
        null=True,blank=True
    )
    survivalAfterIncubation = models.IntegerField(
        verbose_name="Survival After Incubation Period(in days)",
        null=True,blank=True
    )
    entityDetails = models.ForeignKey(
        Entity, on_delete=models.CASCADE,
        verbose_name="Entity Type",
        null=True,blank=True
    )
    entityCertificate = models.FileField(
        upload_to=entity_Certificate,
        blank=True, null=True,
        verbose_name="Entity Certificate"
    )
    logo = models.ImageField(
        upload_to=company_Logo_Photos, 
        verbose_name='Company Logo', 
        null=True,
        blank=True, 
        default='Front End/Images/company-logo.png'
    )
    updateOn = models.DateField(default=datetime.date.today,null=True,blank=True)
 
    def __str__(self):
        return self.company_name
 
    def save(self, *args, **kwargs):
        self.updateOn = datetime.date.today()
        try:
            self.renewalDate = self.enrollmentDate + datetime.timedelta(days=364)
        except:
            pass
        super(Company, self).save(*args, **kwargs)
    
class Project(models.Model):
    incubatee = models.ForeignKey(
        Incubatee,
        on_delete=models.SET_NULL, null=True,
        verbose_name="Select Incubatee", blank=True, 
    )
    financialYear = models.ForeignKey(
        FinancialYear, 
        on_delete=models.CASCADE, 
        verbose_name="Select Financial Year"
    )
    scheme = models.ForeignKey(
        Schemes, 
        on_delete=models.CASCADE, 
        verbose_name="Select Scheme",
    )
    fund_type = models.ForeignKey(
        FundingType, 
        on_delete=models.CASCADE, 
        verbose_name="Select Fund Type"
    )
    title = models.CharField(
        max_length=50,
        validators=[validators['text']],
        verbose_name="Project Title"
    )
    domain = models.CharField(
        max_length=50,
        validators=[validators['text']],
        verbose_name="Project Domain",
        help_text="e.g. 'Computer Science', 'EEE', etc."
    )
    description = models.TextField(
        verbose_name="Project Description",
    )
    term = models.IntegerField(
        verbose_name="Project Term (in months)",
        help_text="e.g. 3, 6, 12",
        validators=[validators['minimum']],
    )
    amount = models.CharField(max_length=20,
        validators = [validators['numbers']],
        verbose_name="Project Sanctioned Amount (in Rs.)"
    )
    amountSanctionedDate = models.DateField(
        verbose_name="Amount Sanctioned Date", 
        null=True,blank=True,
    )
    startDate = models.DateField(verbose_name="Project Start Date",null=True,blank=True)
    endDate = models.DateField(
        null=True,  blank=True, verbose_name="Project End Date"
    )
    status = models.CharField(
        max_length=12,
        choices=(
            ('In Progress', 'In Progress'),
            ('Completed', 'Completed'),
            ('Discontinued', 'Discontinued')
        ),
        default="In Progress",
        verbose_name="Project Status"
    )
    projectStatus = models.CharField(
        max_length=22,
        choices=(
            ('Proof of Concept', 'Proof of Concept'),
            ('Prototype', 'Prototype'),
            ('Minimum Viable Product', 'Minimum Viable Product'),
            ('Product', 'Product'),
            ('Commercialised', 'Commercialised'),
        ),
        default="Proof of Concept",
        verbose_name="Product Status"
    )
    completionDate = models.DateField(
        null=True,  blank=True, verbose_name="Project Completion Date"
    )
    outcome = models.TextField(
        null=True,  blank=True, verbose_name="Project Outcome"
    )
    closureReport = models.FileField(
        upload_to=closureReport_Certificate, 
        null=True,  blank=True, 
        verbose_name="Project Closure Report"
    )
    certifiedUC_SE = models.FileField(
        upload_to=UCReport_Certificate, 
        null=True,  blank=True, 
        verbose_name="Project Certified UC Report"
    )
    dropoutDate = models.DateField(
        null=True, blank=True,
        verbose_name="Dropout Date"
    )
    updateOn = models.DateField(default=datetime.date.today)

    

    class Meta:
        unique_together = ("incubatee", "scheme",)
    
    def save(self, *args, **kwargs):
        self.updateOn = datetime.date.today()
        if str(self.scheme) in [i['schemeName'] for i in Schemes.objects.filter(status = True).exclude(amount = '0').values('schemeName')] or str(self.scheme) == 'Incubation':
            super(Project, self).save(*args, **kwargs)    
        else:
            raise Exception("The selected scheme has No Fund / Not Active.")
        if self.status == "Discontinued":
            self.dropoutDate = datetime.date.today()
               
    def __str__(self):
        return self.title

class IncubateeTeam(models.Model):
    incubatee_ID = models.ForeignKey(Incubatee, on_delete=models.SET_NULL, null=True)
    name = models.CharField(
        max_length=20,
        validators=[validators['text']],
        verbose_name="Name"
    )
    gender = models.CharField(
        max_length=8,
        choices=validators['gender'],
        verbose_name="Gender"
    )
    mail = models.EmailField(
        max_length=60,
        error_messages={'ValueError': "Enter a valid mail id"},
        verbose_name="Email ID"
    )
    mobile = models.CharField(
        validators=[validators['PhoneNumber']],
        max_length=10,
        verbose_name="Mobile Number"
    )
    state = models.CharField(max_length=30, default="", verbose_name="State")
    city = models.CharField(max_length=30, default="", verbose_name="City")
    community = models.CharField(
        max_length=8,
        choices=validators['community'],
        verbose_name="Community ",
        null = True,
    )
    education = models.CharField(
        max_length=40,
        choices=validators['education'],
        verbose_name="Educational Qualification",
        null = True,
    )
    university = models.CharField(
        max_length=40,
        default="",
        validators=[validators['text']],
        verbose_name="University / College / School",
    )
    role = models.CharField(
        max_length=20,
        validators=[validators['text']],
        verbose_name="Role",
        null = True,
    )
    pan = models.CharField(
        max_length=15,
        null=True,blank=True,
        verbose_name="PAN Card Number"
    )
    aadhaar = models.CharField(
        validators=[validators['Aadhaar']],
        max_length=12,
        verbose_name="Aadhaar Card Number"
    )
    alumini = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=(
            ("KEC", "KEC"),
            ("KPIT", "KPIT"),
            ("ITI", "ITI"),
            ("Kongu Arts & Science", "Kongu Arts & Science"),
        ),
    )
    year = models.IntegerField(
        verbose_name="Passout Year",
        help_text="Passout Year E.g.. 2022",
        validators=[validators['minimum']],
        null = True,
        blank= True,
    )
    profile = models.ImageField(
        upload_to=TeamProfilePics, 
        verbose_name='Profile Picture', 
        null=True, 
        blank=True, 
        default='Front End/Images/user.png'
    )
    updateOn = models.DateField(default=datetime.date.today)

    class Meta:
        unique_together = ("incubatee_ID", "aadhaar","pan")
    

    def save(self):
        self.pan = self.pan.upper()
        self.mail = self.mail.lower()
        super(IncubateeTeam, self).save()

    def __str__(self):
        return str(self.incubatee_ID) + ' ' + self.name

class Installment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    installmentDate = models.DateField(verbose_name="Installment Date")
    disbursedOn = models.DateField(
        verbose_name="Disbursed On", 
        null=True,blank=True
    )
    disbursedAmt = models.CharField(max_length=20,
        validators = [validators['numbers']],
        verbose_name="Disbursed Amount (in Rs.)"
    )
    uc_attachment = models.FileField(
        upload_to=Installment_UC_Certificate,
        null=True, blank = True,
    )
    progressReport = models.FileField(
        upload_to=Installment_Progress_Certificate,
        null=True, blank = True,
    )
    remarks = models.TextField(
        null=True, blank=True,
        verbose_name="Remarks"
    )
    updateOn = models.DateField(default=datetime.date.today)

    def save(self):
        self.updateOn = datetime.date.today()
        super(Installment, self).save()
        
    def __str__(self):
        return str(self.project) + " " + self.installmentDate.strftime("%d-%m-%Y")


class Patents(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    title = models.CharField(
        max_length=50,
        validators=[validators['text']],
        verbose_name="Patent Title"
    )
    filedOn = models.DateField(verbose_name="Patent Filing Date")
    patentNo = models.CharField(
        validators=[validators['Number']],
        max_length=10,
        verbose_name="Patent Number"
    )
    publishedAt = models.CharField(
        max_length=30,
        validators=[validators['text']],
        verbose_name="Publication Country"
    )
    type = models.CharField(
        max_length=12,
        choices=(
            ('Product', 'Product'),
            ('Process', 'Process'),
            ('Design', 'Design'),
            ('Utility', 'Utility'),
            ('Other', 'Other')
        ),
        verbose_name="Patent Type"
    )
    status = models.CharField(max_length=42, choices=(
            ('Provisional Patent Filed', 'Provisional Patent Filed'),
            ('Complete Specification Indian Patent Filed',
            'Complete Specification Indian Patent Filed'),
            ('Patent Granted', 'Patent Granted'),
            ('PCT Filed', 'PCT Filed'),
            ('PCT Granted', 'PCT Granted'),
        ),
        verbose_name="Status"
    )

    updateOn = models.DateField(default=datetime.date.today)

    def __str__(self):
        return str(self.project) + " " + self.title

class Copyright(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    title = models.CharField(
        max_length=50,
        validators=[validators['text']],
        verbose_name="Copyright Title"
    )
    filedOn = models.DateField(verbose_name="Copyright Filing Date")
    copyrightNo = models.CharField(
        validators=[validators['Number']],
        max_length=10,
        default="",
        verbose_name="Copyright Number"
    )
    publishedAt = models.CharField(
        max_length=30,
        validators=[validators['text']],
        verbose_name="Publication Country"
    )
    type = models.CharField(
        max_length=12,
        choices=(
            ('Software', 'Software'),
            ('Architecture', 'Architecture'),
        ),
        verbose_name="Copyright Type"
    )
    status = models.CharField(max_length=45, choices=(
            ('Filed', 'Filed'),
            ('Not Granted','Not Granted'),
            ('Granted', 'Granted'),
        ),
        verbose_name="Status"
    )

    updateOn = models.DateField(default=datetime.date.today)

    def __str__(self):
        return str(self.project) + " " + self.title

class Trademark(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(
        upload_to=Trademark_Photo, 
        verbose_name='Logo / Name of the Company', 
        null=True, 
        blank=True, 
    )
    remarks = models.TextField(
        null=True, blank=True,
        verbose_name="Remarks"
    )
    filedOn = models.DateField(verbose_name="Trademark Filing Date")
    trademarkNo = models.CharField(
        validators=[validators['Number']],
        max_length=10,
        default="",
        verbose_name="Trademark Number"
    )
    updateOn = models.DateField(default=datetime.date.today)
    
    def __str__(self):
        return str(self.trademarkNo) + " "

class ProjectRevenue(models.Model):
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
        null=True
    )
    financialYear = models.ForeignKey(
        FinancialYear, 
        on_delete=models.CASCADE, 
        verbose_name="Financial Year"
    )
    revenue = models.CharField(max_length=20,
        validators = [validators['numbers'],validators['minimum']],
        verbose_name="Revenue Amount"
    )
    updateOn = models.DateField(default=datetime.date.today)

    def __str__(self):
        return str(self.project)


class ProjectEmployment(models.Model):
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE, 
    )
    employment = models.IntegerField(
        validators=[validators['minimum']], verbose_name="Employment Generated")
    date = models.DateField()
    updateOn = models.DateField(default=datetime.date.today)

    def __str__(self):
        return str(self.project.id) + " " + " " + str(self.employment)


class ProjectProduct(models.Model):
    financialYear = models.ForeignKey(
        FinancialYear, 
        on_delete=models.CASCADE,
        verbose_name="Financial Year"    
    )
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE,
    )
    product_image = models.ImageField(
        upload_to=Product_Photo, 
        verbose_name='Product Picture', 
        default='static/images/user1.png'
    )
    product_name = models.CharField(max_length=50, verbose_name="Product Name")
    units_sold = models.IntegerField(
        validators=[validators['minimum']], verbose_name="No. of units sold")
    launchDate = models.DateField(verbose_name="Launch Date")
    updateOn = models.DateField(default=datetime.date.today)
    
    
    def __str__(self):
        return str(self.project.title) + " " + self.product_name


class ProjectAwards(models.Model):
    financialYear = models.ForeignKey(
        FinancialYear, 
        on_delete=models.CASCADE, 
        verbose_name="Financial Year"    
    )
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE,
    )
    date = models.DateField(verbose_name="Event Date")
    eventName = models.CharField(max_length=100, verbose_name="Event Name")
    awardTitle = models.CharField(max_length=100, verbose_name="Award Title")
    amount = models.CharField(
        max_length=20,validators = [validators['numbers']],
        verbose_name="Price Money",
        blank=True, null=True,                          
    )
    certificate = models.FileField(
        upload_to=Awards_Certifcate,
        null=True,blank=True,
        verbose_name="Certificate"
    )
    photo = models.ImageField(
        upload_to=Awards_Photo, 
        verbose_name='Award Photo', 
        null=True,
        blank=True, 
    )
    def __str__(self):
        return str(self.project) + " " + str(self.date) + " " + self.eventName
    

class ProjectIntern(models.Model):
    financialYear = models.ForeignKey(
        FinancialYear, 
        on_delete=models.CASCADE,
        verbose_name="Financial Year"    
    )
    rollno = models.CharField(max_length=20, verbose_name="Roll No.")
    name = models.CharField(max_length=50, verbose_name="Name")
    Department = models.CharField(max_length=50, verbose_name="Department")
    title = models.CharField(max_length=50, verbose_name="Intern Title")
    fromdate = models.DateField(verbose_name="Intern Start Date")
    todate = models.DateField(verbose_name="Intern End Date")
    stipend = models.CharField(max_length=20, verbose_name="Stipend", choices=(
        ('Yes', 'Yes'),
        ('No', 'No'),
    ))
    amount = models.CharField(max_length=20, verbose_name="Amount", null=True, blank=True, validators=[validators['numbers']])
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE,
    )
    certificate = models.FileField(
        upload_to=Intern_Certifcate,
        null=True,blank=True,
        verbose_name="Certificate"
    )
    def __str__(self):
        return str(self.project) 


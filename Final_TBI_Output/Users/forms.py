from django.forms import ModelForm, fields
from .models import *
from django import forms

masking = "convertToINRFormat($(this).val(),$(this));"

class DateInput(forms.DateInput):
    input_type = 'date'

class EntityForm(ModelForm):
    class Meta:
        model = Entity
        fields = '__all__'

class SchemeForm(ModelForm):
    class Meta:
        model = Schemes
        fields = ('schemeName',)

class FundingForm(ModelForm):
    class Meta:
        model = FundingType
        fields = '__all__'

class VisitorForm(ModelForm):
    class Meta:
        model = Visitors
        fields = '__all__'
        widgets = {
            'date': DateInput(),
        }
class VisitorImagesForm(ModelForm):
    class Meta:
        model = VisitorImages
        fields = '__all__'

class EventForm(ModelForm):
    class Meta:
        model = Events
        exclude = ('days',)
        widgets = {
            'fromdate': DateInput(),
            'todate': DateInput(),
        }
class EventImagesForm(ModelForm):
    class Meta:
        model = EventImages
        fields = '__all__'
class EventReportsForm(ModelForm):
    class Meta:
        model = EventReports
        fields = '__all__'
class EventSponserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventSponserForm, self).__init__(*args, **kwargs)
        for fields in self.fields:
            if fields == 'amount':
                self.fields[fields].widget.attrs['onkeyup'] = masking    
    class Meta:
        model = EventSponsors
        fields = '__all__'
        

class FundLogForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(FundLogForm, self).__init__(*args, **kwargs)
        for fields in self.fields:
            if fields == 'sanctionedAmt':
                self.fields[fields].widget.attrs['onkeyup'] = masking    
    class Meta:
        model = FundLog
        fields = '__all__'
        widgets = {
            'date': DateInput(),
        }
        
class DisbursementForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DisbursementForm, self).__init__(*args, **kwargs)
        for fields in self.fields:
            if fields in ['openingBalance','closingBalance']:
                self.fields[fields].widget.attrs['readonly'] = "true"    
            if fields not in ['disbursedOn','comment']:
                self.fields[fields].widget.attrs['onkeyup'] = masking    + "addToClosingDisbursement(this.value);"
                # self.fields[fields].widget.attrs['onkeypress'] = "addToClosing(this.value);"    
                
    class Meta:
        model = FundDisbursement
        exclude = ('financialYear','scheme','updateOn')
        widgets = {
            'disbursedOn': DateInput(),
        }
        
class UtilizatedForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UtilizatedForm, self).__init__(*args, **kwargs)
        for fields in self.fields:
            if fields in ['openingBalance','closingBalance','prototypeGrant']:
                self.fields[fields].widget.attrs['readonly'] = "true"    
            if fields not in ['fromDate','toDate']:
                self.fields[fields].widget.attrs['onkeyup'] = masking    + "addToClosingUtlization(this.value);"
                
    class Meta:
        model = FundUtilization
        exclude = ('financialYear','scheme','updateOn')
        widgets = {
            'fromDate': DateInput(),
            'toDate': DateInput(),
        }
        
class IncubateeForm(ModelForm):    
    def __init__(self, *args, **kwargs):
        super(IncubateeForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = Incubatee
        exclude = ('incubatee_ID','updateOn')
        widgets = {
            'dob': DateInput(),
        }
        
class CompanyForm(ModelForm):    
    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        for fields in self.fields:
            if fields in ['year']:
                self.fields[fields].widget.attrs['class'] += "datepicker"
    class Meta:
        model = Company
        fields = ('company_name','company_status','startupFormed','startupFormedDate','logo',)
        widgets = {
            'startupFormedDate': DateInput(),
            'incorporationDate': DateInput(),
            'enrollmentDate': DateInput(),
            'enrollmentagreementDate': DateInput(),
            'renewalDate': DateInput(),
            'graduationDate': DateInput(),
        }
        
class ProjectForm(ModelForm):    
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for fields in self.fields:
            if fields == 'amount':
                self.fields[fields].widget.attrs['onkeyup'] = masking    
        
    class Meta:
        model = Project
        exclude = ('incubatee','updateOn','endDate','completionDate','outcome','closureReport','certifiedUC_SE','dropoutDate')
        widgets = {
            'amountSanctionedDate': DateInput(),
            'startDate': DateInput(),
        }
class ProjectEditForm(ModelForm):    
    def __init__(self, *args, **kwargs):
        super(ProjectEditForm, self).__init__(*args, **kwargs)
        for fields in self.fields:
            if fields == 'amount':
                self.fields[fields].widget.attrs['onkeyup'] = masking    
        
    class Meta:
        model = Project
        exclude = ('incubatee','updateOn','dropoutDate')
        widgets = {
            'amountSanctionedDate': DateInput(),
            'startDate': DateInput(),
            'endDate': DateInput(),
            'completionDate': DateInput(),
            'endDate': DateInput(),
        }
        
        
class TeamForm(ModelForm):    
    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        for fields in self.fields:
            if fields == 'amount':
                self.fields[fields].widget.attrs['onkeyup'] = masking    
        
    class Meta:
        model = IncubateeTeam
        exclude = ('incubatee_ID','updateOn')
        widgets = {
            'amountSanctionedDate': DateInput(),
            'startDate': DateInput(),
        }
        
class InstallmentForm(ModelForm):    
    def __init__(self, *args, **kwargs):
        super(InstallmentForm, self).__init__(*args, **kwargs)
        for fields in self.fields:
            if fields == 'disbursedAmt':
                self.fields[fields].widget.attrs['onkeyup'] = masking    
        
    class Meta:
        model = Installment
        exclude = ('project','updateOn')
        widgets = {
            'installmentDate': DateInput(),
            'disbursedOn': DateInput(),
        }
        
class PatentForm(ModelForm):    
    def __init__(self, *args, **kwargs):
        super(PatentForm, self).__init__(*args, **kwargs)
        for fields in self.fields:
            if fields == 'disbursedAmt':
                self.fields[fields].widget.attrs['onkeyup'] = masking    
        
    class Meta:
        model = Patents
        exclude = ('project','updateOn')
        widgets = {
            'filedOn': DateInput(),
        }
        
class CopyrightForm(ModelForm):    
    def __init__(self, *args, **kwargs):
        super(CopyrightForm, self).__init__(*args, **kwargs)
        for fields in self.fields:
            if fields == 'disbursedAmt':
                self.fields[fields].widget.attrs['onkeyup'] = masking    
        
    class Meta:
        model = Copyright
        exclude = ('project','updateOn')
        widgets = {
            'filedOn': DateInput(),
        }
        
class TrademarkForm(ModelForm):    
    def __init__(self, *args, **kwargs):
        super(TrademarkForm, self).__init__(*args, **kwargs)
        for fields in self.fields:
            if fields == 'disbursedAmt':
                self.fields[fields].widget.attrs['onkeyup'] = masking    
        
    class Meta:
        model = Trademark
        exclude = ('project','updateOn')
        widgets = {
            'filedOn': DateInput(),
        }
        
# impact
class ProjectRevenueForm(ModelForm):    
    def __init__(self, *args, **kwargs):
        super(ProjectRevenueForm, self).__init__(*args, **kwargs)
        for fields in self.fields:
            if fields == 'revenue':
                self.fields[fields].widget.attrs['onkeyup'] = masking    
        
    class Meta:
        model = ProjectRevenue
        exclude = ('project','updateOn')
        
class ProjectInternForm(ModelForm):    
    def __init__(self, *args, **kwargs):
        super(ProjectInternForm, self).__init__(*args, **kwargs)
        for fields in self.fields:
            if fields == 'amount':
                self.fields[fields].widget.attrs['onkeyup'] = masking    
        
    class Meta:
        model = ProjectIntern
        exclude = ('project','updateOn')
        widgets = {
            'fromdate': DateInput(),
            'todate': DateInput(),
        }
        
class ProjectEmploymentForm(ModelForm):    
    class Meta:
        model = ProjectEmployment
        exclude = ('project','updateOn')
        widgets = {
            'date': DateInput(),
        }
        
class ProjectAwardsForm(ModelForm):  
    def __init__(self, *args, **kwargs):
        super(ProjectAwardsForm, self).__init__(*args, **kwargs)
        for fields in self.fields:
            if fields == 'amount':
                self.fields[fields].widget.attrs['onkeyup'] = masking    
          
    class Meta:
        model = ProjectAwards
        exclude = ('project','updateOn')
        widgets = {
            'date': DateInput(),
        }
        
class ProjectProductForm(ModelForm):  
    def __init__(self, *args, **kwargs):
        super(ProjectProductForm, self).__init__(*args, **kwargs)
        for fields in self.fields:
            if fields == 'amount':
                self.fields[fields].widget.attrs['onkeyup'] = masking    
          
    class Meta:
        model = ProjectProduct
        exclude = ('project','updateOn')
        widgets = {
            'launchDate': DateInput(),
        }
        
        
# edit form Incubatee

class CompanyEditForm(ModelForm):    
    def __init__(self, *args, **kwargs):
        super(CompanyEditForm, self).__init__(*args, **kwargs)
        for fields in self.fields:
            if fields in ['year']:
                self.fields[fields].widget.attrs['class'] += "datepicker"
    class Meta:
        model = Company
        exclude = ('incubatee_ID','updateOn',)
        widgets = {
            'startupFormedDate': DateInput(),
            'incorporationDate': DateInput(),
            'enrollmentDate': DateInput(),
            'enrollmentagreementDate': DateInput(),
            'renewalDate': DateInput(),
            'graduationDate': DateInput(),
        }
        
class ProjectForm(ModelForm):    
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for fields in self.fields:
            if fields == 'amount':
                self.fields[fields].widget.attrs['onkeyup'] = masking    
        
    class Meta:
        model = Project
        exclude = ('incubatee','updateOn','dropoutDate')
        widgets = {
            'amountSanctionedDate': DateInput(),
            'startDate': DateInput(),
        }
        
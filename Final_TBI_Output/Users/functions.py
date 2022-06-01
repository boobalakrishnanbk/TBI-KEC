import datetime
from django.core.exceptions import ValidationError
import os
def MinValueValidators(value):
    try:
        value = int(value)
        if value >=0:
            return value
        else:
            raise ValidationError("Negative values are entered.Please Check the values")
    except :
        return 0


def currencySeparator(value):
    if(value == None):
        return 0
    amt = ''
    value = str(int(value))
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

def CheckValidAndSave(request,formObject):
    form = formObject(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        return formObject()
    else:
        return form
    

def getAmount(value):
    try:
        return int((value).replace(",",""))
    except:
        return 0 

def getOpeningBalance(object1,object2,value_list):
    try:
        balance = object1[0][value_list[0]]
    except:
        try:
            balance = getSum(aggregate_Amount(object2,[value_list[1]]))
        except:
            balance = 0
        
    return balance
    
def is_Image(doc_list):
    images_types = ('jpeg','jpg','png','raw')
    image_list = []
    for i in doc_list:
        if i[0].endswith(images_types):
            image_list.append(i)
    return image_list

def is_OtherTypes(doc_list):
    types = ('jpeg','jpg','png','raw','pdf')
    image_list = []
    for i in doc_list:
        if not i[0].endswith(types):
            image_list.append(i)
    return image_list

def is_Empty(object,value):
    try:
        return object[0][value]
    except:
        return 0
    
def aggregate_Amount(object, list_values):
    output_values = []
    for i in list_values:
        sum = 0
        for j in object:
            sum += getAmount(j[i])
        output_values.append(currencySeparator(sum))
    return output_values

def getSum(list_values):
    sum = 0
    for i in list_values:
        sum += getAmount(i)
    return currencySeparator(sum)

def getRecentDate(dateList):
    recentDate = datetime.date(2000, 1, 1)
    for i in dateList:
        try:
            if i > recentDate:
                recentDate = i
        except:
            pass
    if recentDate == datetime.date(2000, 1, 1):
        return ""
    return recentDate
    
def getFiles(path):
    path = "Front End/Images/"+ path
    try:
        files_list = os.listdir(path)
        for i in range(len(files_list)):
            files_list[i] = ["/static/"+ path + files_list[i], files_list[i]]
    except:
        files_list = ""
    image_files = is_Image(files_list)    
    pdf_files = [i for i in files_list if i[0].endswith(".pdf") ]
    other_files = is_OtherTypes(files_list)
    return {
        "files":other_files,
        "pdf":pdf_files,
        "images":image_files,
    }
    
def getAge(born):
    today = datetime.date.today()
    try:
        if born != None:
            birthday = born.replace(year = today.year)
        else:
            return 0
    except:
        birthday = born.replace(year = today.year,month = today.month+1,day = 1)
    if birthday > today:
        return today.year - born.year -1
    else:
        return today.year - born.year
    
def getNumberAsWord(number):
    number = str(number)
    words = [' k',' L',' Cr']
    count = number.count(',')
    number = number.replace(',','.')
    if number[number.find('.')+1] == '0':
        last = number.find('.')
    else:
        last = number.find('.')+2
    if(number[:last] == ''):
        return '0'
    return number[:last] +  words[count-1]
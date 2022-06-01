import os
from .models import *
import datetime




def visitorPhotos(instance, filename):
    file_path = "Front End/Images/Visitors/"
    format = str(instance.visitor.guestName) + '_' + str(instance.visitor.name) + '_' + \
        datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S") + \
        '.' + filename.split(".")[-1]
    file_path = file_path + format
    return file_path

def eventPhotos(instance, filename):
    file_path = "Front End/Images/Events/"
    format = str(instance.event.title) + '/' + \
        str(instance.event.fromdate) + "/"+ str(instance.event.todate) + \
        '.' + filename.split(".")[-1]
    file_path = file_path + format
    return file_path

def eventReports(instance, filename):
    file_path = "Front End/Images/Events/"
    format = str(instance.events.title) + '_' + \
        str(instance.events.fromdate) + "_"+ str(instance.events.todate) + \
        '.' + filename.split(".")[-1]
    file_path = file_path + format
    return file_path

# Incubatee
def incubatee_Photos(instance, filename):
    file_path = "Front End/Images/Incubatees/Profile Pics/"
    format = str(instance.incubatee_ID) + '_' + \
        datetime.datetime.now().strftime("%d-%m-%Y:%S") + \
        '.' + filename.split(".")[-1]
    file_path = file_path + format
    return file_path

# company
def company_Logo_Photos(instance, filename):
    file_path = "Front End/Images/Company/Logo/"
    format = str(instance.company_name) + '_' + \
        datetime.datetime.now().strftime("%d-%m-%Y:%S") + \
        '.' + filename.split(".")[-1]
    file_path = file_path + format
    return file_path

def incorporation_Certificate(instance, filename):
    file_path = "Front End/Images/Company/Incorporation/"
    format = str(instance.company_name) + '_' + \
        datetime.datetime.now().strftime("%d-%m-%Y:%S") + \
        '.' + filename.split(".")[-1]
    file_path = file_path + format
    return file_path
def entity_Certificate(instance, filename):
    file_path = "Front End/Images/Company/Entity/"
    format = str(instance.company_name) + '_' + \
        datetime.datetime.now().strftime("%d-%m-%Y:%S") + \
        '.' + filename.split(".")[-1]
    file_path = file_path + format
    return file_path

# Project
def closureReport_Certificate(instance, filename):
    file_path = "Front End/Images/Project/Closure Report/"
    format = str(instance.title) + '_' + \
        str(instance.incubatee) + '_' + \
        datetime.datetime.now().strftime("%d-%m-%Y:%S") + \
        '.' + filename.split(".")[-1]
    file_path = file_path + format
    return file_path
def UCReport_Certificate(instance, filename):
    file_path = "Front End/Images/Project/UC Report/"
    format = str(instance.title) + '_' + \
        str(instance.incubatee) + '_' + \
        datetime.datetime.now().strftime("%d-%m-%Y:%S") + \
        '.' + filename.split(".")[-1]
    file_path = file_path + format
    return file_path

# team
def TeamProfilePics(instance, filename):
    file_path = "Front End/Images/Company/Team/"
    format = str(instance.name) + '_' + \
        str(instance.incubatee_ID.name) + '_' + \
        datetime.datetime.now().strftime("%d-%m-%Y:%S") + \
        '.' + filename.split(".")[-1]
    file_path = file_path + format
    return file_path

# team
def Installment_UC_Certificate(instance, filename):
    file_path = "Front End/Images/Projects/UC/"
    format = str(instance.project.title) + '_' + \
        str(instance.id) + '_' + \
        datetime.datetime.now().strftime("%d-%m-%Y:%S") + \
        '.' + filename.split(".")[-1]
    file_path = file_path + format
    return file_path
def Installment_Progress_Certificate(instance, filename):
    file_path = "Front End/Images/Projects/Progress/"
    format = str(instance.project.title) + '_' + \
        str(instance.id) + '_' + \
        datetime.datetime.now().strftime("%d-%m-%Y:%S") + \
        '.' + filename.split(".")[-1]
    file_path = file_path + format
    return file_path

# trademark
def Trademark_Photo(instance, filename):
    file_path = "Front End/Images/Projects/Trademark/"
    format = str(instance.project.title) + '_' + \
        str(instance.id) + '_' + \
        datetime.datetime.now().strftime("%d-%m-%Y:%S") + \
        '.' + filename.split(".")[-1]
    file_path = file_path + format
    return file_path

# products
def Product_Photo(instance, filename):
    file_path = "Front End/Images/Projects/Product/"
    format = str(instance.project.title) + '_' + \
        str(instance.id) + '_' + \
        datetime.datetime.now().strftime("%d-%m-%Y:%S") + \
        '.' + filename.split(".")[-1]
    file_path = file_path + format
    return file_path

# awards
def Awards_Photo(instance, filename):
    file_path = "Front End/Images/Projects/Awards/"
    format = str(instance.project.title) + '_' + \
        str(instance.id) + '_' + \
        datetime.datetime.now().strftime("%d-%m-%Y:%S") + \
        '.' + filename.split(".")[-1]
    file_path = file_path + format
    return file_path

def Awards_Certifcate(instance, filename):
    file_path = "Front End/Images/Projects/Awards/"
    format = str(instance.project.title) + '_' + \
        str(instance.id) + '_' + \
        datetime.datetime.now().strftime("%d-%m-%Y:%S") + \
        '.' + filename.split(".")[-1]
    file_path = file_path + format
    return file_path

# Intern
def Intern_Certifcate(instance, filename):
    file_path = "Front End/Images/Projects/Intern/"
    format = str(instance.project.title) + '_' + \
        str(instance.id) + '_' + \
        datetime.datetime.now().strftime("%d-%m-%Y:%S") + \
        '.' + filename.split(".")[-1]
    file_path = file_path + format
    return file_path
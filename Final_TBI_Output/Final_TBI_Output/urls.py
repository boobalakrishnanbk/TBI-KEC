from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static


from Users import views
# from Users import formSubmit

app_name = 'Users'


urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    
    # login / logout
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # home
    path('',views.login_user,name = 'login_user'),
    path('home/',views.home,name = 'home'),
    
    # gallery
    path('galleryVisitors/',views.galleryVisitors,name = 'galleryVisitors'),
    path('galleryEvents/',views.galleryEvents,name = 'galleryEvents'),
    path('galleryIncubatees/',views.galleryIncubatees,name = 'galleryIncubatees'),
    path('galleryTeam/',views.galleryTeam,name = 'galleryTeam'),
    path('galleryCompanyLogo/',views.galleryCompanyLogo,name = 'galleryCompanyLogo'),
    path('galleryIncorporations/',views.galleryIncorporations,name = 'galleryIncorporations'),
    path('galleryEntities/',views.galleryEntities,name = 'galleryEntities'),
    path('galleryClosureReports/',views.galleryClosureReports,name = 'galleryClosureReports'),
    path('galleryUCReports/',views.galleryUCReports,name = 'galleryUCReports'),
    path('galleryInstallments/',views.galleryInstallments,name = 'galleryInstallments'),
    path('galleryInstallmentProgress/',views.galleryInstallmentProgress,name = 'galleryInstallmentProgress'),
    path('galleryProducts/',views.galleryProducts,name = 'galleryProducts'),
    path('galleryTrademarks/',views.galleryTrademarks,name = 'galleryTrademarks'),
    path('galleryAwards/',views.galleryAwards,name = 'galleryAwards'),
    
    # visitors
    path('visitors/',views.visitors,name = 'visitors'),
    
    # events
    path('events/',views.events,name = 'events'),
    
    # settings
    path('settings/',views.settings,name = 'settings'),
    # path('settings/',views.settings,name = 'settings'),

    # fundflow
    path('fundflow/',views.fundflow,name = 'fundflow'),
    path('scheme/<str:name>/<int:pagination>',views.scheme,name = 'scheme'),
    
    path('disbursement_Analysis/<str:name>/<int:pagination>',views.disbursement_Analysis,name = 'disbursement_Analysis'),
    path('utilization_Analysis/<str:name>/<int:pagination>',views.utilization_Analysis,name = 'utilization_Analysis'),
    
    path('fund_Disbursement/<str:name>/<str:years>',views.fund_Disbursement,name = 'fund_Disbursement'),
    path('fund_Utilization/<str:name>/<str:years>',views.fund_Utilization,name = 'fund_Utilization'),
    
    # incubatees
    path('incubatees/<int:pagination>',views.incubatees,name = 'incubatees'),
    path('incubatee/<str:incubateeID>/<str:page>',views.incubatee,name = 'incubatee'),
    
    path('addMember/<str:incubateeID>',views.addMember,name = 'addMember'),
    path('addProject/<str:incubateeID>',views.addProject,name = 'addProject'),
    path('addInstallment/<str:incubateeID>/<str:project_ID>',views.addInstallment,name = 'addInstallment'),
    path('addPatent/<str:incubateeID>/<str:project_ID>',views.addPatent,name = 'addPatent'),
    path('addCopyright/<str:incubateeID>/<str:project_ID>',views.addCopyright,name = 'addCopyright'),
    path('addTrademark/<str:incubateeID>/<str:project_ID>',views.addTrademark,name = 'addTrademark'),
    path('addRevenue/<str:incubateeID>/<str:project_ID>',views.addRevenue,name = 'addRevenue'),
    path('addEmployment/<str:incubateeID>/<str:project_ID>',views.addEmployment,name = 'addEmployment'),
    path('addAwards/<str:incubateeID>/<str:project_ID>',views.addAwards,name = 'addAwards'),
    path('addIntern/<str:incubateeID>/<str:project_ID>',views.addIntern,name = 'addIntern'),
    path('addProduct/<str:incubateeID>/<str:project_ID>',views.addProduct,name = 'addProduct'),
    
    path('editInstallment/<str:incubateeID>/<str:project_ID>',views.editInstallment,name = 'editInstallment'),
    path('editPatent/<str:incubateeID>/<str:project_ID>',views.editPatent,name = 'editPatent'),
    path('editIncubatee/<str:incubateeID>',views.editIncubatee,name = 'editIncubatee'),
    path('editIncubateeProject/<str:incubateeID>/<str:project_ID>',views.editIncubateeProject,name = 'editIncubateeProject'),
    # reports
    path('reportIncubatee/',views.reportIncubatee,name = 'reportIncubatee'),
    path('reportAge/',views.reportAge,name = 'reportAge'),
    path('reportFund/',views.reportFund,name = 'reportFund'),
    path('reportCompany/',views.reportCompany,name = 'reportCompany'),
    path('reportDomain/',views.reportDomain,name = 'reportDomain'),
    path('reportStartup/',views.reportStartup,name = 'reportStartup'),
    
    
    # # profile
    # path('profile/',views.profile,name = 'profile'),
    
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

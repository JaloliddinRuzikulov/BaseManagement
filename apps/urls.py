from django.urls import path
from .views import appsView,addRatsiya,userManager,RatDetailView,TadbirView,TadbirViews,RatListView,Adds,eventClose,omborListView,some_view,printerView
urlpatterns = [
    path('add/',addRatsiya, name ='add'),
    path('main/',appsView,name='main'),
    path('events/<int:tadbirid>/',TadbirView,name='detialevent'),      
    path('events/',TadbirViews.as_view(),name='events'),  
    path('lists/',RatListView.as_view(),name='lists'),    
    path('ombor/',omborListView.as_view(),name='ombor'),        
    path('some_view/',some_view,name='some_view'),    
    path('',userManager, name='logins'),
    path('detial/<int:pk>/', RatDetailView.as_view(), name='detial'),
    path('events/<int:tadbirid>/close',eventClose, name='CEvent'),
    path('events/<int:tadbirid>/print',printerView, name='printer'),
]




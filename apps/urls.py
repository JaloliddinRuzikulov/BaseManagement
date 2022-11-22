from django.urls import path
from .views import apps_view, add_ratsiya, user_manager, RatDetailView, tadbir_view, TadbirViews, RatListView,  \
    event_close, OmborListView,  printer_view

urlpatterns = [
    path('add/', add_ratsiya, name='add'),
    path('main/', apps_view, name='main'),
    path('events/<int:tadbirid>/', tadbir_view, name='detialevent'),
    path('events/', TadbirViews.as_view(), name='events'),
    path('lists/', RatListView.as_view(), name='lists'),
    path('ombor/', OmborListView.as_view(), name='ombor'),
    path('', user_manager, name='logins'),
    path('detial/<int:pk>/', RatDetailView.as_view(), name='detial'),
    path('events/<int:tadbirid>/close', event_close, name='CEvent'),
    path('events/<int:tadbirid>/print', printer_view, name='printer'),
]

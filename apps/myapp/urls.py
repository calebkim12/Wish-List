from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('make_item', views.make_item),
    path('create', views.create),
    path('add_item/<int:item_id>', views.add_item),
    path('show/<int:item_id>', views.show),
    path('destroy/<int:item_id>', views.destroy),
    path('remove/<int:item_id>', views.remove),
    path('logout', views.logout),
]
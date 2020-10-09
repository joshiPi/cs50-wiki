from django.urls import path

from . import views
app_name= 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:entry>',views.display_entry,name='entry'),
    path('save',views.show_entry_form,name='save'),
    path('search',views.search,name='search'),
    path('random',views.random_entry,name='random'),
    path('wiki/edit/<str:title>',views.edit_entry,name='edit')


]

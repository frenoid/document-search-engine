from django.conf.urls import url
from .views_v2 import (
        CountriesListView, CountryDetailsView, HomeView,
        PolicyView, LeadGenerateView)

urlpatterns = [
        url(r'^countries/(?P<iso_code>[\w-]+)/$', CountryDetailsView.as_view(),
            name='country_details'),
        url(r'^countries/$', CountriesListView.as_view(),
            name='countries_list'),
        url(r'^policies/(?P<slug>[\w-]+)/$', PolicyView.as_view(),
            name='policy_details'),
        url(r'^policies/$', PolicyView.as_view(),
            name='policies_list'),
        url(r'^lead/$', LeadGenerateView.as_view(),
            name='generate_lead'),
        url(r'^$', HomeView.as_view(), name='home')
]

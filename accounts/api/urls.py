from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^manager/clients/$', views.ManagerClientListView.as_view(), name='manager-client-list'),
    url(
        r'^manager/clients/(?P<id>[0-9]+)/$',
        views.ManagerClientDetailView.as_view(),
        name='manager-client-detail'
    ),

    url(r'^client/register/$', views.ClientRegisterView.as_view(), name='client-account-register'),
    url(r'^client/profile/$', views.ClientProfileView.as_view(), name='client-profile'),
    url(r'^client/provide_pin/$', views.ClientProvidePINView.as_view(), name='client-provide-pin'),

    url(r'^login/$', views.UserLoginAPIView.as_view(), name='user-login')
]
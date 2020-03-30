"""customer_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from line_up.views import LineupView, index, StoresListView, SingleStoreListView, LineManagerView


urlpatterns = [
# unique registration link
	path('', index, name='home'),
    # path('invitations/', include('invitations.urls', namespace='invitations')),
	path('stores/', StoresListView.as_view(), name='stores_list'),
	path('stores/<str:state>', SingleStoreListView.as_view(), name='stores_in_state'),
    path('manage_line/<int:store_id>', LineManagerView.as_view(), name='stores_line_manager'),
    path('admin/', admin.site.urls),
    path('lineup/<int:store_id>', LineupView.as_view(), name='lineup'),

    path('django-rq/', include('django_rq.urls'))
]

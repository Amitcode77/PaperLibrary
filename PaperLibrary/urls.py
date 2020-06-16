"""PaperLibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import re_path

from PaperManager import views as views_manager
from . import views as views_main

urlpatterns = [
    re_path('^admin/', admin.site.urls),
    re_path('^$', views_main.login_process),
    re_path('^login.html', views_main.login_process),
    re_path('^log-in', views_main.login_process, kwargs={'action': 'log-in'}),
    re_path('^log-out', views_main.login_process, kwargs={'action': 'log-out'}),
    re_path('^main.html$', views_manager.main, kwargs={'init': 'search'}),
    re_path('^main.html,manage', views_manager.main, kwargs={'init': 'manage'}),
    re_path('^add-project', views_manager.add_project),
    re_path('^delete-project', views_manager.delete_project),
    re_path('^add-paper', views_manager.add_paper),
    re_path('^delete-paper', views_manager.delete_paper),
    re_path('^download', views_manager.download),
    re_path('^search', views_manager.main, kwargs={'init': 'search', 'search': True})
]

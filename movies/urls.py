"""movies URL Configuration

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
from  django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static


from django.views.static import serve
from movies_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies_app/', include('movies_app.urls')),
    path(f'api/{settings.API_VERSION}/',include(('movies_app.api.urls','movies_app.api'), namespace='api-movies_app')),
    path('login/',views.MyLoginView.as_view(),name='mylogin'),
    path('logout/',views.MyLogoutView.as_view(),name='mylogout'),
    path('logeo/', include('django.contrib.auth.urls'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^media/(?P<path>.*)$',serve, {'document_root' : settings.MEDIA_ROOT,}),
        #path('media/<path>.*',serve,{'document_root' : settings.MEDIA_ROOT,})
    ]

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
from django.contrib import admin
from django.urls import path, include

from polls.views import MainPage

# musimy stworzyc adres dla domeny
urlpatterns = [
    path('', MainPage.as_view()),
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
]

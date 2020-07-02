from django.urls import path
from . import views

# prefix definiujemy- alias wykorzystanie polls:
app_name = 'polls'

urlpatterns = [
    # path('', views.index, name='main'),
    path('', views.IndexView.as_view(), name="main"),
    # path('<int:question_id>', views.detail, name='detail'),
    path('<int:question_id>', views.Detail.as_view(), name='detail'),
    path('<int:question_id>/vote', views.vote, name="vote"),
    path('<int:question_id>/results', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/results', views.results, name="results"),
    path('create_question', views.CreateQuestion.as_view(), name='create_question'),
    path('<int:question_id>/create_choice',
         views.CreateChoice.as_view(), name='create_choice'),
]

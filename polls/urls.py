from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),  # type: ignore
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("all/", views.all, name="all"),
    path("<int:question_id>/frequency/", views.frequency, name="frequency"),
    path("statistics/", views.statistics, name="statistics"),
    path("add_question/", views.add_question, name="add_question"),
    path("add_question2/", views.add_question2, name="add_question2"),
    path("name/", views.get_name, name="name"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
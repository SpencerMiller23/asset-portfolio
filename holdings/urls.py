from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("dashboard", views.dashboard, name='dashboard'),
    path("user_holdings", views.user_holdings, name='user_holdings'),
    path("add_position", views.add_position, name='add_position'),
    path("user_portfolio", views.user_portfolio, name='user_portfolio')
]

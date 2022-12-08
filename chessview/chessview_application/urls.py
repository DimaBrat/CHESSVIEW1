from django.urls import path
from .views import MainView, NewsView, NewsDetailView, LessonsView, LessonsDetailView, OpeningsView, OpeningsDetailView, ArticlesView, ArticlesDetailView, SignUpView, SignInView, FeedBackView, SuccessView
from django.contrib.auth.views import LogoutView
from django.conf import settings

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('news/', NewsView.as_view(), name='news'),
    path('news/<slug>/', NewsDetailView.as_view(), name='news_detail'),
    path('lessons/', LessonsView.as_view(), name='lessons'),
    path('lessons/<slug>/', LessonsDetailView.as_view(), name='lessons_detail'),
    path('openings/', OpeningsView.as_view(), name='openings'),
    path('openings/<slug>/', OpeningsDetailView.as_view(), name='openings_detail'),
    path('articles/', ArticlesView.as_view(), name='articles'),
    path('articles/<slug>/', ArticlesDetailView.as_view(), name='articles_detail'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='signout',),
    path('contact/', FeedBackView.as_view(), name='contact'),
    path('contact/success/', SuccessView.as_view(), name='success')
]
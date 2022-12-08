from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from .models import News, Lessons, Debuts, Articles, Comment
from .forms import SignUpForm, SignInForm, FeedBackForm, CommentForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail, BadHeaderError

# Вьюха для обработки главной страницы
class MainView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'chessview_application/index.html')

# Вьюха для списка новостей
class NewsView(View):
    def get(self, request, *args, **kwargs):
        news = News.objects.all()
        news = news[::-1]
        paginator = Paginator(news, 6)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'chessview_application/news.html', context={
            'page_obj': page_obj
        })

# Вьюха для страницы новости
class NewsDetailView(View):
    # В методе get мы добавили нашу форму и отправили ее в контекст для рендеринга в шаблоне
    def get(self, request, slug, *args, **kwargs):
        news = get_object_or_404(News, url=slug)
        comment_form = CommentForm()
        return render(request, 'chessview_application/post_detail.html', context={
            'news': news,
            'comment_form': comment_form
        })

    # Метод для создания комментариев
    def post(self, request, slug, *args, **kwargs):
        comment_form = CommentForm(request.POST)  # Сохраняем данные из формы комментариев
        # Если форма валидна, то мы переходим к процессу создания комментария
        if comment_form.is_valid():
            # Для этого нам нужно собрать все данные для модели Comment
            text = request.POST['text']
            username = self.request.user
            news = get_object_or_404(News, url=slug)
            # Далее в переменную comment мы сохраняем созданный нами объект в базе данных
            # Для этого мы используем QuerySet к модели Comment и метод create в который отправляем все данные комментария
            comment = Comment.objects.create(news=news, username=username, text=text)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        return render(request, 'chessview_application/post_detail.html', context={
            'comment_form': comment_form
        })

# Вьюха для списка уроков
class LessonsView(View):
    def get(self, request, *args, **kwargs):
        lessons = Lessons.objects.all()
        return render(request, 'chessview_application/lessons.html', context={
            'lessons': lessons
        })

# Вьюха для страницы урока
class LessonsDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        lessons = get_object_or_404(Lessons, url=slug)
        return render(request, 'chessview_application/lessons_post_detail.html', context={
            'lessons': lessons
        })

# Вьюха для списка дебютов
class OpeningsView(View):
    def get(self, request, *args, **kwargs):
        openings = Debuts.objects.all()
        return render(request, 'chessview_application/openings.html', context={
            'openings': openings
        })

# Вьюха для страницы дебютной лекции
class OpeningsDetailView(View):
    # В методе get мы добавили нашу форму и отправили ее в контекст для рендеринга в шаблоне
    def get(self, request, slug, *args, **kwargs):
        openings = get_object_or_404(Debuts, url=slug)
        return render(request, 'chessview_application/openings_post_detail.html', context={
            'openings': openings
        })

# Вьюха для списка статей
class ArticlesView(View):
    def get(self, request, *args, **kwargs):
        articles = Articles.objects.all()
        return render(request, 'chessview_application/articles.html', context={
            'articles': articles
        })

# Вьюха для страницы статьи
class ArticlesDetailView(View):
    # В методе get мы добавили нашу форму и отправили ее в контекст для рендеринга в шаблоне
    def get(self, request, slug, *args, **kwargs):
        articles = get_object_or_404(Articles, url=slug)
        return render(request, 'chessview_application/articles_post_detail.html', context={
            'articles': articles
        })

class SignUpView(View):
    # Метод get - запрос к серверу на получение страницы
    def get(self, request, *args, **kwargs):
        form = SignUpForm()  # Берём шаблон из формы
        return render(request, 'chessview_application/signup.html', context={
            'form': form
        })

    # POST предназначен для запроса, при котором веб-сервер принимает данные,
    # заключённые в тело сообщения, для хранения и обработки
    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)  # Cохраняем в переменную данные запроса POST, переданные через форму
        if form.is_valid():  # Проверяем форму на валидность
            user = form.save()  # Сохраняем пользователя в БД
            if user is not None:  # Проверка авторизованных данных
                login(request, user)  # Логин пользователя
                return HttpResponseRedirect('/')  # Редирект на главную после логина юзера
        return render(request, 'chessview_application/signup.html', context={
            'form': form
        })

class SignInView(View):
    # Аналогично предыдущему
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'chessview_application/signin.html', context={
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'chessview_application/signin.html', context={
            'form': form,
        })

# Вьюха для обработки формы обратной связи
class FeedBackView(View):
    def get(self, request, *args, **kwargs):
        form = FeedBackForm()
        return render(request, 'chessview_application/contact.html', context={
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = FeedBackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(f'От {name} | {from_email} | {subject}', message, from_email, ['chessview64@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Невалидный заголовок')
            return HttpResponseRedirect('success')
        return render(request, 'chessview_application/contact.html', context={
            'form': form
        })

class SuccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'chessview_application/success.html')
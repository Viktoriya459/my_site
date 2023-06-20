from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView, FormView

from .forms import AddPostForm, RegisterUserForm, LoginUserForm, ContactForm
from .models import *
from .utils import DataMixin

menu = [{'title': 'Про сайт', 'url_name': 'about'},
        {'title': 'Додати статтю', 'url_name': 'addpage'},
        {'title': 'Зворотній зв\'язок', 'url_name': 'contact'},]
        # {'title': 'Увійти', 'url_name': 'login'}]


class MovieHome(DataMixin, ListView):
    model = Movie
    template_name = 'movies/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Головна сторінка')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        return Movie.objects.filter(is_published=True).select_related('cat')


class MovieCategory(DataMixin, ListView):
    model = Movie
    template_name = 'movies/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Movie.objects.filter(cat__slug=self.kwargs['cat_slug'],
                                    is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категорія - ' + str(context['posts'][0].cat), cat_selected=context['posts'][0].cat_id)
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class ShowPost(DataMixin, DetailView):
    model = Movie
    template_name = 'movies/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'movies/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Додавання статті')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'movies/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизація')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_success_url(self):
        return reverse_lazy('home')


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'movies/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Зворотній зв\'язок')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')

# @cache
def logout_user(request):
    logout(request)
    return redirect('login')



# def index(requests):
#     posts = Movie.objects.all()
#     cats = Category.objects.all()
#     context = {'menu': menu, 'cats': cats, 'title': 'Головна сторінка', 'posts': posts, 'cat_selected': 0,}
#     return render(requests, 'movies/index.html', context=context)

def about(requests):

    contact_list = Movie.objects.all()
    paginator = Paginator(contact_list, 3)
    page_number = requests.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(requests,'movies/about.html', {'menu': menu,
                                                 'title': 'Про сайт',
                                                 'page_obj': page_obj})
# class AboutPage(DataMixin, TemplateView):
#     template_name = 'movies/about.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Про сайт')
#         context = dict(list(context.items()) + list(c_def.items()))
#
#         contact_list = Movie.objects.all()
#         paginator = Paginator(contact_list, 3)
#         page_number = self.request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#
#         context['menu'] = menu
#         context['title'] = 'Про сайт'
#         context['page_obj'] = page_obj
#         return context

# def contact(requests):
#     return HttpResponse('Зворотній зв\'язок')

# def login(requests):
#     return HttpResponse('Авторизація')

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'movies/register.html'
    success_url = reverse_lazy('login')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Реєстрація')
        # context = dict(list(context.items()) + list(c_def.items()))
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


# def show_post(requests, post_slug):
#     post = get_object_or_404(Movie, slug=post_slug)
#     context = {'menu': menu, 'post': post, 'title': post.title, 'cat_selected': post.cat_id,}
#
#     return render(requests, 'movies/post.html', context=context)

# def categories(requests, cat_id):
#     return HttpResponse(f'<h1>Фільми по категоріях</h1>{cat_id}')

# def show_category(requests, cat_id):
#     posts = Movie.objects.filter(cat_id=cat_id)
#     cats = Category.objects.all()
#
#     context = {'menu': menu, 'cats': cats, 'title': '', 'posts': posts, 'cat_selected': cat_id,}
#
#     return render(requests, 'movies/index.html', context=context)

# def addpage(request):
#     if request.method  == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # Movie.objects.create(**form.cleaned_data)
#             form.save()
#             return redirect('home')
#
#     else:
#         form = AddPostForm()
#         context = {'form': form,'menu': menu, 'title': 'Додавання статті'}
#     return render(request, 'movies/addpage.html', context=context)

def pageNotFound(requests, exception):
    return HttpResponseNotFound('<h1>Сторінку не знайдено</h1>')

# MTV патерн: Models, Views, Templates
# ORM -
# WSGI - протокол, всі додатки пайтон працюють з ним



from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import FindForm
from .models import Vacansy


def home_view(request):
    find_form = FindForm()
    return render(request, 'scraping/home.html', {'find_form': find_form})


def list_view(request):
    find_form = FindForm(request.GET or None)
    city = request.GET.get('city')
    language = request.GET.get('language')
    context = {'city': city, 'language': language, 'find_form': find_form}
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language

        qs = Vacansy.objects.filter(**_filter)
        paginator = Paginator(qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, 'scraping/list.html', context)
from django.shortcuts import render , redirect
from django.http import Http404 , HttpResponseForbidden
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404
from .serializers import *
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework import generics
from rest_framework.exceptions import ParseError
from django.contrib import messages
from googletrans import Translator
from time import sleep


def handout_sections(request):
    handouts = SectionChoice.objects.all()
    return render(request , 'Handout.html' , {
        'handouts' : handouts
        })


def all_handouts(request):
    handout_section = request.GET.get('value')
    section_choice = SectionChoice.objects.get(value = handout_section)
    handouts = Handout.objects.filter(status = 'p', section = section_choice).order_by('-create_time')
    return render(request ,'hanout_choice.html' , {
        'handouts': handouts,
        'section': section_choice
    })
    
        
def handout_detail(request):
    
    pk = request.GET.get('pk')
    
    handout_detail = get_object_or_404(Handout,pk = pk)
    previous_url = request.META.get('HTTP_REFERER', None)
    if handout_detail.status != 'p':
        return HttpResponseForbidden()

    return render(request,'handout_detail.html',{
        'handout':handout_detail,
        'previous_url' : previous_url
        })


def faq_list(request):

    faqs = SectionChoice.objects.all()
    return render(request , 'faq_sections.html' , {
        'faqs' : faqs
        })


def faq(request):
    try:
        handout_section = request.GET.get('value')
        section_choice = SectionChoice.objects.get(value = handout_section)
        
        faq = Faq.objects.filter(status = 'p',section = section_choice).order_by('-create_time')
    except Faq.DoesNotExist:
        raise Http404('سوال و جوابی موجود نیست')
    return render(request , 'faq_list.html' , {
        'faq':faq,
        'section':section_choice
    })



class FaqApiView(generics.ListCreateAPIView):
    queryset = Faq.objects.all().order_by('-id')
    serializer_class = FaqSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class FaqUpdateApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Faq.objects.all().order_by('-id')
    serializer_class = FaqSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

        
class HandoutApiView(generics.ListCreateAPIView):
    queryset = Handout.objects.all()
    serializer_class = HandoutSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class HandoutUpdateApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Handout.objects.all()
    serializer_class = HandoutSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
   
        
        
def add_new_section_choices(request):
    if request.method == 'POST':
        form = Add_new_section_choicesForm(request.POST)
        if form.is_valid():
            value = 0
            new_choice = form.cleaned_data['new_choice']
            if SectionChoice.objects.last():
                value = SectionChoice.objects.last().pk + 1
            else:
                value = 1
            SectionChoice.objects.create(value = value,display_text = new_choice)
            return redirect('/sectionchoice/List/')
    
    else:
        form = Add_new_section_choicesForm()

    return render(request, 'handout_section_create.html', {
        'form': form,
    })

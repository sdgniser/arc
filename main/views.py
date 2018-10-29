from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate

from authtools.models import User
from authtools.forms import UserCreationForm

from .models import Profile, School, Course, Itr, Item, SEMS
from .forms import *
from .helper import *

REV_DICT_SEMS = dict([i[::-1] for i in SEMS])

def index_view(request):
    school_list = School.objects.order_by('abbr')
    return render(request, 'main/index.htm', {'school_list': school_list})

def school_view(request, abbrev):
    try:
        s = School.objects.get(abbr=abbrev)
        courses = Course.objects.filter(school=s).order_by('code')
        form = CourseForm()
        return render(request, 'main/school.htm', {'sch': s, 'course_list': courses, 'form': form})
    except School.DoesNotExist:
        raise Http404("School not found")

def course_view(request, cd):
    try:
        c = Course.objects.get(code=cd)
        itrs = Itr.objects.filter(course__code=cd).order_by('year', 'sem')
        return render(request, 'main/course.htm', {'crs': c, 'itr_list': itrs})
    except Course.DoesNotExist:
        raise Http404("Course not found")

def itr_view(request, cd, yr, sea):
    try:
        s = REV_DICT_SEMS[sea].lower()
        i = Itr.objects.get(course__code = cd, year=yr, sem=s)
        items = Item.objects.filter(itr=i)
        dmn = get_current_site(request).domain
        return render(request, 'main/itr.htm', {'itr': i, 'item_list': items, dmn: 'dmn'})
    except Itr.DoesNotExist:
        Http404('Page not found')

from django import forms
class EmailForm(forms.Form):
    email = forms.EmailField()

def signup(request):
    if request.method == 'POST':

        emailForm = EmailForm(request.POST)
        if emailForm.is_valid():
            try:
                u = User.objects.get(email=emailForm.cleaned_data['email'])
            except User.DoesNotExist:
                u = None
            if u and not u.is_active:
                u.delete()

        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.is_valid()
            user = form.save(commit=False)
            user.is_active = False

            uvid = genVID(user.email)
            ip = getIP(request)
            user.save()
            user.profile.ip = ip
            user.profile.vid = uvid
            user.save()
            
            # Verification email
            subj = 'Verification of email address - NISER Archive'
            dmn = get_current_site(request).domain
            htm = render_to_string('main/verify.htm', {'user': user, 'vid': uvid, 'dmn': dmn})
            txt = render_to_string('main/verify.txt', {'user': user, 'vid': uvid, 'dmn': dmn})
            mfrom = 'code@niser.ac.in'
            mto = user.email
            msg = EmailMultiAlternatives(subj, txt, mfrom, [mto])
            #msg.attach_alternative(htm, 'text/html')
            msg.send()
            #send_mail(subj, txt, 'code@niser.ac.in', [mto], html_message=htm)
            return HttpResponse('We have sent an email. Please confirm your email address to complete the registration')
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.htm', {'form': form})

def verify(request, uid, vid):
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        user = None
    if user is not None and user.profile.vid == vid:
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def add_item(request, cd, yr, sea):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user is not None:
                i = Itr.objects.get(course__code=cd, year=yr, sem=REV_DICT_SEMS[sea])
                item = form.save(commit=False)
                item.op = request.user
                item.itr = i
                item.save()
                return HttpResponse('File uploaded successfully.')
            else:
                return HttpResponse('User is none')
    else:
        form = ItemForm()
    return render(request, 'main/add.htm', {'form': form})

def add_itr(request, cd):
    c = Course.objects.get(code=cd)
    if request.method == 'POST':
        form = ItrForm(request.POST)
        if form.is_valid():
            if request.user is not None:
                itr =  form.save(commit=False)
                itr.op = request.user
                itr.course = c
                itr.save()
                return HttpResponse('Iteration added successfully')
            else:
                return HttpResponse('User is none')
    else:
        form = ItrForm()
    return render(request, 'main/add-itr.htm', {'crs': c, 'form': form})

def add_crs(request, abbrev):
    s = School.objects.get(abbr=abbrev)
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            if request.user is not None:
                crs =  form.save(commit=False)
                crs.code = crs.code.lower()
                crs.op = request.user
                crs.school = s
                crs.save()
                return render(request, 'main/add-crs.htm', {'crs': crs, 'success': True})
            else:
                return HttpResponse('User is none')
    else:
        form = CourseForm()
    return render(request, 'main/add-crs.htm', {'sch': s, 'form': form})

from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.urls import reverse
from django.views import generic
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.db import models

from urllib.parse import urlencode

from authtools.models import User
from authtools.forms import UserCreationForm

from .models import Profile, School, Course, Itr, Item, SEMS
from .forms import *
from .helper import *

import datetime

REV_DICT_SEMS = dict([i[::-1] for i in SEMS])

def index_view(request):
    school_list = School.objects.order_by('abbr')
    return render(request, 'main/index.htm', {'school_list': school_list})

def school_view(request, abbrev):
    try:
        s = School.objects.get(abbr__iexact=abbrev)
        courses = Course.objects.filter(school=s, appr=True).order_by('code')
        form = CourseForm()
        return render(request, 'main/school.htm', {'sch': s, 'course_list': courses, 'form': form})
    except School.DoesNotExist:
        raise Http404("School not found")

def course_view(request, cd):
    try:
        form = None
        if request.user is not None:
            form = ItrForm()
        c = Course.objects.get(code=cd)
        itrs = Itr.objects.filter(course__code=cd, appr=True).order_by('year', 'sem')
        return render(request, 'main/course.htm', {'crs': c, 'itr_list': itrs, 'form': form})
    except Course.DoesNotExist:
        raise Http404("Course not found")

def itr_view(request, cd, yr, sea):
    try:
        s = REV_DICT_SEMS[sea.title()]
        i = Itr.objects.get(course__code = cd, year=yr, sem=s)
        items = Item.objects.filter(itr=i)
        comments = Comment.objects.filter(itr=i, vis=True)
        form = None
        form2 = CommentReportForm()
        form3 = ItemReportForm()
        if request.user is not None:
            form = CommentForm()
        return render(request, 'main/itr.htm', {
            'itr': i,
            'item_list': items,
            'comm_list': comments,
            'form': form,
            'report_form': form2,
            'item_report_form': form3
            })
    except Itr.DoesNotExist:
        raise Http404('No such iteration was found')

def user_view(request, uid):
    try:
        u = User.objects.get(id = uid)
        u2 = request.user
        if request.method == 'POST':
            if u2 is not None and u2.is_authenticated and u == u2:
                form = ProfileForm(request.POST, instance=u.profile)
                pro = form.save(commit=False)
                pro.upd = True
                pro.save()
                return render(request, 'main/user.htm', {'user_page': u, 'form': form})
            else:
                return HttpResponse('You shouldn\'t be here')
        if request.user.is_authenticated:
            if u == u2:
                form = ProfileForm()
                return render(request, 'main/user.htm', {'user_page': u, 'form': form})
            form = UserReportForm()
            return render(request, 'main/user.htm', {'user_page': u, 'report_form': form})
        return render(request, 'main/user.htm', {'user_page': u})
    except (User.DoesNotExist, ValueError):
        # ValueError will occur when someone tries /u/asdf (since asdf cannot be parsed as
        # an integer)
        raise Http404('User not found')

def add_comment(request, cd, yr, sea):
    url = reverse('itr', args=[cd, yr, sea])
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if request.user is not None:
                comm =  form.save(commit=False)
                comm.user = request.user
                s = REV_DICT_SEMS[sea.title()]
                i = Itr.objects.get(course__code = cd, year=yr, sem=s)
                comm.itr = i
                comm.save()
                return redirect(url)
                return render(request, 'main/itr.htm', {'crs': c, 'itr': itr, 'success': True})
            else:
                return HttpResponse('User is none')

def delete_comment(request, cid):
    c = Comment.objects.get(id = cid)
    if request.user == c.user:
        c.vis = False
        c.save()
        return HttpResponse('<div class="alert alert-success"> Comment successfully deleted </div>')

from django import forms
class EmailForm(forms.Form):
    email = forms.EmailField()

def signup(request):
    if request.user is not None and request.user.is_authenticated:
        return redirect('/?su=li')
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
            dmn = get_current_site(request).domain + '/arc'
            htm = render_to_string('main/verify.htm', {'user': user, 'vid': uvid, 'dmn': dmn})
            txt = render_to_string('main/verify.txt', {'user': user, 'vid': uvid, 'dmn': dmn})
            mfrom = 'NISER Archive'
            mto = user.email
            msg = EmailMultiAlternatives(subj, txt, mfrom, [mto])
            #msg.attach_alternative(htm, 'text/html')
            msg.send()
            #send_mail(subj, txt, 'code@niser.ac.in', [mto], html_message=htm)
            base_url = reverse('home')
            query_string =  urlencode({'su': True})
            url = '{}?{}'.format(base_url, query_string)
            return redirect(url)
            #return HttpResponse('We have sent an email. Please confirm your email address to complete the registration')
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
        base_url = reverse('home')
        query_string =  urlencode({'ver': True})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)
        #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def add_item(request, cd, yr, sea):
    i = Itr.objects.get(course__code=cd, year=yr, sem=REV_DICT_SEMS[sea.title()])
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user is not None:
                item = form.save(commit=False)
                item.op = request.user
                item.itr = i
                item.save()
                return render(request, 'main/add-item.htm', {'itr': i, 'item': item, 'success': True})
            else:
                return HttpResponse('User is none')
    else:
        form = ItemForm()
    return render(request, 'main/add-item.htm', {'itr': i, 'form': form})

def add_itr(request, cd):
    c = Course.objects.get(code=cd)
    if request.method == 'POST':
        form = ItrForm(request.POST)
        if form.is_valid():
            if request.user is not None:
                itr =  form.save(commit=False)
                itr.op = request.user
                itr.course = c
                try:
                    i = Itr.objects.get(course=c, sem=itr.sem, year=itr.year)
                    return render(request, 'main/add-itr.htm',
                            {'exists': True, 'crs': c, 'itr': itr})
                except Itr.DoesNotExist:
                    itr.save()
                    return render(request, 'main/add-itr.htm', {'crs': c, 'itr': itr, 'success': True})
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
                cd = form.cleaned_data['code'].lower()
                try:
                    crs = Course.objects.get(code=cd)
                    return render(request, 'main/add-crs.htm',
                            {'exists': True, 'crs': crs})
                except Course.DoesNotExist:
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

def file_view(request, fname):
    try:
        i = Item.objects.get(fl = fname)
        return render(request, 'main/file.htm', {'item': i})
    except Item.DoesNotExist:
        raise Http404("File not found")

def report_comment(request, cid):
    if request.method == 'POST':
        rep_form = CommentReportForm(request.POST)
        if rep_form.is_valid():
            if request.user is not None:
                try:
                    c = Comment.objects.get(id=cid)
                    rep = rep_form.save(commit=False)
                    rep.user = request.user
                    rep.comment = c
                    rep.save()
                    return HttpResponse('<div class="alert alert-success"> Report submitted successfully. Thanks. </div>')
                except Comment.DoesNotExist:
                    raise Http404('Comment Not Found')
            return HttpResponse('User is none')
    return HttpResponse('You shouldn\'t be here.')

def report_item(request, iid):
    if request.method == 'POST':
        rep_form = ItemReportForm(request.POST)
        if rep_form.is_valid():
            if request.user is not None:
                try:
                    i = Item.objects.get(id=iid)
                    rep = rep_form.save(commit=False)
                    rep.user = request.user
                    rep.item = i
                    rep.save()
                    return HttpResponse('<div class="alert alert-success"> Report submitted successfully. Thanks. </div>')
                except Item.DoesNotExist:
                    raise Http404('File Not Found')
            return HttpResponse('User is none')
    return HttpResponse('You shouldn\'t be here.')

def report_user(request, uid):
    if request.method == 'POST':
        rep_form = UserReportForm(request.POST)
        if rep_form.is_valid():
            if request.user is not None:
                try:
                    u = User.objects.get(id=uid)
                    rep = rep_form.save(commit=False)
                    rep.user = request.user
                    rep.target = u
                    rep.save()
                    return HttpResponse('<div class="alert alert-success"> Report submitted successfully. Thanks. </div>')
                except User.DoesNotExist:
                    raise Http404('User Not Found')
            return HttpResponse('User is none')
    return HttpResponse('You shouldn\'t be here.')

def faq(request):
    return render(request, 'main/faq.htm')

def log_view(request):

    recent_uploads = Item.objects.all().order_by('-id')[:20]
    t2 = timezone.now()
    for item in recent_uploads:
        if item.time != None:
            t1 = item.time
            delta = t2 - t1
            item.when = readableDuration(delta.total_seconds())
        else:
            item.when = ''

    recent_comments = Comment.objects.all().order_by('-id')[:20]
    for comment in recent_comments:
        t1 = comment.posted
        t2 = timezone.now()
        delta = t2 - t1
        comment.when = readableDuration(delta.total_seconds())

    top_uploaders = Item.objects.values('op').annotate(models.Count('id')).order_by('-id__count')[:10]
    for i in range(len(top_uploaders)):
        top_uploaders[i]['pos'] = i+1
        top_uploaders[i]['op'] = User.objects.get(id=top_uploaders[i]['op'])

    uploads_this_month = Item.objects.filter(time__month = t2.month)
    top_recent_uploaders = uploads_this_month.values('op').annotate(models.Count('id')).order_by('-id__count')[:3]
    for i in range(len(top_recent_uploaders)):
        top_recent_uploaders[i]['pos'] = i+1
        top_recent_uploaders[i]['op'] = User.objects.get(id=top_recent_uploaders[i]['op'])
   
    # set it to be None if the query set is empty, so that we can catch it in the template
    # is there a better way to do this?
    #if len(top_recent_uploaders) == 0:
    #    top_recent_uploaders = None
    
    return render(request, 'main/log.htm', {
        'recent_uploads': recent_uploads,
        'recent_comments': recent_comments,
        'top_uploaders': top_uploaders,
        'top_recent_uploaders': top_recent_uploaders
        })

def error404(request, exception):
    return render(request, 'main/404.htm', {'exp': exception}, status=404)

def error500(request, exception):
    return render(request, 'main/500.htm', {'exp': exception}, status=500)

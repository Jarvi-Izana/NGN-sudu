from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import PersonalInfo, ProjectInfo
from django.utils import timezone
from django.http import HttpResponse, Http404, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index(request):
    return render(request, 'index.html')

def detail(request):
    return render(request, 'db_manager/howtouse.html')

def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# correct. the key word for querying is the project_name
@csrf_exempt
def group_member(request):
    if request.method == 'POST':
        try:
            email_addr = request.POST['email_addr']
            project_name = request.POST['project_name']
        except KeyError:
            return HttpResponseNotAllowed('')
        try:
            user = PersonalInfo.objects.get(email_addr=email_addr)
            status = user.status
        except PersonalInfo.DoesNotExist:
            return HttpResponseNotAllowed('')
        if status:
            people = ProjectInfo.objects.filter(project_name=project_name)
            if not people:
                return HttpResponse('ERROR: NO SUCH PROJECT')
            msg = ''
            try:
                for person in people:
                    try:
                        msg += '{0},{1},{2},{3},'.format(person.email_addr, person.user_name, person.project_status,
                                                PersonalInfo.objects.get(email_addr__exact=person.email_addr).token)
                    except PersonalInfo.DoesNotExist:
                        continue
                return HttpResponse(msg[:-1])
            except IndexError:
                raise Http404
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponseNotAllowed('NOT LOGIN')
    else:
        # reverse the format of the web.
        ip = get_ip(request)
        return HttpResponse('<h1>Test Page</h1> <p>ERROR: METHOD POST EXPECTED--CLIENT@'+str(ip)+'</p>')


# each person at least have one project. and use this API to trace his project.
# correct
@csrf_exempt
def personal_project(request):
    if request.method == 'POST':
        user = PersonalInfo.objects.get(email_addr=request.POST['email_addr'])
        if user.status:
            user = user.personalproject_set.all()
            msg = ''
            for item in user:
                msg += item.project_name + ','
            # tail the last comma
            if not msg:
                return  HttpResponse(msg[:-1])
            else:
                return HttpResponse(msg)
        else:
            return HttpResponseNotAllowed('')
    else:
        raise Http404('ERROR: METHOD POST EXPECTED')

# correct
@csrf_exempt
def register_with_project(request):
    if request.method == 'POST':
        try:
            user_name=request.POST['user_name']
            email_addr=request.POST['email_addr']
            password=request.POST['password']
            token=request.POST['token']
            project_name=request.POST['project_name']
        except KeyError:
            return HttpResponse('ERROR: LACK ATTRIBUTE IN JSON')
        else:
            try:
                check = PersonalInfo.objects.get(email_addr=email_addr)
                if check:
                    return HttpResponse('ERROR: USER ALREADY REGISTERED')
            except ObjectDoesNotExist:
                user = PersonalInfo(email_addr=email_addr, password=password, user_name=user_name,
                            status=True, token=token, time=timezone.now())
                user.save()
                user.personalproject_set.create(project_name=project_name)
                ProjectInfo(email_addr=email_addr, user_name=user_name,
                            project_name=project_name).save()
                return HttpResponse('OK: SUCCESSFULLY REGISTERED')
    else:
        raise Http404('ERROR: METHOD POST EXPECTED')

#
@csrf_exempt
def unregister(request):
    if request.method == 'POST':
        try:
            email_addr = request.POST['email_addr']
            password = request.POST['password']
        except KeyError:
            return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'],content='NOT ALLOWED')
        user = get_object_or_404(PersonalInfo, email_addr=email_addr, password=password)
        if user.status:
            user.delete()
        else:
            return HttpResponseNotAllowed('NOT ALLOWED')
        user = ProjectInfo.objects.filter(email_addr=email_addr)
        if user:
            for u in user:
                u.delete()
        return HttpResponse('USER DELETED '+email_addr)


# add project for one person at a time, the entry (email, project_name) should be unique.
#
@csrf_exempt
def add_project(request):
    if request.method == 'POST':
        try:
            email_addr = request.POST['email_addr']
            project_name = request.POST['project_name']
        except KeyError:
            return HttpResponseNotAllowed('NOT ALLOWED')
        if ProjectInfo.objects.filter(email_addr=email_addr, project_name=project_name):
            return HttpResponseNotAllowed()
        user = get_object_or_404(PersonalInfo, email_addr=email_addr)
        user.personalproject_set.create(project_name=project_name)
        ProjectInfo(email_addr=email_addr, user_name=user.user_name,
                    project_name=project_name).save()
        return HttpResponse('PROJECT ADDED: '+project_name)
    else:
        # 405
        return HttpResponseNotAllowed('ERROR: METHOD POST EXPECTED')

# correct
@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            user_name=request.POST['user_name']
            password = request.POST['password']
            user = get_object_or_404(PersonalInfo ,user_name=user_name, password=password)
            user.status = True
            user.save()
            return HttpResponse('login')
        except KeyError:
            try:
                email_addr = request.POST['email_addr']
                password = request.POST['password']
                user = get_object_or_404(PersonalInfo, email_addr=email_addr, password=password)
                user.status = True
                user.save()
                return HttpResponse('LOGIN SUCCESSFULLY')
            except KeyError:
                return Http404()
    else:
        raise Http404('ERROR: METHOD POST EXPECTED')

# correct
@csrf_exempt
def logout(request):
    if request.method == 'POST':
        try:
            email_addr = request.POST['email_addr']
            password = request.POST['password']
        except KeyError:
            raise Http404()
        user = get_object_or_404(PersonalInfo, email_addr=email_addr, password=password)
        user.status = False
        user.save()
        return HttpResponse('LOGOUT')
    else:
        raise Http404('ERROR: METHOD POST EXPECTED')

# correct
@csrf_exempt
def finish(request):
    if request.method == 'POST':
        try:
            email_addr = request.POST['email_addr']
            project_name = request.POST['project_name']
            password = request.POST['password']
        except KeyError:
            raise Http404()
        if get_object_or_404(PersonalInfo, email_addr=email_addr, password=password).status:
            user = get_object_or_404(ProjectInfo, email_addr=email_addr, project_name=project_name)
            user.project_status = True
            user.save()
            return HttpResponse('Project Status Update')
    else:
        raise Http404('ERROR: METHOD POST EXPECTED')


# correct
@csrf_exempt
def quit_project(request):
    if request.method == 'POST':
        try:
            email_addr=request.POST['email_addr']
            project_name=request.POST['project_name']
        except KeyError:
            raise Http404('FORMAT ERROR')
        user = get_object_or_404(PersonalInfo, email_addr=email_addr)
        print(user.email_addr)
        if user.status:
            try:
                ProjectInfo.objects.get(email_addr=email_addr, project_name=project_name).delete()
            except ProjectInfo.DoesNotExist:
                return HttpResponse('NO SUCH PROJECT NAMED: '+project_name)
            user.personalproject_set.get(project_name=project_name).delete()
            return HttpResponse('SUCCESSFULLY QUIT '+project_name)
        else:
            return HttpResponseNotAllowed('INVALID PROCESSION')
    else:
        return HttpResponse('<h1>method quit_project</h1>')






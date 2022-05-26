import datetime
from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.
from core.forms import LoginForm, TeacherregForm, StudentForm, TimeTableForm, NotificationForm, FeedbackForm
from core.models import teacherreg, Login, Student, Attendance, TimeTable, Notification, Feedback


def home(request):
    return render(request,'index.html')

def loginview(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('adminview')
            elif user.is_teacher:
                return redirect('teacherhome')
            elif user.is_student:
                return redirect('studenthome')

        else:
            messages.info(request, 'invalid credentials')
    return render(request,'login.html')

@login_required(login_url='loginview')
def adminview(request):
    return render(request,'adminpannel/adminhome.html')

@login_required(login_url='loginview')
def teacherregister(request):
    login_form = LoginForm()
    teacher_form = TeacherregForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        teacher_form = TeacherregForm(request.POST)
        if login_form.is_valid() and teacher_form.is_valid():
            user = login_form.save(commit=False)
            user.is_teacher = True
            user.save()
            s = teacher_form.save(commit=False)
            s.user = user
            s.save()
            messages.info(request, 'teacher registered successfully')
            return redirect('teacherview')
    return render(request,'adminpannel/teacherregister.html',{'login_form':login_form,'teacher_form':teacher_form})

@login_required(login_url='loginview')
def teacherview(request):
    Tr = teacherreg.objects.all()
    return render(request, 'adminpannel/teacherview.html', {'Tr': Tr})

@login_required(login_url='loginview')
def teacherupdate(request,id):
    tchr = teacherreg.objects.get(id=id)
    t=Login.objects.get(teacher=tchr)
    if request.method=='POST':
        form=TeacherregForm(request.POST or None,instance=tchr)
        login_form=LoginForm(request.POST or None,instance=t)
        if form.is_valid() and login_form.is_valid():
            form.save()
            login_form.save()
            messages.info(request,'student updated successfully')
            return redirect('teacherview')
    else:
        form=TeacherregForm(instance=tchr)
        login_form=LoginForm(instance=t)
    return render(request,'adminpannel/teacherupdate.html',{'form':form,'login_form':login_form})
def teacherdelete(request,id):
    tchr = teacherreg.objects.get(id=id)
    t = Login.objects.get(teacher=tchr)
    if request.method == 'POST':
        t.delete()
        return redirect('teacherview')
    else:
        return redirect('teacherview')
def logoutview(request):
    logout(request)
    return redirect('loginview')

@login_required(login_url='loginview')
def teacherhome(request):
    return render(request,'teacher/teacherhome.html')

@login_required(login_url='loginview')
def studentregister(request):
    login_form = LoginForm()
    student_form = StudentForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        student_form = StudentForm(request.POST)
        if login_form.is_valid() and student_form.is_valid():
            user = login_form.save(commit=False)
            user.is_student = True
            user.save()
            s = student_form.save(commit=False)
            s.user = user
            s.save()
            messages.info(request, 'student registered successfully')
            return redirect('studentview')
    return render(request, 'teacher/studentregister.html', {'login_form': login_form, 'student_form': student_form})

@login_required(login_url='loginview')
def studentview(request):
    stud=Student.objects.all()
    return render(request,'teacher/studentview.html',{'stud':stud})

@login_required(login_url='loginview')
def studentupdate(request,id):
    stud=Student.objects.get(id=id)
    s=Login.objects.get(student=stud)
    if request.method == 'POST':
        form=StudentForm(request.POST or None,instance=stud)
        login_form=LoginForm(request.POST or None,instance=s)
        if form.is_valid() and login_form.is_valid():
            form.save()
            login_form.save()
            messages.info(request,'student updated successfully')
            return redirect('studentview')
    else:
        form=StudentForm(instance=stud)
        login_form=LoginForm(instance=s)
    return render(request,'teacher/studentupdate.html',{'form':form,'login_form':login_form})

@login_required(login_url='loginview')
def studentdelete(request,id):
    stud=Student.objects.get(id=id)
    s=Login.objects.get(student=stud)
    if request.method=='POST':
        s.delete()
        return redirect('studentview')
    else:
        return redirect('studentview')

@login_required(login_url='loginview')
def studenthome(request):
    return render(request,'student/studenthome.html')

@login_required(login_url='loginview')
def viewprofile(request):
    p= request.user
    profile=Student.objects.filter(user=p)
    return render(request,'student/studprofile.html',{'profile':profile})

@login_required(login_url='loginview')
def studteacherview(request):
    Tr = teacherreg.objects.all()
    return render(request, 'student/studteacherview.html', {'Tr': Tr})

@login_required(login_url='loginview')
def Attendance_stud(request):
    student = Student.objects.all()
    return render(request, 'teacher/attendance.html', {'student': student})

now = datetime.datetime.now()

@login_required(login_url='loginview')
def mark(request,id):
    user=Student.objects.get(id=id)
    att=Attendance.objects.filter(student=user,date=datetime.date.today())
    if att.exists():
        messages.info(request,'Todays attendance is already marked')
        return redirect('Attendance_stud')
    else:
        if request.method=='POST':
            attndc= request.POST.get('attendance')
            Attendance(student=user, date=datetime.date.today(), attendance=attndc, time=now.time()).save()
            messages.info(request, "Attendance added successfully")
            return redirect('Attendance_stud')
        return render(request,'teacher/std_attendance.html')
@login_required(login_url='loginview')
def viewattendance(request):
    value_list=Attendance.objects.values_list('date',flat=True).distinct()
    attendance = {}
    for value in value_list:
        attendance[value] = Attendance.objects.filter(date=value)
    return render(request,'teacher/viewattendance.html',{'attendance':attendance})
@login_required(login_url='loginview')
def dayattendance(request,date):
        attendance=Attendance.objects.filter(date=date)
        context = {'attendance': attendance, 'date': date}
        return render(request,'teacher/dayattendanceview.html',context)
@login_required(login_url='loginview')
def addtimetable(request):
    form=TimeTableForm()
    if request.method =='POST':
        form = TimeTableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewtimetable')

    return render(request,'adminpannel/addtimetable.html',{'form':form})
@login_required(login_url='loginview')
def viewtimetable(request):
    tmtbl = TimeTable.objects.all()
    return render(request, 'adminpannel/viewtimetable.html', {'tmtbl': tmtbl})
@login_required(login_url='loginview')
def timetabledelete(request,id):
    ttbl=TimeTable.objects.get(id=id)

    if request.method=='POST':
        ttbl.delete()
        return redirect('viewtimetable')
    else:
        return redirect('viewtimetable')

@login_required(login_url='loginview')
def std_viewtimetable(request):
    tmtbl = TimeTable.objects.all()
    return render(request, 'student/std_viewtimetable.html', {'tmtbl': tmtbl})
@login_required(login_url='loginview')
def notification(request):
    form = NotificationForm()
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewnotification')
    return render(request, 'teacher/notification.html', {'form': form})
@login_required(login_url='loginview')
def viewnotification(request):
    noti = Notification.objects.all()
    return render(request, 'teacher/viewnotification.html', {'noti': noti})
@login_required(login_url='loginview')
def notificationdelete(request,id):
    noti= Notification.objects.get(id=id)
    if request.method == 'POST':
        noti.delete()
        return redirect('viewnotification')
    else:
        return redirect('viewnotification')

@login_required(login_url='loginview')
def std_viewnotification(request):
    noti = Notification.objects.all()
    return render(request, 'student/std_viewnotification.html', {'noti': noti})
def tchr_timetableview(request):
    tmtbl = TimeTable.objects.all()
    return render(request, 'student/std_viewtimetable.html', {'tmtbl': tmtbl})
def feedback(request):
   feed =FeedbackForm()
   if request.method=='POST':
       feed=FeedbackForm(request.POST)
       if feed.is_valid():
           feed.save()
           return redirect('feedbackview')
   return render(request,'teacher/feedback.html',{'feed': feed})
def feedbackview(request):
    feed = Feedback.objects.all()
    return render(request, 'teacher/feedbackview.html', {'feed':feed})
def ad_feedbackview(request):
    feed = Feedback.objects.all()
    return render(request, 'adminpannel/ad_feedbackview.html', {'feed': feed})
def replyfeed(request,id):
    adreply = Feedback.objects.get(id=id)
    if request.method == 'POST':
        r=request.POST.get('reply')
        adreply.reply = r
        adreply.save()
        messages.info(request,'reply send for feedback')
        return redirect('ad_feedbackview')
    return render(request,'adminpannel/replyfeed.html',{'adreply':adreply})
def tr_replyview(request):
    feed = Feedback.objects.all()
    return render(request, 'teacher/tr_replyview.html',{'feed': feed})
def stud_viewattendance(request):
    value_list = Attendance.objects.values_list('date', flat=True).distinct()
    attendance = {}
    for value in value_list:
        attendance[value] = Attendance.objects.filter(date=value)
    return render(request, 'student/stud_viewattendance.html', {'attendance': attendance})
def stud_dayattendance(request,date):
    attendance = Attendance.objects.filter(date=date)
    context = {'attendance': attendance, 'date': date}
    return render(request, 'student/stud_dayattendance.html', context)


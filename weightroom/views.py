from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Member, Usage, Checklist, UsageTime
from .forms import MemberCreationForm, ChecklistForm, UsageTimeForm, LoginForm
from django.utils import timezone
from django.utils import timezone
from datetime import timedelta
from .forms import MemberCreationForm
from django.utils import timezone

def is_manager(user):
    return user.is_staff


def home(request):
    context = {}
    if request.user.is_authenticated:
        member = request.user
        context['member'] = member
        context['warnings'] = member.accumulated_warnings
        context['current_fine'] = member.fine
        context['overdue_fine'] = member.unpaid_fine

        # 현재 사용 중인 사용자가 있는지 확인
        current_usage = Usage.objects.filter(usage_time__end_time__gt=timezone.now().time()).first()
        context['gym_status'] = '사용중' if current_usage else '사용가능'
        context['status_color'] = 'red' if current_usage else 'green'

    return render(request, 'weightroom/home.html', context)


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        student_number = request.POST['student_number']
        password = request.POST['password']
        user = authenticate(request, username=student_number, password=password)
        if user is not None:
            login(request, user)
            return redirect('weightroom:home')
        else:
            return render(request, 'weightroom/login.html', {'error': '비밀번호가 틀렸습니다.'})
    return render(request, 'weightroom/login.html')

def logout_view(request):
    logout(request)
    return redirect('weightroom:home')

def register(request):
    if request.method == 'POST':
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('weightroom:home')  # 'weightroom:home'으로 수정
    else:
        form = MemberCreationForm()
    return render(request, 'weightroom/register.html', {'form': form})


@login_required
def checklist(request):
    checklist, created = Checklist.objects.get_or_create(member=request.user)
    if request.method == 'POST':
        form = ChecklistForm(request.POST, instance=checklist)
        if form.is_valid():
            form.save()
            messages.success(request, '체크리스트가 저장되었습니다.')
            return redirect('weightroom:home')
    else:
        form = ChecklistForm(instance=checklist)

    field_names = ['원판_청소', '바벨_청소', '벤치_청소', '덤벨_청소', '싯업보드_청소', '비상문_확인', '소등']

    return render(request, 'weightroom/checklist.html', {'form': form, 'field_names': field_names})

from django.utils import timezone
from datetime import datetime, time

from django.utils import timezone
from datetime import datetime, time, timedelta

@login_required
def usage_time(request):
    member = request.user
    now = timezone.now()
    current_usage = Usage.objects.filter(
        member=member,
        usage_time__start_time__lte=now.time(),
        usage_time__end_time__gt=now.time(),
        usage_date=now.date()
    ).first()

    if request.method == 'POST':
        if 'extend' in request.POST and current_usage:
            end_time = datetime.combine(now.date(), current_usage.usage_time.end_time)
            end_time = timezone.make_aware(end_time)
            if end_time - now <= timedelta(minutes=10):
                new_end_time = end_time + timedelta(minutes=30)
                current_usage.usage_time.end_time = new_end_time.time()
                current_usage.usage_time.save()
                messages.success(request, '사용 시간이 30분 연장되었습니다.')
        elif 'start' in request.POST and not current_usage:
            end_time = now + timedelta(hours=1)
            usage_time = UsageTime.objects.create(start_time=now.time(), end_time=end_time.time())
            Usage.objects.create(member=member, usage_time=usage_time, usage_date=now.date())
            messages.success(request, '사용 시간이 시작되었습니다.')
        elif 'end' in request.POST and current_usage:
            current_usage.usage_time.end_time = now.time()
            current_usage.usage_time.save()
            messages.success(request, '사용이 종료되었습니다.')

        return redirect('weightroom:usage_time')

    return render(request, 'weightroom/usage_time.html', {'current_usage': current_usage})

@login_required
@user_passes_test(is_manager)
def manager_dashboard(request):
    members = Member.objects.all()
    recent_usages = Usage.objects.order_by('-usage_date')[:10]

    return render(request, 'weightroom/manager_dashboard.html', {
        'members': members,
        'recent_usages': recent_usages
    })
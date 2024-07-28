from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
class Member(AbstractUser):
    student_number = models.IntegerField(unique=True)
    year = models.IntegerField(null=True, blank=True)
    fine = models.IntegerField(default=0)
    unpaid_fine = models.IntegerField(default=0)
    accumulated_warnings = models.IntegerField(default=0)
    total_usage_time = models.IntegerField(default=0)
    latest_usage_time = models.CharField(max_length=11, default='')
    using_now = models.IntegerField(default=0)
    total_fine = models.IntegerField(default=0)

    # AbstractUser의 필드를 명시적으로 포함
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'student_number'
    REQUIRED_FIELDS = ['year']  # 'student_number'를 여기서 제거

    def __str__(self):
        return f"{self.username} ({self.student_number})"

    class Meta:
        db_table = 'weightroom_member'

class Manager(models.Model):
    student_number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"Manager {self.name} ({self.student_number})"

class UsageTime(models.Model):
    start_time = models.TimeField(primary_key=True)
    end_time = models.TimeField(null=False)
    extended_time = models.IntegerField(null=True)
    name = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(extended_time__lte=30), name='extended_time_lte_30')
        ]

    def __str__(self):
        return f"Usage from {self.start_time} to {self.end_time}"

from django.db import models
from django.utils import timezone
class Usage(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    usage_time = models.ForeignKey(UsageTime, on_delete=models.CASCADE)
    usage_date = models.DateField(null=False)
    created_at = models.DateTimeField(default=timezone.now)  # 새로운 필드 추가

    class Meta:
        ordering = ['-created_at']  # 최신 생성 순으로 정렬
        unique_together = ('member', 'usage_time')

    def __str__(self):
        return f"{self.member} used on {self.usage_date} at {self.usage_time} (Created: {self.created_at})"



from django.db import models
from django.utils import timezone

class Checklist(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, primary_key=True, related_name='checklist')
    created_at = models.DateTimeField(default=timezone.now)  # 새로운 필드 추가
    updated_at = models.DateTimeField(auto_now=True)  # 새로운 필드 추가
    원판_청소 = models.CharField(max_length=3, choices=[('예', '예'), ('아니오', '아니오')], default='아니오')
    바벨_청소 = models.CharField(max_length=3, choices=[('예', '예'), ('아니오', '아니오')], default='아니오')
    벤치_청소 = models.CharField(max_length=3, choices=[('예', '예'), ('아니오', '아니오')], default='아니오')
    덤벨_청소 = models.CharField(max_length=3, choices=[('예', '예'), ('아니오', '아니오')], default='아니오')
    싯업보드_청소 = models.CharField(max_length=3, choices=[('예', '예'), ('아니오', '아니오')], default='아니오')
    비상문_확인 = models.CharField(max_length=3, choices=[('예', '예'), ('아니오', '아니오')], default='아니오')
    소등 = models.CharField(max_length=3, choices=[('예', '예'), ('아니오', '아니오')], default='아니오')
    원판_파손 = models.BooleanField(default=False)
    바벨_파손 = models.BooleanField(default=False)
    벤치_파손 = models.BooleanField(default=False)
    덤벨_파손 = models.BooleanField(default=False)
    싯업보드_파손 = models.BooleanField(default=False)
    비상문_파손 = models.BooleanField(default=False)
    소등_파손 = models.BooleanField(default=False)
    요구_및_불편사항 = models.TextField(blank=True)

    def __str__(self):
        return f"체크리스트 for {self.member} (마지막 업데이트: {self.updated_at})"

    class Meta:
        ordering = ['-updated_at']  # 최신 업데이트 순으로 정렬
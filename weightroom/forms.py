from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Member, Checklist, UsageTime

class MemberCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Member
        fields = UserCreationForm.Meta.fields + ('student_number', 'year')

    def clean_student_number(self):
        student_number = self.cleaned_data.get('student_number')
        if not isinstance(student_number, int):
            raise forms.ValidationError("학번은 숫자여야 합니다.")
        return student_number

from django import forms
from .models import Checklist

class ChecklistForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = ['원판_청소', '바벨_청소', '벤치_청소', '덤벨_청소', '싯업보드_청소', '비상문_확인', '소등',
                  '원판_파손', '바벨_파손', '벤치_파손', '덤벨_파손', '싯업보드_파손', '비상문_파손', '소등_파손', '요구_및_불편사항']
        widgets = {
            '원판_청소': forms.RadioSelect(choices=[('예', '예'), ('아니오', '아니오')]),
            '바벨_청소': forms.RadioSelect(choices=[('예', '예'), ('아니오', '아니오')]),
            '벤치_청소': forms.RadioSelect(choices=[('예', '예'), ('아니오', '아니오')]),
            '덤벨_청소': forms.RadioSelect(choices=[('예', '예'), ('아니오', '아니오')]),
            '싯업보드_청소': forms.RadioSelect(choices=[('예', '예'), ('아니오', '아니오')]),
            '비상문_확인': forms.RadioSelect(choices=[('예', '예'), ('아니오', '아니오')]),
            '소등': forms.RadioSelect(choices=[('예', '예'), ('아니오', '아니오')]),

        }

class UsageTimeForm(forms.ModelForm):
    class Meta:
        model = UsageTime
        fields = ['start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

class LoginForm(forms.Form):
    student_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
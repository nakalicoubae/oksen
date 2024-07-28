from django.contrib import admin
from .models import Member, UsageTime, Usage, Checklist

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('student_number', 'username', 'year', 'accumulated_warnings', 'fine', 'unpaid_fine')
    search_fields = ('student_number', 'username')


@admin.register(UsageTime)
class UsageTimeAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'extended_time', 'get_user_name')

    def get_user_name(self, obj):
        usage = Usage.objects.filter(usage_time=obj).first()
        return usage.member.username if usage else '미사용'

    get_user_name.short_description = '사용자 이름'

from django.contrib import admin
from .models import Member, UsageTime, Usage, Checklist
@admin.register(Usage)
class UsageAdmin(admin.ModelAdmin):
    list_display = ('member', 'usage_time', 'usage_date', 'created_at')
    list_filter = ('usage_date', 'created_at')
    search_fields = ('member__username', 'member__student_number')
    ordering = ('-created_at',)

from django.contrib import admin
from .models import Checklist

@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('member', 'updated_at', '원판_청소', '바벨_청소', '벤치_청소', '덤벨_청소', '싯업보드_청소', '비상문_확인', '소등',
                    '원판_파손', '바벨_파손', '벤치_파손', '덤벨_파손', '싯업보드_파손', '비상문_파손', '소등_파손')
    list_filter = ('updated_at', '원판_파손', '바벨_파손', '벤치_파손', '덤벨_파손', '싯업보드_파손', '비상문_파손', '소등_파손')
    search_fields = ('member__username', 'member__student_number')
    ordering = ('-updated_at',)  # 최신 업데이트 순으로 정렬

    fields = ('member', 'updated_at', '원판_청소', '바벨_청소', '벤치_청소', '덤벨_청소', '싯업보드_청소', '비상문_확인', '소등',
              '원판_파손', '바벨_파손', '벤치_파손', '덤벨_파손', '싯업보드_파손', '비상문_파손', '소등_파손', '요구_및_불편사항')
    readonly_fields = ('updated_at', '요구_및_불편사항')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # 이미 존재하는 객체일 경우
            return self.readonly_fields + ('member',)
        return self.readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        obj = self.get_object(request, object_id)
        if obj:
            extra_context['요구_및_불편사항'] = obj.요구_및_불편사항
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
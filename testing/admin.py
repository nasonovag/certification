from django.contrib import admin
from .models import (
    Test, Question, Answer,
    Result, UserProfile,
    UserTestResult, ResultHistory
)

# Ответы внутри вопроса
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2

# Вопросы внутри теста
class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

# Настройка Test с inline вопросов
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('title', 'category', 'difficulty', 'description')
    search_fields = ('title', 'description')
    list_filter = ('category', 'difficulty')

# Настройка Question с inline ответов
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('text', 'test')
    search_fields = ('text',)
    list_filter = ('test',)

# Answer с редактируемым полем is_correct
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_editable = ('is_correct',)
    list_filter = ('is_correct', 'question')

# Result
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'percent', 'passed', 'completed_at')
    search_fields = ('user__username', 'test__title')
    list_filter = ('passed', 'test', 'completed_at')

# UserProfile с кастомным отображением
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'registration_date', 'is_active')
    search_fields = ('user__username',)
    list_filter = ('role', 'is_active')

# UserTestResult
@admin.register(UserTestResult)
class UserTestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'passed', 'created_at')
    list_filter = ('passed', 'created_at')
    search_fields = ('user__username', 'test__title')

# ResultHistory
@admin.register(ResultHistory)
class ResultHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'completed_at')
    search_fields = ('user__username', 'test__title')
    list_filter = ('completed_at',)
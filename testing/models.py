from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('hr', 'HR'),
        ('admin', 'Администратор'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    registration_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="Активен ли пользователь?")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name="Фото профиля")

    def __str__(self):
        return f"{self.user.username} — {self.get_role_display()}"


class Test(models.Model):
    CATEGORY_CHOICES = [
        ('it', 'IT'),
        ('soft', 'Навыки общения'),
        ('career', 'Профориентация'),
    ]

    DIFFICULTY_CHOICES = [
        ('easy', 'Легкий'),
        ('medium', 'Средний'),
        ('hard', 'Сложный'),
    ]

    title = models.CharField(max_length=200, verbose_name="Название теста")
    description = models.TextField(verbose_name="Описание теста")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='it', verbose_name="Категория")
    difficulty = models.CharField(max_length=50, choices=DIFFICULTY_CHOICES, default='medium', verbose_name="Сложность")
    time_limit = models.IntegerField(null=True, blank=True, verbose_name="Лимит времени (в минутах)", default=None)

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст вопроса")
    order = models.PositiveIntegerField(verbose_name="Порядок вопроса", default=0)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField(verbose_name="Текст ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ли ответ?")
    order = models.PositiveIntegerField(verbose_name="Порядок ответа", default=0)

    def __str__(self):
        return self.text


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    percent = models.FloatField()
    passed = models.BooleanField()
    completed_at = models.DateTimeField()

    class Meta:
        unique_together = ('user', 'test')

    def __str__(self):
        return f"Результат: {self.user.username} — {self.test.title} ({self.score}/{self.total})"


class ResultHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"История: {self.user.username} — {self.test.title} ({self.score})"


class UserTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    score = models.FloatField()
    passed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    

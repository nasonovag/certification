from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse, FileResponse, HttpResponseForbidden
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.conf import settings
from .models import Test, Question, Answer, Result, UserProfile
from .forms import UserProfileForm, CustomUserCreationForm
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors

# Подключаем шрифт Arial
pdfmetrics.registerFont(TTFont('Arial', 'C:\\Windows\\Fonts\\arial.ttf'))

# Главная страница с тестами
def test_list(request):
    query = request.GET.get('q')
    tests = Test.objects.filter(title__icontains=query) if query else Test.objects.all()
    return render(request, 'testing/test_list.html', {'tests': tests, 'query': query})

# Прохождение теста
@login_required
def take_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    questions = test.question_set.prefetch_related('answers')

    previous_result = (
        Result.objects.filter(user=request.user, test=test)
        .order_by('-completed_at')
        .first()
    )

    if previous_result and previous_result.passed:
        return render(request, 'testing/test_already_passed.html', {
            'test': test,
            'result': previous_result,
            'message': 'Вы уже успешно прошли этот тест и не можете пройти его снова.'
        })

    # 👉 удаляем предыдущие НЕуспешные попытки
    Result.objects.filter(user=request.user, test=test, passed=False).delete()

    return render(request, 'testing/take_test.html', {
        'test': test,
        'questions': questions,
        'previous_result': previous_result,
    })

# Отправка результатов теста
@login_required
def submit_test(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    questions = test.question_set.prefetch_related('answers')
    score = 0
    total = questions.count()

    for question in questions:
        selected_answer_id = request.POST.get(f'question_{question.id}')
        if selected_answer_id:
            try:
                selected_answer = question.answers.get(id=selected_answer_id)
                if selected_answer.is_correct:
                    score += 1
            except Answer.DoesNotExist:
                pass

    percent = (score / total) * 100 if total > 0 else 0
    passed = percent >= 70

    # ✅ Сохраняем результат
    result = Result.objects.create(
        user=request.user,
        test=test,
        score=score,
        total=total,
        percent=percent,
        passed=passed,
        completed_at=timezone.now()
    )

    # ✅ Если прошел тест — показываем сертификат
    if passed:
        return redirect('certificate', result_id=result.id)

    # ❌ Если не прошел — обычный результат
    return render(request, 'testing/result.html', {
        'test': test,
        'score': score,
        'total': total,
        'percent': round(percent, 2),
        'passed': passed,
    })

# Сертификат после сдачи теста
@login_required
def download_certificate(request, test_id):
    test = get_object_or_404(Test, pk=test_id)
    result = get_object_or_404(Result, user=request.user, test=test)

    if not result.passed:
        return HttpResponse("Сертификат доступен только при успешном прохождении теста.")

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    p.setStrokeColor(colors.darkblue)
    p.setLineWidth(4)
    p.rect(1.5 * cm, 1.5 * cm, width - 3 * cm, height - 3 * cm)

    p.setFont("Arial", 26)
    p.setFillColor(colors.darkblue)
    p.drawCentredString(width / 2, height - 4 * cm, "СЕРТИФИКАТ")

    p.setFont("Arial", 16)
    p.setFillColor(colors.black)
    full_name = request.user.get_full_name() or request.user.username
    p.drawCentredString(width / 2, height - 6 * cm, f"Выдан: {full_name}")

    p.setFont("Arial", 14)
    p.drawCentredString(width / 2, height - 8 * cm, "За успешное прохождение теста:")
    p.setFont("Arial", 15)
    p.setFillColor(colors.darkgreen)
    p.drawCentredString(width / 2, height - 9 * cm, f"«{test.title}»")

    p.setFont("Arial", 13)
    p.setFillColor(colors.black)
    p.drawCentredString(width / 2, height - 11 * cm, f"Результат: {result.percent}%")

    p.setFont("Arial", 12)
    p.drawCentredString(width / 2, height - 13 * cm, f"Дата: {now().strftime('%d.%m.%Y')}")

    p.setFont("Arial", 10)
    p.drawRightString(width - 3 * cm, 3 * cm, "Подпись: ___________________")

    p.showPage()
    p.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='certificate.pdf')

# Профиль пользователя
@login_required
def profile_view(request):
    results = Result.objects.filter(user=request.user).select_related('test')
    return render(request, 'testing/profile.html', {'results': results})

# Редактирование профиля
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'testing/edit_profile.html', {'form': form})

# Регистрация
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Создание тестов (только HR)
from .forms import TestForm

@login_required
def create_test(request):
    if request.user.profile.role != 'hr':
        return HttpResponseForbidden("Доступ только для HR")

    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.creator = request.user  # если в модели есть поле creator
            test.save()
            return redirect('test_list')  # перенаправляем на список тестов
    else:
        form = TestForm()

    return render(request, 'testing/create_test.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from .models import Result
from datetime import datetime

def certificate_view(request, result_id):
    result = get_object_or_404(Result, id=result_id)
    test = result.test
    user = result.user

    context = {
        'user': user,
        'test': test,
        'result': result,
        'year': datetime.now().year
    }

    return render(request, 'testing/certificate.html', context)
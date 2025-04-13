from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.conf import settings
import os
from io import BytesIO

def generate_certificate(user, test, score, percent):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Заголовок
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 100, "СЕРТИФИКАТ")

    # Имя пользователя
    c.setFont("Helvetica", 18)
    c.drawCentredString(width / 2, height - 150, f"Выдан: {user.get_full_name() or user.username}")

    # Название теста
    c.setFont("Helvetica", 16)
    c.drawCentredString(width / 2, height - 200, f"За успешное прохождение теста: \"{test.title}\"")

    # Баллы и процент
    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 250, f"Баллов: {score} из {test.questions.count()} ({round(percent, 2)}%)")

    # Подпись и дата
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(50, 100, "Центр занятости г. Москвы")
    c.drawRightString(width - 50, 100, "Дата: __________")

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer
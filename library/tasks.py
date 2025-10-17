from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass

@shared_task
def check_overdue_loans():
    today = timezone.now().date()
    overdue_loans = Loan.objects.filter(is_returned=False, due_date__lt=today)

    for loan in overdue_loans:
        member_email = loan.member.user.email
        book_title = loan.book.title 
        due_date = loan.due_date.strftime("%y-%m-%d") 

        subject = f"overdue notices"
        message = (f" the book is overdue") 

        send_mail(subject, message, "me@test.com", [member_email], fail_silently=True,) 

    return f"sent {len(overdue_loans)} Overdue notification"     

from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Expense
from datetime import datetime, timedelta

@shared_task
def send_weekly_expenditure_summary():
    """
        This shared task is used to sent weekly emails to the users

        This function, looks for the last 7 days data and then sends
        email to the users.
    """
    # Calculate start and end dates for the week
    end_date = datetime.now()
    start_date = end_date - timedelta(days=end_date.weekday())  # Assuming Sunday is the first day of the week

    # Fetch expenses for the week
    users = User.objects.all()
    for user in users:
        weekly_expenses = Expense.objects.filter(date__gte=start_date, date__lte=end_date, payer=user.id)

        # Calculate total expenditure for each user
        user = user
        expenditure = sum([expense.amount for expense in weekly_expenses])

        # Compose and send emails
        subject = "Weekly Expenditure Summary"
        message = "Here is your weekly expenditure summary:\n"
        
        message += f"{user.username}: Rupees {expenditure}\n"

        from_email = "sshashwat004@gmail.com"
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)

@shared_task
def send_expense_notification(passboook_data):
    """
        This function takes in the 'passbook_data', which is exactly like the 
        Passbook model and then sends email everytime a new entry is added in
        the passbook table
    """
    # Compose and send emails
    subject = f"New Expense Added by : {passboook_data.payer_id.username}"
    message = f"A New Expense of amount :{passboook_data.amount} is added to your account"
    from_email = "sshashwat004@gmail.com"
    recipient_list = [passboook_data.user.email]

    send_mail(subject, message, from_email, recipient_list)
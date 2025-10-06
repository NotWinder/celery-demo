import time
from datetime import datetime

from celery import shared_task


@shared_task
def send_single_email(email, subject, message):
    """
    Simulates sending a single email
    In production, you'd use Django's send_mail here
    """
    print(f"\n{'='*50}")
    print(f"📧 SENDING EMAIL")
    print(f"To: {email}")
    print(f"Subject: {subject}")
    print(f"Message: {message}")
    print(f"Time: {datetime.now()}")
    print(f"{'='*50}\n")

    # Simulate email sending delay
    time.sleep(3)

    return f"✅ Email sent to {email}"


@shared_task
def send_bulk_emails(email_list, subject, message):
    """
    Sends emails to multiple recipients
    Each email is sent as a separate task
    """
    print(f"\n🚀 Starting bulk email job for {len(email_list)} recipients\n")

    results = []
    for email in email_list:
        # Queue each email as a separate task
        task = send_single_email.delay(email, subject, message)
        results.append(task.id)

    return {
        "total": len(email_list),
        "task_ids": results,
        "status": "All emails queued",
    }


@shared_task
def add_numbers(x, y):
    """Simple task to test Celery is working"""
    print(f"Adding {x} + {y}")
    time.sleep(2)
    result = x + y
    print(f"Result: {result}")
    return result

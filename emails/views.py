from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .tasks import add_numbers, send_bulk_emails, send_single_email


def index(request):
    """Home page with API info"""
    return JsonResponse(
        {
            "message": "Celery + Django Demo",
            "endpoints": {
                "/test/": "Test basic Celery task",
                "/send-email/": "Send single email",
                "/send-bulk/": "Send bulk emails",
            },
        }
    )


@require_http_methods(["GET"])
def test_celery(request):
    """Test if Celery is working"""
    task = add_numbers.delay(5, 10)

    return JsonResponse(
        {
            "status": "Task queued",
            "task_id": task.id,
            "message": "Check Celery worker terminal to see the result",
        }
    )


@require_http_methods(["GET"])
def send_email_view(request):
    """Send a single email asynchronously"""
    email = request.GET.get("email", "user@example.com")

    # This returns IMMEDIATELY - email sent in background
    task = send_single_email.delay(
        email,
        "Welcome to Our Newsletter!",
        "Thank you for subscribing. You will receive updates weekly.",
    )

    return JsonResponse(
        {
            "status": "Email queued successfully",
            "task_id": task.id,
            "recipient": email,
            "message": "The email is being sent in the background",
        }
    )


@require_http_methods(["GET"])
def send_bulk_view(request):
    """Send emails to multiple recipients"""
    # Sample email list
    email_list = [
        "alice@example.com",
        "bob@example.com",
        "charlie@example.com",
        "diana@example.com",
        "eve@example.com",
    ]

    # Queue the bulk email job
    task = send_bulk_emails.delay(
        email_list,
        "Monthly Newsletter",
        "Here is your monthly update with the latest news!",
    )

    return JsonResponse(
        {
            "status": "Bulk email job queued",
            "task_id": task.id,
            "total_recipients": len(email_list),
            "message": "All emails are being sent in the background",
        }
    )


@require_http_methods(["GET"])
def check_task_status(request, task_id):
    """Check the status of a task"""
    from celery.result import AsyncResult

    task = AsyncResult(task_id)

    response = {
        "task_id": task_id,
        "status": task.status,
        "ready": task.ready(),
    }

    if task.ready():
        response["result"] = task.result

    return JsonResponse(response)

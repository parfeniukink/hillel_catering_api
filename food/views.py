from django.core.handlers.wsgi import WSGIRequest
from django.template.response import TemplateResponse

from .forms import UploadDishesForm


def import_dishes(request: WSGIRequest, **kwargs):
    if request.method == "GET":
        form = UploadDishesForm()
        context = {"form": form}

        return TemplateResponse(request, "admin/import_dishes.html", context)
    elif request.method == "POST":
        return
    else:
        raise ValueError(f"Method {request.method} is not allowed")

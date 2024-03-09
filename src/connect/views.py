import os, json, base64
from pathlib import Path
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.exceptions import PermissionDenied, BadRequest
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404, JsonResponse
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from .tasks import (
    process_students,
    process_subjects,
    process_assessments,
    process_results,
    process_full
)


SERVICE_NAME = "Studyport"
SERVICE_VERSION = "1.0"
SAVE_SYNC_TYPES = ["assessments", "results", "full", "part"]


@csrf_exempt
def handler_view(request):
    if request.method != "POST":
        raise BadRequest('Invalid request method')

    try:
        data = json.loads(request.body)
        sync = data["SMSDirectoryData"]["sync"]
    except:
        return JsonResponse(status=401, data={
            "error": 401,
            "result": "No Data",
            "service": SERVICE_NAME,
            "version": SERVICE_VERSION,
        })

    # Route to view based on query type
    if sync == "check":         return CheckView.as_view()(request)
    if sync == "assessments":   return AssessmentsView.as_view()(request)
    if sync == "results":       return ResultsView.as_view()(request)
    if sync == "full":          return FullView.as_view()(request)
    if sync == "part":          return PartView.as_view()(request)
    else:                       return PushHandlerView.as_view()(request)


class PushHandlerView(View):
    save_path = None

    def post(self, request):
        status = 403
        response = {
            "error": 403,
            "result": "Authentication Failed",
            "service": SERVICE_NAME,
            "version": SERVICE_VERSION,
        }

        # Authenticate and update response status
        if self.authenticate():
            status = 200
            response = {
                **response,
                "error": 0,
                "result": "OK",
            }

            # Get other response data
            response = {**response, **self.get_response_data()}

            # Save data
            if self.save_path != None:
                self.save_to_file()
                self.save_to_database()

        # Wrap data and return response
        data = {"SMSDirectoryData": response}
        return JsonResponse(status=status, data=data)

    def authenticate(self):
        # Get authentication data
        data = json.loads(self.request.body)

        # Calculate auth string
        username = settings.KAMAR_KEY
        password = settings.KAMAR_SECRET
        authcheck = "Basic " + base64.b64encode((username+":"+password).encode()).decode()

        # Authenticate source
        # Compare auth string with source
        if authcheck == self.request.META["HTTP_AUTHORIZATION"]:
            return True
        return False

    def save_to_file(self):
        # Save request data
        directory = os.path.join(settings.KAMAR_CACHE_ROOT, self.save_path)
        Path(directory).mkdir(parents=True, exist_ok=True)
        path = os.path.join(directory, f"{timezone.now().strftime('%Y-%m-%d-%H-%M-%S-%f')}.json")
        with open(path, 'w+') as f:
            json.dump(json.loads(self.request.body), f, indent=4)

    def save_to_database(self):
        pass

    def get_response_data(self):
        return {}


class CheckView(PushHandlerView):
    def get_response_data(self):
        data = super(CheckView, self).get_response_data()
        data = {
            **data,
            "status": "Ready",
            "infourl": "https://studyport.co",
            "privacystatement": "Privacy Statement (Needs to be 50 words long)",
            "options": {
                "ics": False,
                "students": {
                    "details": True,
                    "passwords": True,
                    "photos": False,
                    "groups": False,
                    "awards": False,
                    "timetables": False,
                    "attendance": False,
                    "assessments": True,
                    "pastoral": False,
                    "learningsupport": False,
                    "fields": {
                        "required": "firstnamelegal;lastnamelegal;email;yearlevel;uniqueid;",
                        "optional": "id;",
                    }
                },
                "common": {
                    "subjects": True,
                    "notices": False,
                    "calendar": False,
                    "bookings": False
                }
            }
        }
        return data


class AssessmentsView(PushHandlerView):
    save_path = "assessments"

    def save_to_database(self):
        process_assessments()


class ResultsView(PushHandlerView):
    save_path = "results"

    def save_to_database(self):
        process_results()


class FullView(PushHandlerView):
    save_path = "full"

    def save_to_database(self):
        process_full()


class PartView(PushHandlerView):
    save_path = "part"

    def save_to_database(self):
        process_subjects()
        process_students()






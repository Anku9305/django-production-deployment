from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student
import json

@csrf_exempt
def student_list(request):
    if request.method == "GET":
        data = list(Student.objects.values())
        return JsonResponse(data, safe=False)

    if request.method == "POST":
        body = json.loads(request.body)
        Student.objects.create(
            name=body["name"],
            email=body["email"],
            age=body["age"]
        )
        return JsonResponse({"message": "Student created"})


@csrf_exempt
def student_detail(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    if request.method == "PUT":
        body = json.loads(request.body)
        student.name = body["name"]
        student.email = body["email"]
        student.age = body["age"]
        student.save()
        return JsonResponse({"message": "Student updated"})

    if request.method == "DELETE":
        student.delete()
        return JsonResponse({"message": "Student deleted"})


# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("Django backend is running 🚀")

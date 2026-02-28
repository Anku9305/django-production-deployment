import json

from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import StudentForm
from .models import Student


def home(request):
    return HttpResponse("Django Student Management backend is running 🚀")


def student_list_view(request):
    students = Student.objects.all()
    return render(request, "core/student_list.html", {"students": students})


def student_create_view(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student created successfully.")
            return redirect("student_list")
    else:
        form = StudentForm()

    return render(
        request,
        "core/student_form.html",
        {"form": form, "title": "Add student"},
    )


def student_update_view(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully.")
            return redirect("student_list")
    else:
        form = StudentForm(instance=student)

    return render(
        request,
        "core/student_form.html",
        {"form": form, "title": "Edit student"},
    )


def student_delete_view(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect("student_list")

    return render(
        request,
        "core/student_confirm_delete.html",
        {"student": student},
    )


@csrf_exempt
@require_http_methods(["GET", "POST"])
def student_list_api(request):
    if request.method == "GET":
        data = list(
            Student.objects.values(
                "id", "name", "email", "age", "created_at", "updated_at"
            )
        )
        return JsonResponse(data, safe=False)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body"}, status=400)

    required_fields = ["name", "email", "age"]
    missing = [field for field in required_fields if field not in body]
    if missing:
        return JsonResponse(
            {"error": f"Missing fields: {', '.join(missing)}"},
            status=400,
        )

    student = Student.objects.create(
        name=body["name"],
        email=body["email"],
        age=body["age"],
    )
    return JsonResponse(
        {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "age": student.age,
        },
        status=201,
    )


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def student_detail_api(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(
            {
                "id": student.id,
                "name": student.name,
                "email": student.email,
                "age": student.age,
                "created_at": student.created_at,
                "updated_at": student.updated_at,
            }
        )

    if request.method == "PUT":
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

        for field in ["name", "email", "age"]:
            if field in body:
                setattr(student, field, body[field])

        student.save()
        return JsonResponse({"message": "Student updated"})

    student.delete()
    # 204 responses should not include a body
    return JsonResponse({}, status=204)

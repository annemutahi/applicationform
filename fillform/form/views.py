from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Question, Response, Answer, UploadedFile, Center, Department
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.messages import get_messages

def submit_response(request):
    if request.method == 'POST':
        response = Response.objects.create(
            respondent_name=request.POST.get('name'),
            respondent_center=request.POST.get('center'),
            respondent_attachment_period=request.POST.get('attachment_period'),
            respondent_department=request.POST.get('department'),
            submitted_at=timezone.now()
        )

        # Save text answers
        text_fields = {
            "Name": request.POST.get('name'),
            "Email": request.POST.get('email'),
            "Phone": request.POST.get('phone'),
            "ID": request.POST.get('id'),
            "Gender": request.POST.get('gender'),
            "Age": request.POST.get('age'),
            "Ethnicity": request.POST.get('ethnicity'),
            "Disability": request.POST.get('disability'),
            "Specify Disability": request.POST.get('specify_disability'),
            "Institution": request.POST.get('institution'),
            "Area of Study": request.POST.get('area_of_study'),
            "Attachment Period": request.POST.get('attachment_period'),
            "Center": request.POST.get('center'),
            "Department": request.POST.get('department'),
        }

        for question, answer in text_fields.items():
            if answer:
                Answer.objects.create(
                    response=response,
                    question_text=question,
                    text_answer=answer
                )

        # Save file answers
        file_fields = {
            "ID Upload": "id_upload",
            "Request Letter": "request_letter",
            "CV": "cv",
            "Cover Letter": "cover_letter",
            "Insurance": "insurance",
            "Other Document": "other",
        }

        for question, field_name in file_fields.items():
            uploaded_file = request.FILES.get(field_name)
            if uploaded_file:
                Answer.objects.create(
                    response=response,
                    question_text=question,  # ✅ must provide
                    file_answer=uploaded_file
                )
        request.session['form_submitted'] = True

        return redirect('success')

    return render(request, 'form/submit_form.html')

def success_page(request):
    return render(request, "success.html")

def super_or_dashboard_staff(user):
    return user.is_superuser or user.is_staff

def dashboard_access_required(view_func):
    return user_passes_test(
        super_or_dashboard_staff,
        login_url='admin_login'  # points to your custom login view
    )(view_func)

@dashboard_access_required
def admin_responses_list(request):
    query = request.GET.get('query', '').strip()
    responses = Response.objects.all()

    if query:
        responses = responses.filter(
            Q(respondent_center__icontains=query) |
            Q(respondent_attachment_period__icontains=query) |
            Q(submitted_at__icontains=query) |
            Q(respondent_department__icontains=query)
        )
        if not responses.exists():
            messages.error(request, "No matching results found.")
    else:
        pass
    return render(request, "admin_responses_list.html", {"responses": responses})

@dashboard_access_required
def admin_response_detail(request, response_id):
    response = get_object_or_404(Response, id=response_id)
    answers = response.answers.all()
    files = response.files.all()
    return render(request, 'admin_response_detail.html', {
        'response': response,
        'answers': answers,
        'files': files,
    })

def admin_login(request):
    if request.user.is_authenticated and super_or_dashboard_staff(request.user):
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None and super_or_dashboard_staff(user):
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not authorized.')
        
        storage = get_messages(request)
        for _ in storage:
            pass

    return render(request, 'admin_login.html')


@dashboard_access_required
def admin_dashboard(request):
    total_responses = Response.objects.count()
    recent_responses = Response.objects.order_by('-submitted_at')[:5]

    return render(request, 'admin_dashboard.html', {
        'total_responses': total_responses,
        'recent_responses': recent_responses
    })

@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

def get_departments(request, center_id):
    departments = Department.objects.filter(center_id=center_id).values('id', 'name')
    return JsonResponse(list(departments), safe=False)

def attachment_form(request):
    centers = Center.objects.all()
    return render(request, 'submit_form.html', {'centers': centers})

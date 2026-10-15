from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Count, Avg, Max
from .forms import RegisterForm, AnalysisForm, ResumeUploadForm, JobForm
from .models import Resume, Analysis, Job
from .utils import extract_text, find_skills, check_sections, calculate_match

def home(request):
    return render(request, 'analyzer/home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)      # log the user in right after registering
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect('faculty_dashboard')
    return redirect('student_dashboard')


@login_required
def new_analysis(request):
    return redirect('dashboard')


@login_required
def student_dashboard(request):
    if request.user.is_staff:
        return redirect('faculty_dashboard')
    jobs = Job.objects.filter(is_active=True)
    recent = Analysis.objects.filter(user=request.user)[:5]
    return render(request, 'analyzer/student_dashboard.html', {'jobs': jobs, 'recent': recent})


@login_required
def analyze_job(request, job_id):
    if request.user.is_staff:
        return redirect('faculty_dashboard')
    job = get_object_or_404(Job, pk=job_id, is_active=True)
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                resume_text = extract_text(form.cleaned_data['resume_file'])
            except Exception:
                resume_text = ''

            if not resume_text.strip():
                form.add_error('resume_file', 'Could not read text from this PDF. Please upload a text-based PDF, not a scanned image.')
            else:
                resume_skills = find_skills(resume_text)
                job_skills = find_skills(job.description)
                found, missing, percentage = calculate_match(job_skills, resume_skills)
                sections = check_sections(resume_text)

                resume = Resume.objects.create(
                    user=request.user,
                    file=form.cleaned_data['resume_file'],
                )
                analysis = Analysis.objects.create(
                    user=request.user,
                    resume=resume,
                    job=job,
                    job_title=job.title,
                    job_description=job.description,
                    match_percentage=percentage,
                    found_skills=','.join(found),
                    missing_skills=','.join(missing),
                    sections_found=','.join(sections),
                )
                return redirect('result', pk=analysis.pk)
    else:
        form = ResumeUploadForm()
    return render(request, 'analyzer/analyze_job.html', {'form': form, 'job': job})


@login_required
def faculty_dashboard(request):
    if not request.user.is_staff:
        return redirect('student_dashboard')
    jobs = Job.objects.filter(posted_by=request.user).annotate(total=Count('analysis'))
    return render(request, 'analyzer/faculty_dashboard.html', {'jobs': jobs})


@login_required
def add_job(request):
    if not request.user.is_staff:
        return redirect('student_dashboard')
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('faculty_dashboard')
    else:
        form = JobForm()
    return render(request, 'analyzer/add_job.html', {'form': form})


@login_required
@require_POST
def toggle_job(request, pk):
    if not request.user.is_staff:
        return redirect('student_dashboard')
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    job.is_active = not job.is_active
    job.save()
    return redirect('faculty_dashboard')


@login_required
@require_POST
def delete_job(request, pk):
    if not request.user.is_staff:
        return redirect('student_dashboard')
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    job.delete()
    return redirect('faculty_dashboard')

@login_required
def result(request, pk):
    analysis = get_object_or_404(Analysis, pk=pk, user=request.user)
    return render(request, 'analyzer/result.html', {'analysis': analysis})

@login_required
@require_POST
def delete_analysis(request, pk):
    analysis = get_object_or_404(Analysis, pk=pk, user=request.user)
    resume = analysis.resume
    analysis.delete()
    resume.file.delete(save=False)
    resume.delete()
    return redirect('dashboard')

@login_required
def job_results(request, pk):
    if not request.user.is_staff:
        return redirect('student_dashboard')
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    analyses = Analysis.objects.filter(job=job).select_related('user').order_by('-match_percentage')
    stats = analyses.aggregate(avg=Avg('match_percentage'), top=Max('match_percentage'))
    return render(request, 'analyzer/job_results.html', {'job': job, 'analyses': analyses, 'stats': stats})

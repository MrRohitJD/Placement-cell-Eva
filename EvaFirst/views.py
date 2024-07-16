
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.models import User
from .models import StudentProfile, ManagerProfile, RecruiterProfile, PostJob, Applications
from .decorators import role_required
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'home.html')

User = get_user_model()

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        user = User.objects.create_user(first_name=username,username=email, email= email, password=password, role=role)
        messages.success(request, "User registered successfully please login " )
        # Handle role-specific logic if necessary
        # if role == 'student':
        #     StudentProfile.objects.create(user=user, student_name=username, student_email=email)
        

        # elif role == 'manager':
        #     ManagerProfile.objects.create(user=user, manager_name=username, manager_email=email)

        # elif role == 'recruiter':
        #     RecruiterProfile.objects.create(user=user, recruiter_name=username, recruiter_email=email)
          
            

        return redirect('login') 
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.role == 'student':
                messages.success(request, f"Student {user.first_name} Login successfully..." )
                return redirect('studentProfile')
            
            elif user.role == 'manager':
                messages.success(request, f"Manager {user.first_name} Login successfully..." )
                return redirect('managerProfile')
            elif user.role == 'recruiter':
                messages.success(request, f"Recruiter {user.first_name} Login successfully..." )
                return redirect('recruiterProfile')
            else:
                messages.error(request, "User Not Login " )
                return redirect('login')  # Default redirect if no role matches
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')


def logout(request):
    if auth_logout(request):
        return HttpResponseRedirect('/') # Redirect to home page or any other page
    return HttpResponseRedirect('/')

@role_required('student')
def studentProfile(request):
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        surname = request.POST.get('surname')
        mobileNumber = request.POST.get('mobileNumber')
        address = request.POST.get('address')
        university = request.POST.get('university')
        college = request.POST.get('college')
        course = request.POST.get('course')
        passingYear = request.POST.get('passingYear')
        rollNum = request.POST.get('rollNum')
        marks = request.POST.get('marks')
        skills = request.POST.get('skills')
        resume = request.FILES.get('resume')  # Corrected: Use get() instead of ()

        userr = request.user
        try:
            profile = StudentProfile.objects.get(user=userr)
            profile.studentFirstname = firstName
            profile.studentLastname = surname
            profile.student_mob = mobileNumber
            profile.student_rollNo = rollNum
            profile.student_address = address
            profile.std_university = university
            profile.std_college = college
            profile.latest_edu = course
            profile.mark = marks
            profile.passing_year = passingYear
            profile.skills = skills
            if resume:
                profile.resume = resume  # Only update if a new resume is provided
            messages.success(request, "Updated Your Profile" )

        except StudentProfile.DoesNotExist:
            profile = StudentProfile(
                user=userr,
                studentFirstname=firstName,
                studentLastname=surname,
                student_mob=mobileNumber,
                student_rollNo=rollNum,
                student_address=address,
                std_university=university,
                std_college=college,
                latest_edu=course,
                mark=marks,
                passing_year=passingYear,
                skills=skills,
                resume=resume
            )

        profile.save()
        messages.info(request, "Successfully added User Information" )
        return HttpResponseRedirect('/')
    
    else:
        messages.error(request, "Some error occurred!!" )
        return render(request, 'stdProf.html')

@role_required('manager')
def managerProfile(request):
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        surname = request.POST.get('surname')
        mobileNumber = request.POST.get('mobileNumber')
        emailId = request.POST.get('emailId')
        department =  request.POST.get('department')
        user = request.user
        try:
            profile = ManagerProfile.objects.get(user=user)
            profile.manager_Firstname = firstName
            profile.manager_Lastname = surname
            profile.manager_email = emailId
            profile.manager_mob = mobileNumber
            profile.manager_dep = department
            profile.save()
            messages.success(request, "Updated Your Profile" )
        except ManagerProfile.DoesNotExist:
            profile = ManagerProfile.objects.create(
                user=user,
                manager_Firstname=firstName,
                manager_Lastname=surname,
                manager_mob=mobileNumber,
                manager_email = emailId,
                manager_dep = department

            )
        messages.info(request, "Successfully added User Information" )
        return redirect('managerProfile')
    return render(request, 'managerPro.html' )


@role_required('recruiter')
def recruiterProfile(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'form_one':
            Company = request.POST.get('CompanyName')
            jobtitle = request.POST.get('jobtitle')
            jobrole = request.POST.get('jobrole')
            qualification = request.POST.get('qualification')
            experience = request.POST.get('experience')
            Loc = request.POST.get('loc')
            about_Job = request.POST.get('about_Job')

            recruiter_profile = RecruiterProfile.objects.get(user=request.user)

            post_job = PostJob(
            recruiter=recruiter_profile,
            company_name=Company,
            job_title=jobtitle,
            job_role=jobrole,
            qualification=qualification,
            experience=experience,
            location = Loc,
            about_job=about_Job
            )
            messages.success(request, "job Posted Successfully..." )
            post_job.save()
            return redirect('home')

        elif form_type == 'form_two':
            firstName = request.POST.get('firstName')
            surname = request.POST.get('surname')
            mobileNumber = request.POST.get('mobileNumber')
            emailId = request.POST.get('emailId')
            CompanyName =  request.POST.get('CompanyName')
            compid =  request.POST.get('compid')
            comp_about =  request.POST.get('comp_about')
            address =  request.POST.get('address')
            user = request.user
            try:
                profile = RecruiterProfile.objects.get(user=user)
                profile.recruiter_Firstname = firstName
                profile.recruiter_Lastname = surname
                profile.recruiter_email = emailId
                profile.recruiter_mob = mobileNumber
                profile.company_name = CompanyName
                profile.recruiter_id_Num = compid
                profile.about_comp = comp_about
                profile.company_location = address
                messages.success(request, "Updated Your Profile" )
                profile.save()
            except RecruiterProfile.DoesNotExist:
                profile = RecruiterProfile.objects.create(
                    user=user,
                    recruiter_Firstname=firstName,
                    recruiter_Lastname=surname,
                    recruiter_mob=mobileNumber,
                    recruiter_email = emailId,
                    company_name = CompanyName,
                    recruiter_id_Num = compid,
                    about_comp = comp_about,
                    company_location = address
                )
                messages.info(request, "Successfully added User Information" )
            return redirect('recruiterProfile')
    return render(request, 'recruProf.html' )



@role_required('manager')
def studentInfo(request):
    student = StudentProfile.objects.all()
    return render(request, 'std_Info.html', {'student': student})


@role_required('manager')
def recruiterInfo(request):
    recruiter = RecruiterProfile.objects.all();
    return render(request, 'rec_Info.html', {'recruiter' : recruiter})



def joblist(request):
    post = PostJob.objects.all()
    user = request.user.id
    print(user)
    try:
        pass
    except StudentProfile.DoesNotExist:
        return render(request, 'error.html', {'message': 'Student profile not found'})
    
    
    if  request.method == 'POST':
        job_postid = request.POST.get('job_post')
        job_post = PostJob.objects.get(id=job_postid)
        std =StudentProfile.objects.get(user_id=user)
        alpInfo  = Applications(
            jobpostInfo = job_post,
            first_name = std.studentFirstname,
            last_name = std.studentLastname,
            education = std.latest_edu,
            experience = '00',
            resume = std.resume
        )
        alpInfo.save()
        return render(request, 'success.html')
    else:
        return render(request, 'jobList.html', {'post' : post})

@role_required('manager')
def showApplications(request):
    ApplicationsInfo = Applications.objects.all()
    return render(request, 'applyInfo.html', {'ApplicationsInfo' : ApplicationsInfo})



def success(request):
    return render(request, 'success.html')


def about(request):
    return render(request, 'about.html')

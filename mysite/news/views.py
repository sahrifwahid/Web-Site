from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import *
from django.contrib.auth.models import User
from .forms import EmployeeForm
from .models import Employee
from .models import Products

from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


from django.db import connection, transaction
from .forms import *
import json
from django.http import JsonResponse

# Create your views here.

class Home(TemplateView):
    template_name = 'news/index.html'

class about_me(TemplateView):
    template_name = 'news/aboutme.html'

    def get(self, request):
        data = dict()
        usr = User.objects.get(username=request.user)
        user_full_name = usr.first_name+" "+usr.last_name
        request.session["user_full_name"] = user_full_name
        data["user_full_name"] = request.session["user_full_name"]
        # data["user_full_name"]=user_full_name
        return render(request, self.template_name, data)


class artical_list(TemplateView):
    template_name = 'news/artical_list.html'

    def get(self, request):
        data = dict()
        my_list = [1, 2, 3, 4, 5]
        data['my_list'] = my_list
        data["user_full_name"] = request.session["user_full_name"]
        return render(request, self.template_name, data)

def news_submit_action(request):
    fname = request.GET["fname"]
    lname = request.GET["lname"]
    mydata = My_Info(first_name=fname, last_name=lname)
    mydata.save()
    return render(request, 'news/index.html')

def employee_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = EmployeeForm()
        else:
            employee = Employee.objects.get(pk=id)
            form = EmployeeForm(instance=employee)
        return render(request, "news/employee_form.html", {'form': form})
    else:
        if id == 0:
            form = EmployeeForm(request.POST)
        else:
            employee = Employee.objects.get(pk=id)
            form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
        return redirect('employee_list')

def employee_list(request):
    context = {'employee_list': Employee.objects.all()}
    return render(request, "news/employee_list.html", context)

def employee_delete(request, id):
    employee = Employee.objects.get(pk=id)
    employee.delete()
    return redirect('employee_list')

class employee_login_view(TemplateView):
    template_name = 'news/employee-login.html'

def employee_login_submit(request):
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        request.session['app_user_id'] = username
        request.session['user_full_name'] = username
        return HttpResponseRedirect(reverse("employee_insert"))
    else:
        return render(request, "news/employee-login.html", {"message": "Invalid Username or Password"})

class employee_form_js_view(TemplateView):
    template_name = 'news/employee_form_js.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'news/employee-login.html')
        data = dict()
        form = EmployeeForm()
        data['form'] = form
        return render(request, self.template_name, data)

def employee_signup(request):
    if request.method == "GET":
        return render(request, "news/employee-signup.html")
    else:
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        confirm_password = request.POST.get('confirm_password', False)

        if len(username)==0 or len(password)==0:
            return render(request, "news/employee-signup.html", {"message": "Please check your Input"})

        if password != confirm_password:
            return render(request, "news/employee-signup.html", {"message": "Password and Confirm Password does't match"})
        else:
            user = User.objects.create_user(username, '', password)
            user.save()
            return render(request, 'news/employee-login.html')


class product_create_view(TemplateView):
    template_name = 'news/product-create.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'news/employee-login.html')
        data = dict()
        form = ProductsModelForm()
        print(form)
        data['form'] = form
        return render(request, self.template_name, data)

@transaction.atomic
def product_create_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'news/employee-login.html')
    data=dict()
    data['form_is_valid'] = False

    if request.method=='POST':
        form = ProductsModelForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    app_user_id = request.session["app_user_id"]

                    sales_price = form.cleaned_data['sales_price']
                    product_code = form.cleaned_data['product_code']

                    if Products.objects.filter(product_code=product_code).exists():
                        data['error_message']='Product Code Already Exist!'
                        return JsonResponse(data)

                    if sales_price<0:
                        data['error_message']='Sales price should not have negative values!'
                        return JsonResponse(data)

                    post = form.save(commit=False)
                    post.app_user_id = app_user_id
                    post.save()
                    data['form_is_valid'] = True
                    data['succ_message'] = "Save Successfully"
            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)


class sales_create_view(TemplateView):
    template_name = 'news/product-sales.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'news/employee-login.html')
        data = dict()
        form = ProductsSalesModelForm()
        data['form'] = form
        return render(request, self.template_name, data)


@transaction.atomic
def sales_create_insert(request):
    if not request.user.is_authenticated:
        return render(request, 'news/employee-login.html')
    data=dict()
    data['form_is_valid'] = False

    if request.method=='POST':
        form = ProductsSalesModelForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    app_user_id = request.session["app_user_id"]
                    product_code = form.cleaned_data['product_code']

                    post = form.save(commit=False)
                    post.app_user_id = app_user_id
                    post.save()
                    data['form_is_valid'] = True
                    data['succ_message'] = "Save Successfully"
            except Exception as e:
                print(str(e))
                data['form_is_valid'] = False
                data['error_message']=str(e)
                return JsonResponse(data)
        else:
            data['error_message']=form.errors.as_json()
    return JsonResponse(data)


def get_product_info(request, product_code):

    data = dict()
    product_name=''
    sales_price=0
    try:
        product_info = Products.objects.get(product_code=product_code)
        product_name = product_info.product_name
        sales_price = product_info.sales_price
    except Exception as e:
        product_name = ''
        sales_price=0

    data['product_name']=product_name
    data['sales_price']=sales_price
    data['form_is_valid'] = True
    return JsonResponse(data)
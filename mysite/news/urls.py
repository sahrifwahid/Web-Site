from django.urls import path

from . import views




urlpatterns = [
    path('home', views.Home.as_view(), name='home'),
    path('', views.Home.as_view(), name=''),
    path('aboutme', views.about_me.as_view(), name='aboutme'),
    path('artical-list', views.artical_list.as_view(), name='artical-list'),
    path('news-submit-action', views.news_submit_action, name='news-submit-action'),
    path('employee_insert', views.employee_form, name='employee_insert'),
    path('employee_list/',views.employee_list,name='employee_list'),
    path('employee_update/<int:id>/', views.employee_form,name='employee_update'),
    path('employee_delete/<int:id>/',views.employee_delete,name='employee_delete'),
    path('employee-entry', views.employee_form_js_view.as_view(), name='employee-entry'),
    path('employee-login', views.employee_login_view.as_view(), name='employee-login'),
    path('employee-login-sbmit', views.employee_login_submit, name='employee-login-sbmit'),
    path('employee-signup', views.employee_signup, name='employee-signup'),
    path('product-create-view', views.product_create_view.as_view(), name='product-create-view'),
    path('product-create-insert', views.product_create_insert, name='product-create-insert'),
    path('sales-create-view', views.sales_create_view.as_view(), name='sales-create-view'),
    path('sales-create-insert', views.sales_create_insert, name='sales-create-insert'),
    path('get-product-info/<slug:product_code>', views.get_product_info, name='get-product-info'),
]
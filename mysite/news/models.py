from django.db import models

class Reporter(models.Model):
    full_name = models.CharField(max_length=70)
    def __str__(self):
        return self.full_name

class Article(models.Model):
    pub_date = models.DateField()
    headline = models.CharField(max_length=200)
    content = models.TextField()
    reporter = models.ForeignKey(Reporter, on_delete=models.PROTECT)

    def __str__(self):
        return self.headline

class My_Info(models.Model):
    first_name =  models.CharField(max_length=200)
    last_name =  models.CharField(max_length=200)

class Position(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Employee(models.Model):
    fullname = models.CharField(max_length=100)
    emp_code = models.CharField(max_length=3)
    mobile= models.CharField(max_length=15)
    position= models.ForeignKey(Position,on_delete=models.CASCADE)

class Products(models.Model):
    product_code = models.CharField(max_length=100, primary_key=True)
    product_name = models.CharField(max_length=100)
    sales_price = models.DecimalField(max_digits=22, decimal_places=2,default=0.00, blank=True)
    total_sales = models.IntegerField(default =0)
    app_user_id = models.CharField(max_length=200,blank=False, null=True)
    app_data_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product_name

class Products_Sales(models.Model):
    product_code = models.ForeignKey(Products,on_delete=models.PROTECT)
    unit_price = models.DecimalField(max_digits=22, decimal_places=2,default=0.00, blank=True)
    total_quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=22, decimal_places=2,default=0.00, blank=True)
    app_user_id = models.CharField(max_length=200,blank=False, null=True)
    app_data_time = models.DateTimeField(auto_now_add=True)

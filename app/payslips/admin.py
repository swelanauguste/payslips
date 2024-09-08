from django.contrib import admin

# Register your models here.
from .models import Allowance, Deduction, Payslip

admin.site.register(Payslip)
admin.site.register(Deduction)
admin.site.register(Allowance)

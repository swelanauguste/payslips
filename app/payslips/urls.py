from django.urls import path

from . import views

urlpatterns = [
    path("", views.user_payslip_list, name="payslip-list"),
    # path("<int:pk>/", views.user_payslip_detail, name="payslip-detail"),
    path(
        "payslip/<int:payslip_id>/pdf/",
        views.generate_payslip_pdf,
        name="generate-payslip-pdf",
    ),
]

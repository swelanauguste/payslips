import os

from django.contrib.auth.decorators import login_required
from django.db.models.functions import ExtractMonth, ExtractYear
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from weasyprint import HTML

from .models import Allowance, Deduction, Payslip


@login_required
def generate_payslip_pdf(request, payslip_id):
    # Get the payslip for the given ID
    payslip = Payslip.objects.get(id=payslip_id, user=request.user)

    # Render the HTML template for the payslip
    html_string = render_to_string(
        "payslips/pdf/payslip_pdf.html", {"payslip": payslip}
    )

    # Generate the PDF from the HTML string
    html = HTML(string=html_string)
    pdf = html.write_pdf()

    # Create an HTTP response with the PDF as an attachment
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="payslip_{payslip.user.employee_id}_{payslip.date.month}_{payslip.date.year}.pdf"'
    )

    return response


@login_required
def user_payslip_list(request):
    # Get distinct years from all payslips
    all_payslips = Payslip.objects.filter(user=request.user)
    years = all_payslips.annotate(year=ExtractYear("date")).values("year").distinct()

    # Get year and month from query parameters
    year = request.GET.get("year")
    month = request.GET.get("month")

    # Apply filters to the payslips
    filtered_payslips = all_payslips
    if year:
        filtered_payslips = filtered_payslips.annotate(year=ExtractYear("date")).filter(
            year=year
        )

    # Filter the months based on the selected year
    months = []
    if year:
        months = (
            all_payslips.annotate(year=ExtractYear("date"), month=ExtractMonth("date"))
            .filter(year=year)
            .values("month")
            .distinct()
        )

    if month:
        filtered_payslips = filtered_payslips.annotate(
            month=ExtractMonth("date")
        ).filter(month=month)

    return render(
        request,
        "payslips/payslip_list.html",
        {
            "payslips": filtered_payslips,
            "years": years,
            "months": months,
            "selected_year": year,
            "selected_month": month,
        },
    )


@login_required
def user_payslip_detail(request, pk):
    payslip = Payslip.objects.get(pk=pk)
    return render(request, "payslips/payslip_detail.html", {"payslip": payslip})


# class IPAddress(models.Model):
#     """
#     This class represents an IP address.
#     """

#     ip_address = models.GenericIPAddressField(
#         verbose_name="IP Address",
#         help_text="The IP address of the client.",
#         unique=True,
#         blank=False,
#         null=False,
#     )
#     created_at = models.DateTimeField(auto_now_add=True, null=True)

#     class Meta:
#         verbose_name = "IP Address"
#         verbose_name_plural = "IP Addresses"

#     def __str__(self):
#         return self.ip_address

# def get_client_ip(request):
#     x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
#     if x_forwarded_for:
#         ip_address = x_forwarded_for.split(",")[0]
#     else:
#         ip_address = request.META.get("REMOTE_ADDR")
#     return ip_address


# class PostDetailView(DetailView):
#     model = Post

#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         context = self.get_context_data(object=self.object)
#         ip_address = get_client_ip(self.request)
#         if IPAddress.objects.filter(ip_address=ip_address).exists():
#             post_slug = request.GET.get("post-slug")
#             post = Post.objects.get(slug=post_slug)
#             post.views.add(IPAddress.objects.get(ip_address=ip_address))
#         else:
#             IPAddress.objects.create(ip_address=ip_address)
#             post_slug = request.GET.get("post-slug")
#             post = Post.objects.get(slug=post_slug)
#             post.views.add(IPAddress.objects.get(ip_address=ip_address))
#         return self.render_to_response(context)

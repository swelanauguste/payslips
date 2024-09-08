import random

from django.core.management.base import BaseCommand
from faker import Faker
from users.models import User

from ...models import Allowance, Deduction, Payslip

fake = Faker()


class Command(BaseCommand):
    help = "Generate fake data for Payslip, Deduction, and Allowance models"

    def handle(self, *args, **kwargs):

        for _ in range(5):  # Adjust the number of users you want to create
            user = User.objects.create_user(
                username=fake.user_name(),
                employee_id=fake.random_int(min=222222, max=888888),
                email=fake.email(),
                password="password123",  # Set a default password for all fake users
                # first_name=fake.first_name(),
                # last_name=fake.last_name(),
                is_active=True,  # Set the users as active
            )
            self.stdout.write(self.style.SUCCESS(f"Created user {user.username}"))

        users = User.objects.all().exclude(is_superuser=True)

        if not users.exists():
            self.stdout.write(self.style.ERROR("No users found in the database."))
            return

        # Generate fake Deductions
        for _ in range(10):  # Adjust the number of deductions
            Deduction.objects.create(
                name=fake.word(),
                amount=round(random.uniform(100, 1000), 2),
                date=fake.date_this_decade(),
                user=random.choice(users),
            )

        # Generate fake Allowances
        for _ in range(10):  # Adjust the number of allowances
            Allowance.objects.create(
                name=fake.word(),
                amount=round(random.uniform(100, 1000), 2),
                date=fake.date_this_decade(),
                user=random.choice(users),
            )

        # Generate fake Payslips
        for _ in range(10):  # Adjust the number of payslips
            payslip = Payslip.objects.create(
                user=random.choice(users),
                tnp=fake.ssn(),
                department=fake.job(),
                salary=round(random.uniform(2000, 5000), 2),
                tax_number=round(random.uniform(500, 2000), 2),
                date=fake.date_this_decade(),
                end_date=fake.date_this_decade(),
                other_deductions=round(random.uniform(50, 500), 2),
            )

            # Add random deductions and allowances
            deductions = Deduction.objects.order_by("?")[
                : random.randint(1, 3)
            ]  # Random 1-3 deductions
            allowances = Allowance.objects.order_by("?")[
                : random.randint(1, 3)
            ]  # Random 1-3 allowances
            payslip.deductions.add(*deductions)
            payslip.allowance.add(*allowances)

        self.stdout.write(self.style.SUCCESS("Successfully created fake data!"))

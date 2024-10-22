# core/management/commands/add_patients.py

import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Patient

class Command(BaseCommand):
    help = 'Populate the database with patients'

    def handle(self, *args, **kwargs):
        fake = Faker()

        names = [
            "Chikondi Banda", "Thoko Kamwendo", "Mwayi Mwale", "Zikomo Phiri", "Tadala Mbewe",
            "Chisomo Tembo", "Zodiak Nyirenda", "Dalitso Mkandawire", "Zione Gondwe", "Tamala Chirwa",
            "Fatsani Kaunda", "Zawadi Nyirongo", "Kondwani Lungu", "Ntchindi Mulenga", "Lusungu Jere",
            "Taonga Mvula", "Wezi Chikopa", "Nkhoma Chimwemwe", "Mphatso Mwansa", "Levison Moyo"
        ]

        for name in names:
            user = User.objects.create_user(
                username=fake.user_name(),
                password='password123',
                email=fake.email()
            )
            dob = fake.date_of_birth(minimum_age=18, maximum_age=60)
            gender = random.choice(['Male', 'Female', 'Other'])
            address = fake.address()
            phone = fake.phone_number()
            emergency_contact = fake.phone_number()
            insurance_provider = random.choice([fake.company(), None])
            insurance_number = random.choice([fake.bothify(text='??########'), None])

            patient = Patient(
                user=user,
                name=name,
                dob=dob,
                gender=gender,
                address=address,
                phone=phone,
                emergency_contact=emergency_contact,
                insurance_provider=insurance_provider,
                insurance_number=insurance_number
            )
            patient.save()
            self.stdout.write(f'Added: {name}')

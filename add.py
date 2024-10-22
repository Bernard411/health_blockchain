import os
import django
import random
from faker import Faker
from django.contrib.auth.models import User
from core.models import Patient

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_blockchain.settings')
django.setup()

# Initialize Faker (using default locale)
fake = Faker()

# List of Malawian names
names = [
    "Chikondi Banda", "Thoko Kamwendo", "Mwayi Mwale", "Zikomo Phiri", "Tadala Mbewe",
    "Chisomo Tembo", "Zodiak Nyirenda", "Dalitso Mkandawire", "Zione Gondwe", "Tamala Chirwa",
    "Fatsani Kaunda", "Zawadi Nyirongo", "Kondwani Lungu", "Ntchindi Mulenga", "Lusungu Jere",
    "Taonga Mvula", "Wezi Chikopa", "Nkhoma Chimwemwe", "Mphatso Mwansa", "Levison Moyo"
]

# Add 20 patients with randomly generated data to the database
def populate_patients():
    for name in names:
        # Create a new user for each patient
        user = User.objects.create_user(
            username=fake.user_name(),
            password='password123',  # Use a default password; consider using a more secure method
            email=fake.email()
        )

        # Generate random patient data
        dob = fake.date_of_birth(minimum_age=18, maximum_age=60)
        gender = random.choice(['Male', 'Female', 'Other'])
        address = fake.address()
        phone = fake.phone_number()
        emergency_contact = fake.phone_number()
        insurance_provider = random.choice([fake.company(), None])
        insurance_number = random.choice([fake.bothify(text='??########'), None])

        # Create and save the patient
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
        print(f'Added: {name}')

if __name__ == '__main__':
    populate_patients()

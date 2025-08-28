from django import forms
from .models import InventoryItem, Offline_Patient, Appointment, Doctor


class OfflinePatientAppointmentForm(forms.Form):
    name = forms.CharField(max_length=200, label="Full Name")
    age = forms.IntegerField(min_value=0, label="Age")
    gender = forms.ChoiceField(choices=Offline_Patient.gender_type, label="Gender")
    phone_number = forms.CharField(max_length=10, label="Phone Number")
    address = forms.CharField(widget=forms.Textarea, label="Address")
    appointment_date = forms.DateTimeField(label="Appointment Date")

    # Appointment fields
    appointment_id = forms.CharField(max_length=30, label="Appointment ID")

    def save(self, opd):
        # Create Offline_Patient instance
        patient = Offline_Patient.objects.create(
            name=self.cleaned_data["name"],
            age=self.cleaned_data["age"],
            gender=self.cleaned_data["gender"],
            phone_number=self.cleaned_data["phone_number"],
            address=self.cleaned_data["address"],
        )

        # Create Appointment instance
        Appointment.objects.create(
            opd=opd,
            offline_patient=patient,
            appointment_id=self.cleaned_data["appointment_id"],
            appointment_date=self.cleaned_data["appointment_date"],
            status="seen",
        )

    def __init__(self, *args, **kwargs):
        super(OfflinePatientAppointmentForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})  # type: ignore


class OnlinePatientAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["appointment_id", "appointment_date"]
        labels = {
            "appointment_id": "Appointment ID",
            "appointment_date": "appointment_date",
        }


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            "name",
            "profile_image",
            "speciality",
            "phone_number",
            "address",
            "experience",
            "about",
            "education",
        ]
        labels = {
            "name": "Full Name",
            "profile_image": "Profile Image",
            "speciality": "Speciality",
            "phone_number": "Phone Number",
            "address": "Address",
            "experience": "Years of Experience",
            "about": "About",
            "education": "Education & Qualifications",
        }

class InventoryItemsForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = [
            "name",
            "quantity",
            "price",
        ]

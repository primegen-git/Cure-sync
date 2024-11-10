# Smart-India-Hackathon
File breakdown:
pycache: This directory stores compiled Python bytecode files for faster execution.
migrations: Contains files that track database schema changes and migrations.
templates: Stores HTML templates used for rendering views.
admin.py: Defines the administrative interface for managing models and data.
apps.py: Configures the app's metadata.
models.py: Defines the database models representing the app's data structures.
tests.py: Contains unit tests for the app's functionality.
urls.py: Defines the URL patterns for the app.
views.py: Contains the view functions that handle HTTP requests and generate responses.
forms.py: (Optional) Defines custom forms used in the app



Applications:
Home: The landing page that leads directly into index.html
Hospital: Application dealing with hospital requests and doctor user details and features
OPD: Application dealing with OPD booking, appointments and other user based features
SIH: Adding User interface and accessibility

Home urls.py
Login: /login/ - Handles the login process for doctors.
Logout: /logout/ - Handles the logout process for doctors.
Home: /home/ - Displays the home page for doctors.
Products: /products/ - Lists available products or services.
Profile: /profile/ - Displays the doctor's profile information.
Appointment: /appointment/ - Handles appointment-related actions (e.g., scheduling, viewing).
Earning: /earning/ - Displays the doctor's earnings or revenue.
Appointment Request: /appointment_request/ - Handles appointment requests from patients.
Patient Report: /patient_report/<str:id>/ - Displays the report for a specific patient.

Hospitals urls.py
hospital/ - Handles the hospital details to be shown

Sih urls.py
/admin/: Points to the Django admin interface.
path("", include(home_urls, namespace="home")): Includes URLs from the home app, accessible through the root URL (/) and assigned the namespace "home".
Similar patterns exist for the hospital, user, and OPD apps, each with their own namespace.

Opd urls.py
Login: /login/ - Handles the login process for doctors.
Logout: /logout/ - Handles the logout process for doctors.
Home: /home/ - Displays the home page for doctors.
Products: /products/ - Lists available products or services.
Profile: /profile/ - Displays the doctor's profile information.
Appointment: /appointment/ - Handles appointment-related actions (e.g., scheduling, viewing).
Earning: /earning/ - Displays the doctor's earnings or revenue.
Appointment Request: /appointment_request/ - Handles appointment requests from patients.
Patient Report: /patient_report/<str:id>/ - Displays the report for a specific patient.

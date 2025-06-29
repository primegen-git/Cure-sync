# OPD Fullstack - Hospital Outpatient Department Management System

A comprehensive full-stack web application for managing hospital outpatient department (OPD) operations, built with Django.

## Features

- **User Authentication:** Secure login and registration for hospital staff and users.
- **Patient Management:** Add, view, update, and delete patient records with detailed medical and billing information.
- **Appointment Scheduling:** Book, view, and manage patient appointments.
- **Hospital Administration:** Manage hospital details, departments, and staff.
- **Revenue & Analytics:** Visualize revenue trends and department-wise earnings with interactive charts.
- **Responsive UI:** Modern, user-friendly interface with custom CSS and JavaScript enhancements.
- **Role-Based Access:** Different access levels for admin, doctors, and staff.
- **Reports:** Generate and view detailed patient medical and billing reports.

## Tech Stack

- **Backend:** Django, Django ORM
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (default, can be switched to PostgreSQL/MySQL)
- **Other:** Chart.js/ApexCharts for analytics, Django Admin for backend management

## Project Structure

```
opd_fullstack/
├── manage.py
├── home/
├── hospital/
├── opd/
├── sih/
├── static/
├── staticfiles/
├── templates/
├── user/
└── media/
```

- **home/**: Landing page and general site views
- **hospital/**: Hospital and department management
- **opd/**: Core OPD logic (patients, appointments, billing, reports)
- **user/**: User authentication and profile management
- **static/** & **staticfiles/**: CSS, JS, and image assets
- **templates/**: HTML templates for all modules

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/opd_fullstack.git
   cd opd_fullstack
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the app:**
   - Open [http://localhost:8000](http://localhost:8000) in your browser.

## Screenshots


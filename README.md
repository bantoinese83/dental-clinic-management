# 🦷 Dental Clinic Management System

Welcome to the Dental Clinic Management System! This project is designed to manage various aspects of a dental clinic, including appointments, billing, patient records, and more.

## 🚀 Features

- **User Authentication**: Secure login and registration for patients, dentists, and admins.
- **Appointment Management**: Create, update, and delete dental appointments.
- **Patient Records**: Manage patient information and medical history.
- **Billing System**: Handle billing records and payment statuses.
- **Dentist Availability**: Manage dentist schedules and availability.
- **Feedback System**: Collect feedback from patients about their appointments.

## 🛠️ Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/bantoinese83/dental-clinic-management.git
    cd dental-clinic-management
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements/dev.txt
    ```

4. **Set up the database**:
    ```bash
    alembic upgrade head
    ```

5. **Run the application**:
    ```bash
    uvicorn src.main:app --reload
    ```

## 📋 API Endpoints

### Authentication

- **Register**: `POST /auth/register`
- **Login**: `POST /auth/token`

### Appointments

- **Create Appointment**: `POST /appointment/dental/appointments`
- **Get Appointments by Patient**: `GET /appointment/dental/patients/{patient_id}/appointments`
- **Get Appointment Details**: `GET /appointment/dental/appointments/{appointment_id}`
- **Update Appointment**: `PUT /appointment/dental/appointments/{appointment_id}`
- **Delete Appointment**: `DELETE /appointment/dental/appointments/{appointment_id}`

### Billing

- **Create Billing Record**: `POST /billing/`
- **Get Billing Records by Patient**: `GET /billing/patient/{patient_id}`
- **Update Billing Record**: `PUT /billing/{billing_id}`
- **Delete Billing Record**: `DELETE /billing/{billing_id}`

### Dentists

- **Create Dentist**: `POST /dentist/dentists`
- **Get Dentist by ID**: `GET /dentist/dentists/{dentist_id}`
- **Update Dentist**: `PUT /dentist/dentists/{dentist_id}`
- **Delete Dentist**: `DELETE /dentist/dentists/{dentist_id}`

### Availability

- **Create Availability**: `POST /availability/`
- **Get Availability by Dentist ID**: `GET /availability/{dentist_id}`
- **Update Availability**: `PUT /availability/{availability_id}`
- **Delete Availability**: `DELETE /availability/{availability_id}`

## 🧪 Running Tests

To run the tests, use the following command:

```bash
pytest
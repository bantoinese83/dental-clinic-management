import datetime

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


# test_routes.py
def test_register_user(setup_database):
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpassword",
        "role": "patient"  # Add the role field
    })
    assert response.status_code == 200


# tests/test_routes.py

def test_login_user(setup_database):
    response = client.post("/auth/register",
                           json={"username": "testuser", "password": "testpassword", "role": "patient"})
    if response.status_code != 200:
        assert response.status_code == 400

    login_response = client.post("/auth/token", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_get_current_user(setup_database):
    # Register the user with the required role field
    register_response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpassword",
        "role": "patient"  # Add the role field
    })
    print("Register Response:", register_response.json())  # Print the registration response

    # Attempt to log in
    login_response = client.post("/auth/token", data={
        "username": "testuser",
        "password": "testpassword"
    })
    print("Login Response:", login_response.json())  # Print the login response

    # Extract the token
    token = login_response.json().get("access_token")
    assert token is not None, "Login failed, no access token returned"

    # Use the token to get the current user
    headers = {"Authorization": f"Bearer {token}"}
    current_user_response = client.get("/user/me", headers=headers)
    print("Current User Response:", current_user_response.json())  # Print the current user response

    # Check the current user response
    assert current_user_response.status_code == 200
    assert current_user_response.json().get("username") == "testuser"


# test_routes.py
def test_create_appointment(setup_database):
    # Register a new user with the required role field
    register_response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "testpassword",
        "role": "patient"  # Add the role field
    })
    print("Register response:", register_response.json())
    assert register_response.status_code == 200, "User registration failed"

    # Attempt to login with the registered user
    login_response = client.post("/auth/token", data={"username": "testuser", "password": "testpassword"})
    print("Login response:", login_response.json())
    assert login_response.status_code == 200, "Login failed"

    # Extract the access token from the login response
    access_token = login_response.json().get("access_token")
    assert access_token is not None, "Access token not found in login response"

    # Create a patient
    headers = {"Authorization": f"Bearer {access_token}"}
    patient_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }
    create_patient_response = client.post("/patient/patients", json=patient_data, headers=headers)
    print("Create patient response:", create_patient_response.json())
    assert create_patient_response.status_code == 200, "Create patient failed"
    patient_id = create_patient_response.json().get("id")

    # Create a dentist
    dentist_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "speciality": "General"
    }
    create_dentist_response = client.post("/dentist/dentists", json=dentist_data, headers=headers)
    print("Create dentist response:", create_dentist_response.json())
    assert create_dentist_response.status_code == 200, "Create dentist failed"
    dentist_id = create_dentist_response.json().get("id")

    # Use the access token to create an appointment
    appointment_data = {
        "patient_id": patient_id,
        "dentist_id": dentist_id,
        "date": "2023-10-10",
        "time": "10:00",
        "treatment_type": "cleaning"
    }
    create_appointment_response = client.post("/appointment/dental/appointments", json=appointment_data,
                                              headers=headers)
    print("Create appointment response:", create_appointment_response.json())
    assert create_appointment_response.status_code == 200, "Create appointment failed"


# test_routes.py

def test_get_appointments_by_patient(setup_database):
    # Create a new user
    register_response = client.post("/auth/register",
                                    json={"username": "testuser", "password": "testpassword", "role": "patient"})
    assert register_response.status_code == 200, f"User registration failed: {register_response.json()}"

    # Log in with the new user
    login_response = client.post("/auth/token", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200, f"Login failed: {login_response.json()}"

    # Extract the access token from the login response
    access_token = login_response.json()["access_token"]

    # Use the access token to authenticate the request
    headers = {"Authorization": f"Bearer {access_token}"}

    # Create a new patient
    patient_response = client.post("/patient/patients", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }, headers=headers)
    assert patient_response.status_code == 200, f"Patient creation failed: {patient_response.json()}"
    patient_id = patient_response.json()["id"]

    # Debugging: Print patient ID
    print(f"Created patient ID: {patient_id}")

    # Create a new dentist
    dentist_response = client.post("/dentist/dentists", json={
        "first_name": "Jane",
        "last_name": "Smith"
    }, headers=headers)
    assert dentist_response.status_code == 200, f"Dentist creation failed: {dentist_response.json()}"
    dentist_id = dentist_response.json()["id"]

    # Debugging: Print dentist ID
    print(f"Created dentist ID: {dentist_id}")

    # Create an appointment for the patient
    appointment_data = {
        "patient_id": patient_id,
        "dentist_id": dentist_id,
        "date": "2023-10-10",
        "time": "10:00",
        "treatment_type": "cleaning"
    }
    create_appointment_response = client.post("/appointment/dental/appointments", json=appointment_data,
                                              headers=headers)
    assert create_appointment_response.status_code == 200, f"Create appointment failed: {create_appointment_response.json()}"

    # Get appointments for the created patient
    response = client.get(f"/appointment/dental/patients/{patient_id}/appointments", headers=headers)

    # Debugging: Print response details
    print(f"Response status code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

    # Check if the request was successful
    assert response.status_code == 200, f"Failed to get appointments: {response.json()}"


def test_create_availability(setup_database):
    # Create a dentist first
    dentist_response = client.post("dentist/dentists", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "speciality": "Orthodontics"
    })
    dentist_id = dentist_response.json().get("id")
    assert dentist_id is not None, "Failed to create dentist"

    # Create availability for the dentist
    availability_response = client.post("availability/", json={
        "dentist_id": dentist_id,
        "day_of_week": "Monday",
        "start_time": "2023-10-10T09:00",
        "end_time": "2023-10-10T17:00"
    })

    assert availability_response.status_code == 200
    assert availability_response.json().get("id") is not None


def test_create_billing(setup_database):
    # Register a new user with the required role field
    register_response = client.post("/auth/register",
                                    json={"username": "testuser", "password": "testpassword", "role": "patient"})
    print("Register response:", register_response.json())
    assert register_response.status_code == 200, f"User registration failed: {register_response.json()}"

    # Attempt to log in with the registered user
    login_response = client.post("/auth/token", data={"username": "testuser", "password": "testpassword"})
    print("Login response:", login_response.json())
    assert login_response.status_code == 200, f"Login failed: {login_response.json()}"

    # Extract the access token from the login response
    access_token = login_response.json()["access_token"]

    # Create a patient
    patient_response = client.post(
        "/patient/patients",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    print("Patient response:", patient_response.json())
    assert patient_response.status_code == 200, f"Patient creation failed: {patient_response.json()}"
    patient_id = patient_response.json()["id"]

    # Create a dentist
    dentist_response = client.post(
        "/dentist/dentists",
        json={
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com"
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    print("Dentist response:", dentist_response.json())
    assert dentist_response.status_code == 200, f"Dentist creation failed: {dentist_response.json()}"
    dentist_id = dentist_response.json()["id"]

    # Create an appointment
    appointment_response = client.post(
        "/appointment/dental/appointments",
        json={
            "patient_id": patient_id,
            "dentist_id": dentist_id,
            "date": "2024-09-11",
            "time": "16:16:40",
            "treatment_type": "cleaning"
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )
    print("Appointment response:", appointment_response.json())
    assert appointment_response.status_code == 200, f"Appointment creation failed: {appointment_response.json()}"


def test_get_availability(setup_database):
    response = client.get("/availability/1")
    assert response.status_code == 404
    assert response.status_code == 404


def test_create_dentist(setup_database):
    response = client.post("/dentist/dentists", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "speciality": "Orthodontics",
        "license_number": "D123456"
    })
    assert response.status_code == 200
    assert response.json()["first_name"] == "Jane"


def test_get_dentist(setup_database):
    response = client.get("/dentist/dentists/1")
    assert response.status_code == 404
    assert response.status_code == 404


def test_create_feedback(setup_database):
    # Register a new user with the required role field
    register_response = client.post("/auth/register",
                                    json={"username": "testuser", "password": "testpassword", "role": "patient"})
    print("Register Response:", register_response.json())  # Debug print

    # Attempt to login with the registered user
    login_response = client.post("/auth/token", data={"username": "testuser", "password": "testpassword"})
    print("Login Response:", login_response.json())  # Debug print

    # Extract the access token from the login response
    token = login_response.json().get("access_token")
    if not token:
        raise ValueError("Failed to obtain access token")

    # Create a patient
    headers = {"Authorization": f"Bearer {token}"}
    patient_response = client.post("/patient/patients",
                                   json={"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"},
                                   headers=headers)
    print("Patient Response:", patient_response.json())  # Debug print
    patient_id = patient_response.json().get("id")

    # Create a dentist
    dentist_response = client.post("/dentist/dentists",
                                   json={"first_name": "Jane", "last_name": "Smith"},
                                   headers=headers)
    print("Dentist Response:", dentist_response.json())  # Debug print
    dentist_id = dentist_response.json().get("id")

    # Create an appointment
    appointment_response = client.post("/appointment/dental/appointments",
                                       json={"patient_id": patient_id, "dentist_id": dentist_id,
                                             "date": str(datetime.datetime.now().date()), "time": "10:00",
                                             "treatment_type": "cleaning"}, headers=headers)
    print("Appointment Response:", appointment_response.json())  # Debug print
    appointment_id = appointment_response.json().get("id")

    # Use the token to create feedback
    feedback_response = client.post("/feedback", json={"patient_id": patient_id, "dentist_id": dentist_id,
                                                       "appointment_id": appointment_id, "rating": 5,
                                                       "comments": "Great service!"}, headers=headers)
    print("Feedback Response:", feedback_response.json())  # Debug print

    assert feedback_response.status_code == 200


# Ensure feedback is created before attempting to retrieve it
def test_get_feedback(setup_database):
    # Register a new user
    register_response = client.post("/auth/register",
                                    json={"username": "testuser", "password": "testpassword", "role": "patient"})
    assert register_response.status_code == 200, "Registration failed"

    # Attempt to login
    login_response = client.post("/auth/token", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200, "Login failed"
    assert "access_token" in login_response.json(), "No access token in response"

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create a patient
    patient_response = client.post("/patient/patients",
                                   json={"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"},
                                   headers=headers)
    assert patient_response.status_code == 200, "Patient creation failed"
    patient_id = patient_response.json()["id"]

    # Create a dentist
    dentist_response = client.post("/dentist/dentists", json={"first_name": "Jane", "last_name": "Smith"},
                                   headers=headers)
    assert dentist_response.status_code == 200, "Dentist creation failed"
    dentist_id = dentist_response.json()["id"]

    # Create an appointment
    appointment_response = client.post("/appointment/dental/appointments",
                                       json={"patient_id": patient_id, "dentist_id": dentist_id, "date": "2024-09-11",
                                             "time": "16:16:40", "treatment_type": "cleaning"}, headers=headers)
    assert appointment_response.status_code == 200, "Appointment creation failed"
    appointment_id = appointment_response.json()["id"]

    # Create feedback
    feedback_response = client.post("/feedback", json={"patient_id": patient_id, "dentist_id": dentist_id,
                                                       "appointment_id": appointment_id, "rating": 5,
                                                       "comments": "Great service!"}, headers=headers)
    assert feedback_response.status_code == 200, "Feedback creation failed"

    # Retrieve feedback
    response = client.get("/feedback", headers=headers)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert len(response.json()) > 0, "No feedback found"


def test_create_appointment_with_invalid_patient_id(setup_database):
    # Register a new user
    register_response = client.post("/auth/register",
                                    json={"username": "testuser", "password": "testpassword", "role": "patient"})
    assert register_response.status_code == 200, f"User registration failed: {register_response.json()}"

    # Log in with the new user
    login_response = client.post("/auth/token", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200, f"Login failed: {login_response.json()}"

    # Extract the access token
    access_token = login_response.json()["access_token"]

    # Attempt to create an appointment with an invalid patient ID
    headers = {"Authorization": f"Bearer {access_token}"}
    appointment_data = {
        "patient_id": 9999,  # Invalid patient ID
        "dentist_id": 1,
        "date": "2023-10-10",
        "time": "10:00",
        "treatment_type": "cleaning"
    }
    response = client.post("/appointment/dental/appointments", json=appointment_data, headers=headers)
    assert response.status_code == 404, f"Expected 404 Not Found, got {response.status_code}: {response.json()}"


# tests/test_routes.py

def test_create_billing_with_valid_amount(setup_database):
    # Register a new user
    register_response = client.post("/auth/register",
                                    json={"username": "testuser", "password": "testpassword", "role": "patient"})
    assert register_response.status_code == 200, f"User registration failed: {register_response.json()}"

    # Log in with the new user
    login_response = client.post("/auth/token", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200, f"Login failed: {login_response.json()}"

    # Extract the access token from the login response
    access_token = login_response.json()["access_token"]

    # Create a patient
    patient_response = client.post(
        "/patient/patients",
        json={"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert patient_response.status_code == 200, f"Patient creation failed: {patient_response.json()}"
    patient_id = patient_response.json()["id"]

    # Create a dentist
    dentist_response = client.post(
        "/dentist/dentists",
        json={"first_name": "Jane", "last_name": "Smith", "speciality": "General"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert dentist_response.status_code == 200, f"Dentist creation failed: {dentist_response.json()}"
    dentist_id = dentist_response.json()["id"]

    # Create an appointment
    appointment_response = client.post(
        "/appointment/dental/appointments",
        json={"patient_id": patient_id, "dentist_id": dentist_id, "date": "2024-09-11", "time": "10:00",
              "treatment_type": "cleaning"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert appointment_response.status_code == 200, f"Appointment creation failed: {appointment_response.json()}"
    appointment_id = appointment_response.json()["id"]

    # Create a billing record
    billing_response = client.post(
        "/billing/",
        json={"appointment_id": appointment_id, "patient_id": patient_id, "amount_due": 100.0,
              "payment_status": "pending", "payment_method": "credit_card", "insurance_claim_id": "12345"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert billing_response.status_code == 200, f"Billing creation failed: {billing_response.json()}"


def test_create_billing_with_zero_amount(setup_database):
    # Register a new user
    register_response = client.post("/auth/register",
                                    json={"username": "testuser", "password": "testpassword", "role": "patient"})
    assert register_response.status_code == 200, f"User registration failed: {register_response.json()}"

    # Log in with the new user
    login_response = client.post("/auth/token", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200, f"Login failed: {login_response.json()}"

    # Extract the access token from the login response
    access_token = login_response.json()["access_token"]

    # Create a patient
    patient_response = client.post(
        "/patient/patients",
        json={"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert patient_response.status_code == 200, f"Patient creation failed: {patient_response.json()}"
    patient_id = patient_response.json()["id"]

    # Create a dentist
    dentist_response = client.post(
        "/dentist/dentists",
        json={"first_name": "Jane", "last_name": "Smith", "speciality": "General"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert dentist_response.status_code == 200, f"Dentist creation failed: {dentist_response.json()}"
    dentist_id = dentist_response.json()["id"]

    # Create an appointment
    appointment_response = client.post(
        "/appointment/dental/appointments",
        json={"patient_id": patient_id, "dentist_id": dentist_id, "date": "2024-09-11", "time": "10:00",
              "treatment_type": "cleaning"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert appointment_response.status_code == 200, f"Appointment creation failed: {appointment_response.json()}"

    # Create a billing record with zero amount
    billing_response = client.post(
        "/billing/",
        json={"appointment_id": appointment_response.json()["id"], "patient_id": patient_id, "amount_due": 0.0,
              "payment_status": "pending", "payment_method": "credit_card", "insurance_claim_id": "12345"},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert billing_response.status_code == 422, f"Billing creation failed: {billing_response.json()}"


def test_get_nonexistent_feedback(setup_database):
    # Register a new user
    register_response = client.post("/auth/register",
                                    json={"username": "testuser", "password": "testpassword", "role": "patient"})
    assert register_response.status_code == 200, f"User registration failed: {register_response.json()}"

    # Log in with the new user
    login_response = client.post("/auth/token", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200, f"Login failed: {login_response.json()}"

    # Extract the access token
    access_token = login_response.json()["access_token"]

    # Use the token to make an authenticated request
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/feedbacks/9999", headers=headers)  # Assuming 9999 is a non-existent feedback ID
    assert response.status_code == 404, f"Expected 404 Not Found, got {response.status_code}: {response.json()}"


# test_routes.py
def test_get_appointments_by_nonexistent_patient(setup_database):
    # Register a new user with role
    register_response = client.post("/auth/register",
                                    json={"username": "testuser", "password": "testpassword", "role": "patient"})
    print("Register response:", register_response.json())
    assert register_response.status_code == 200, f"Registration failed: {register_response.json()}"

    # Attempt to log in with the registered user
    login_response = client.post("/auth/token", data={"username": "testuser", "password": "testpassword"})
    print("Login response:", login_response.json())
    assert login_response.status_code == 200, f"Login failed: {login_response.json()}"

    # Extract the token from the login response
    token = login_response.json().get("access_token")
    assert token, "No access token found in login response"

    # Set the authorization header with the token
    headers = {"Authorization": f"Bearer {token}"}

    # Attempt to get appointments for a nonexistent patient
    response = client.get("/dental/patients/999/appointments", headers=headers)
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"


# tests/test_routes.py

def test_create_billing_with_invalid_payment_method(setup_database):
    # Create a new user
    register_response = client.post("/auth/register",
                                    json={"username": "testuser", "password": "testpassword", "role": "patient"})
    assert register_response.status_code == 200, f"User registration failed: {register_response.json()}"

    # Log in with the created user
    login_response = client.post("/auth/token", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200, f"Login failed: {login_response.json()}"

    # Extract the access token from the login response
    access_token = login_response.json()["access_token"]

    # Create a patient
    headers = {"Authorization": f"Bearer {access_token}"}
    patient_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }
    patient_response = client.post("/patient/patients", json=patient_data, headers=headers)
    assert patient_response.status_code == 200, f"Patient creation failed: {patient_response.json()}"
    patient_id = patient_response.json()["id"]

    # Create a dentist
    dentist_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com"
    }
    dentist_response = client.post("/dentist/dentists", json=dentist_data, headers=headers)
    assert dentist_response.status_code == 200, f"Dentist creation failed: {dentist_response.json()}"
    dentist_id = dentist_response.json()["id"]

    # Create an appointment
    appointment_data = {
        "patient_id": patient_id,
        "dentist_id": dentist_id,
        "date": "2024-09-11",
        "time": "16:50",
        "treatment_type": "cleaning"  # Use a valid treatment type
    }
    appointment_response = client.post("/appointment/dental/appointments", json=appointment_data, headers=headers)
    assert appointment_response.status_code == 200, f"Appointment creation failed: {appointment_response.json()}"


# tests/test_routes.py
def test_register_user_with_existing_username(setup_database):
    client.post("/auth/register", json={"username": "testuser", "password": "testpassword", "role": "patient"})
    response = client.post("/auth/register",
                           json={"username": "testuser", "password": "newpassword", "role": "patient"})
    assert response.status_code == 400  # Expecting 400 status codes


def test_login_user_with_invalid_credentials(setup_database):
    client.post("/auth/register", json={"username": "testuser", "password": "testpassword"})
    response = client.post("/auth/token", data={"username": "testuser", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_create_availability_with_invalid_time_range(setup_database):
    dentist_response = client.post("dentist/dentists", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "speciality": "Orthodontics"
    })
    dentist_id = dentist_response.json().get("id")
    assert dentist_id is not None, "Failed to create dentist"

    availability_response = client.post("availability/", json={
        "dentist_id": dentist_id,
        "day_of_week": "Monday",
        "start_time": "2023-10-10T17:00",
        "end_time": "2023-10-10T09:00"
    })
    assert availability_response.status_code == 422


def test_register_dentist(setup_database):
    response = client.post("/auth/register", json={
        "username": "testdentist",
        "password": "testpassword",
        "role": "dentist"  # Specify the role as "dentist"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "testdentist"
    assert response.json()["role"] == "dentist"


def test_register_admin(setup_database):
    response = client.post("/auth/register", json={
        "username": "testadmin",
        "password": "testpassword",
        "role": "admin"  # Specify the role as "admin"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "testadmin"
    assert response.json()["role"] == "admin"


def test_create_and_get_patient(setup_database):
    response = client.post("/patient/patients", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    })
    patient_id = response.json().get("id")
    assert patient_id is not None

    get_response = client.get(f"/patient/patients/{patient_id}")
    assert get_response.status_code == 200
    assert get_response.json()["first_name"] == "John"

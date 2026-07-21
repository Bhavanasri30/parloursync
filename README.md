# ParlourSync – Beauty Parlour Appointment Booking Platform

ParlourSync is a web-based Beauty Parlour Appointment Booking Platform that allows customers to book beauty services online while helping parlour owners manage appointments, services, staff, and customers efficiently. The platform replaces manual appointment booking with a simple, organized, and user-friendly digital system.

---

## Features

### Customer
- User Registration & Login
- Browse Beauty Services
- Book Appointments
- View Appointment History
- Cancel Appointments
- Update Profile

### Admin / Parlour Owner
- Dashboard
- Manage Customers
- Manage Services
- Manage Staff
- Manage Appointments
- Track Payments
- View Business Statistics

### Freelance Beauticians
- Create Professional Profile
- Add Services
- Set Availability
- Receive Customer Bookings
- Manage Appointments

---

## Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap

### Backend
- Python
- Flask

### Database
- MySQL
- SQLAlchemy

### Tools
- VS Code
- GitHub
- Git
- Figma

---

## Project Structure

```
ParlourSync/
│
├── app.py
├── config.py
├── requirements.txt
├── models.py
├── forms.py
├── routes.py
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── booking.html
│   ├── dashboard.html
│   └── profile.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── database/
│
└── README.md
```

---

## System Workflow

1. Customer registers or logs in.
2. Customer browses available beauty services.
3. Customer selects a preferred date and time.
4. Appointment request is submitted.
5. Admin confirms the appointment.
6. Customer receives the service.
7. Payment is completed.
8. Appointment history is stored.

---

## System Architecture

```
Customer
      │
      ▼
Frontend
(HTML, CSS, JavaScript)
      │
HTTP Request
      │
      ▼
Flask Backend
      │
      ▼
MySQL Database
      │
      ▼
Admin Dashboard
```

---

## Database Tables

- Users
- Customers
- Staff
- Services
- Appointments
- Payments
- Freelance Beauticians

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/parloursync.git
```

### Move to Project Folder

```bash
cd parloursync
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Database

Update your MySQL credentials in:

```
config.py
```

### Run the Application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## Future Enhancements

- Online Payment Gateway
- SMS & Email Notifications
- AI Appointment Recommendations
- Mobile Application
- Loyalty & Rewards Program
- Multi-Branch Parlour Support
- Analytics Dashboard
- Customer Reviews & Ratings

---

## Advantages

- Easy Online Appointment Booking
- Reduces Manual Work
- Prevents Double Bookings
- Better Customer Management
- Efficient Staff Scheduling
- Organized Business Operations
- User-Friendly Interface
- Time Saving

---

## Target Users

- Customers
- Beauty Parlour Owners
- Staff Members
- Freelance Beauticians

---

## Authors

Developed by the ParlourSync Team

---

## License

This project is developed for educational purposes as a college mini project.

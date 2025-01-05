# MORPHEUS

## Overview
This project is a dynamic form builder and response system built with Django. Users can create customizable forms, submit responses, and view analytics. It supports various question types.

## Features
- Form creation and management
- Multiple question types (Text, Dropdown, Checkbox, File Upload, etc.)
- User-friendly form submission
- Analytics and response tracking
- Simple, responsive user interface

## Requirements
- Python 3.x
- Django 3.x or higher
- Database (SQL)

## Setup Instructions

### 1. Clone the Repository
```
git clone https://github.com/SiddhanthShah100/morpheus.git
cd form_builder
```

### 2. Configure Database
Add your Db name in settings.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'form_db_builder',
        'USER': '****',
        'PASSWORD': '*****',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
```
python manage.py makemigrations
python manage.py migrate
```

### 3. Create a Superuser
```
python manage.py createsuperuser
```

### 4. Run the Development Server
```
python manage.py runserver

```

Application will be available at http://127.0.0.1:8000

### Access the Admin Panel
Login to the Django admin panel at
```
http://127.0.0.1:8000/admin
```
using the superuser credentials you created earlier.


## How to Use

### 1. **Create Forms**
- **Route:** `http://127.0.0.1:8000/create`

### 2. **Submit Responses**
- **Route:** `http://127.0.0.1:8000/<form_id>/respond/`
- Users can visit the form page, answer the questions, and submit their responses.

### 3. **View Responses**
- **Route:** `http://127.0.0.1:8000/<form_id>/responses/`
- Admins can view responses in the admin panel or directly through the "View Responses" button.

### 4. **View Analytics**
- **Route:** `http://127.0.0.1:8000/<form_id>/analytics/`
- Analytics will be available for each form, showing metrics such as total responses and breakdowns for various question types.

---

## Documentation

### Form Creation
- Forms can be created with various question types (Text, Dropdown, Checkbox, File Upload, etc.).
- Each question can be given options for dropdowns and checkboxes.
- The form can be saved and viewed by the users.

### Question Types
- **Text**: A single-line input field for user responses.
- **Dropdown**: A list of options for the user to choose from.
- **Checkbox**: Multiple options that can be selected.
- **File Upload**: Allows users to upload files.
- **Slider**: A numeric range slider for users to select values.
- **Ranking**: Users can rank multiple items in order.

### Response Collection
- **Route for Form Submission**: `http://127.0.0.1:8000/<form_id>/respond/`
  - Users fill out forms and submit them.
  - Responses are stored in the database with associated form data.
  - Admins can view responses for each form.

### Analytics
- **Route for Viewing Analytics**: `http://127.0.0.1:8000/<form_id>/analytics/`
  - Analytics can be viewed to track response trends, breakdowns for text answers, and summary counts for checkbox and dropdown selections.

---

## Notes
- This project is designed to be extended, allowing for more question types and dynamic features.
- You can customize the styling by modifying `styles.css`.
- To implement additional functionality like email notifications or advanced analytics, further development is required.



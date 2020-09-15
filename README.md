
# Project Management

###Setup the project:
 - Create a virtual environment:
 
 `virtualenv --python=/usr/bin/python3.6 env`
 
- Clone the repository:

 `git clone https://github.com/JackPrajapati/ProjectManagement.git`

- Install requirements:

 `pip3 install -r requirements.txt`

- Migrate the database:

 `python3 manage.py makemigrations`
 `python3 manage.py migrate`

- Create superuser:
 
 `django-admin createsuper`
 

- Run the project at  [Localhost](localhost:8000 "Localhost")


### Features
- Create projects with name, description, start date and end date.
- Register employee with roles like devloper, team leader, and project manager.
- Assign projects to roles.
- Simplified django admin view with assigned projects to role.
- Protected data view for super user and staff members.
- Custom queryset to view the filtered data.

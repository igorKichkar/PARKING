<h1 align="center">PARKING</h1>.
<h2>The project was created based on the Django framework.</h2>

PARKING app allows you to manage parking spaces.

The administrator can appoint a user as a manager.
- Login: admin
- Password: 1

### Employees can:
- Register on the site.
- Book parking spaces for an available time.
- Edit booking records.
- Delete records.

### Managers can:
- Add, remove parking spaces.
- Book parking spaces for the available time for employees.
- Edit booking records for employees.
- Delete records for employees.


### When creating a PARKING, the following were used:
- Django framework.
- Sqlite database.

### To start the server, you need to:
- Clone the repository PARKING.
- Set the virtual environment in the project folder:
```
python3 -m venv .venv
```
- Activate virtual environment:
```
source .venv/bin/activate
```
- Install Django:
```
pip3 install django
```
- Start the server:
```
./manage.py runserver
```

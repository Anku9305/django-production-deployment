# Django Production Deployment on AWS EC2

This project demonstrates how to deploy a Django application on an AWS EC2 instance using Gunicorn and Nginx.

## Tech Stack

- Python
- Django
- Gunicorn
- Nginx
- AWS EC2
- Ubuntu
- Git & GitHub

## Project Structure

manage.py – Django management script  
core/ – Django application  
myproject/ – Django project configuration  

## Deployment Steps

1. Created AWS EC2 instance
2. Connected via SSH
3. Installed Python and pip
4. Installed Django and project dependencies
5. Ran migrations and collected static files
6. Configured Gunicorn as WSGI server
7. Configured Nginx as reverse proxy
8. Bound Gunicorn with Nginx
9. Started services and verified deployment

## Author

Ankush Chaubey

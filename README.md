# ApleHotels
Online hotels booking service.

Aplehotels is a platform for online booking of hotels for reservations. Customers can select the available hotels within wanted region and confirm the advance reservation by paying in advance. Customers also get necessary confirmations by emails and history of their reservations. 
> **Note:** This is in development phase. Some extra features are still to be added. Although the main functionalities work fine.

## Setup

### Database
1. Django provided SQLite3 or MySQL databases are used to store data.

### Installation
1. python 3 and above is required. 
2. To setup virtual environment for our project. follow below commands to create one,
  To create virtual environment.
    
      pip install virtualenv
      
      eg. cd C:\Users\user\Desktop\UserDjangoProject> pip install virtualenv
      
  Create the virtual environment using following command.(can use any name for virtual environment instead 'venv')
  
      virtualenv -p python3 venv
      
  To activate virtual environment. use following commands,
  
      venv\Scripts\activate
      
      it will look like following,
      eg. (venv) C:\Users\user\Desktop\UserDjangoProject>
    
3. Now our virtual environment is active. Install Django within current active virtual environment.
  
       pip install django
      
4. create superuser for project using following command

       django-admin create superuser
      
5. Change the directory to our project with requirements.txt file within,
6. To install all of the required packages for project run following command,

       pip install -r requirements.txt

7. As all the packages are downloaded in current virtual environment. go ahead and run the following command to run project,

       python manage.py runserver
        
8. Get a copy of this code using git, or by downloading the zip

       git clone https://github.com/sachin30/aplehotels.git
    
9. For using payment functionality Create Razorpay account.

10. Django celery is used for email sending tasks. Open another cmd prompt and run following command, Make sure redis is installed on your system and running.

       celery -A  hotels.celery worker --pool=solo -l info

11. Set Environmental variables
   - `EMAIL_HOST_USER`      :   Email address for sending the emails.
   - `EMAIL_HOST_PASSWORD`  :   Use a gmail app password generated by 2 step verification
   - `razorpay_id`          :   Secret key created from razorpay dashboard
   - `razorpay_account_id`  :   Razorpay account id

12. The project will run on following address by default,
    
    127.0.0.1:8000
    
> **Note:** if u face any genuine problem, contact me at sachinpandhare1996@gmail.com . I am also new to django. Its my first portfolio project.Thank You.

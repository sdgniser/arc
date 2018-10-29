# arc
NISER Archive

#### How to run a local instance?

 * Install: `python`, `postgresql`
 * Clone the repo.
 * Create a virtual environment and install `django`, `django-authtools`, `django-widget-tweaks`, `psycopg2`
 * You'll have to provide the following files: `/arc/keys.py` (containing the SECRET\_KEY) and `/arc/mail.py` (containing the admin's email configuration)
 * You'll also have to fix some of the absolute paths in `/arc/settings.py` because I am lazy.
 * `cd` in the the directory (while you're still in virtual env) and run: `python manage.py collectstatic`, `python manage.py makemigrations`, `python manage.py migrate`
 * Start the server: `python manage.py runserver` OR you can run an apache server, thats how the current development server is running. Configuring an apache server is very machine-specific. Google how to do it on your machine.)
 * Please let me know if you're unable to run it on your machine.

#### WHY ARE WE NOT USING A CDN?!?

Because we plan to run it locally on NISER's intranet, so I think its better to keep a local copy of bootstrap, jquery, open-iconic and other libraries.

##### Note:

I am not expecting any contributions in the python part: views/models/forms, because most of the code is currently spaghetti. However, I am hoping to get some help on JS/CSS part in the templates.

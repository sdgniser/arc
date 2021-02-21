# arc
NISER Archive

#### How to run a local instance?

 * Sit tight. ~~If migrations fail, delete everything (the repo, the database, etc.) and start over.~~ (I have learnt this the hard way: DO NOT TRACK MIGRATIONS FILES, and everything works fine.)
 * Install: `python`, `postgresql`
 * Clone the repo.
 * Create a [virtual environment](https://docs.python.org/3/tutorial/venv.html) and run `pip install -r requirements.txt`.
 * You'll have to provide [`/arc/local_settings.py`](https://pastebin.com/S9yV4yj5).
 * ~~You'll also have to fix some of the absolute paths in `/arc/settings.py` because~~ I am lazy.
 * `cd` to `/main/static/main` and
 `npm install -g jquery popper.js bootstrap katex showdown open-iconic`.
 * `cd` to the cloned repo (while you're still in virtual env) and run: `python manage.py collectstatic`, `python manage.py makemigrations main`, `python manage.py migrate`
 * Start the server: `python manage.py runserver` OR you can run an apache server, thats how the current development server is running. Configuring an apache server is very machine-specific. Google how to do it on your machine.)
 * Please let me know if you're unable to run it on your machine.

 #### TODO:

 * **User model**: currently we are using `django-authtools` which is **not**
   compatible with Django 3.
 * **Django 3**: Make the source compatible with Django 3. I believe that
   `django-authtools` is the only thing that is not compatible, but there might
   be other dependencies which don't support Django 3 yet.
 * **Non-Upload Items**: Add support for items which are not necessarily file
 uploads (for example, links).

# arc
NISER Archive

#### How to run a local instance?

 * Sit tight. ~~If migrations fail, delete everything (the repo, the database, etc.) and start over.~~ (I have learnt this the hard way: DO NOT TRACK MIGRATIONS FILES, and everything works fine.)
 * Install:
    * `python` : Install python 3.9.25 or lower preferably using pyenv(or the more modern uv) as django 2.2.28 does not support python 3.10 and above
    * `postgresql` : Last checked with postgresql18
 * Clone the repo.
 * Create a [virtual environment](https://docs.python.org/3/tutorial/venv.html) using the python version you installed and run `pip install -r requirements.txt`.
 * You'll have to provide `/arc/local_settings.py`(look at the example file attached).
 * Install nodejs and npm systemwide(if not present already) and then 
 `cd` to `/main/static/main` and
 `npm install jquery popper.js bootstrap katex showdown open-iconic`.
 * Make a new database in postgresql and register the database and db account credentials in local_settings.py
 * `cd` to the cloned repo (while you're still in virtual env) and run: `python manage.py collectstatic`, `python manage.py makemigrations main`, `python manage.py migrate`
 * Start the server: `python manage.py runserver` or you can run an apache
   server, thats how the deployed server is running presently. Configuring an
   apache server is very machine-specific. Google how to do it on your
   machine.)
 * For verification mails, update the 'dmn' variable in views.py to the current ip/domain at which you are hosting the site.
 * Please let me know if you're unable to run it on your machine.

 #### TODO:

 * **User model**: currently we are using `django-authtools` which is **not**
   compatible with Django 3.
 * **Django 3**: Make the source compatible with Django 3. I believe that
   `django-authtools` is the only thing that is not compatible, but there might
   be other dependencies which don't support Django 3 yet.
 * **Non-Upload Items**: Add support for items which are not necessarily file
   uploads (for example, links).

 #### Useful Links:

  * Apache - [Debian Wiki](https://wiki.debian.org/Apache), [Arch Wiki](https://wiki.archlinux.org/index.php/Apache_HTTP_Server), [Django on Apache](https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/modwsgi/)
  * Postgres - [Debian Wiki](https://wiki.debian.org/PostgreSql), [Arch Wiki](https://wiki.archlinux.org/index.php/PostgreSQL)
  * Django - [Official Docs](https://docs.djangoproject.com/en/3.1/)
  * HTML - [MDN](https://developer.mozilla.org/en-US/docs/Web/HTML)

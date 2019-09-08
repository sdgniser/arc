# arc
NISER Archive

#### How to run a local instance?

 * Sit tight. ~~If migrations fail, delete everything (the repo, the database, etc.) and start over.~~ (I have learnt this the hard way: DO NOT TRACK MIGRATIONS FILES, and everything works fine.)
 * Install: `python`, `postgresql`
 * Clone the repo.
 * Create a [virtual environment](https://docs.python.org/3/tutorial/venv.html) and run `pip install -r requirements.txt`.
 * You'll have to provide [`/arc/local_settings.py`](https://pastebin.com/S9yV4yj5).
 * ~~You'll also have to fix some of the absolute paths in `/arc/settings.py` because~~ I am lazy.
 * `npm install -g jquery popper.js bootstrap katex showdown open-iconic`. Then, `cd` to `/main/static/main` and create a symlink to the installed dependencies using: `npm link jquery popper.js bootstrap katex open-iconic showdown`.
 * `cd` to the cloned repo (while you're still in virtual env) and run: `python manage.py collectstatic`, `python manage.py makemigrations main`, `python manage.py migrate`
 * Start the server: `python manage.py runserver` OR you can run an apache server, thats how the current development server is running. Configuring an apache server is very machine-specific. Google how to do it on your machine.)
 * Please let me know if you're unable to run it on your machine.

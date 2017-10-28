Getting up and running
----------------------

The steps below will get you up and running with a local development environment. We assume you have the following installed:

* pip
* virtualenv
* PostgreSQL

At first, Linux or MacOs is more suitable to this project than Windows system.
Oracle VirtualBox is a good choice to install a virtual Ubuntu system If your current system is Windows. 
http://www.beopensource.com/2016/05/how-to-install-Ubuntu-1604-LTS-in-Virtual-Box-VmWare.html is a good reference.

The second part is to install portgesql and create a database. we need to return the root at first.
Then, steps are listed:
      1 refresh our local package index by 'sudo apt-get update'.
	  2 install postgres package by 'sudo apt-get install postgresql postgresql-contrib'. 
	  3 to our project, we also need to install backend server by 'postgresql-server-dev-x.y' x.y is the version number. it can 9.5 or others.
	  4 switch over to the postgres account by typing 'sudo -i -u postgres'.
	  5 create a database by 'createdb ulpa_local'(ulpa_local is the name of my local database).
	  6 access a Postgres prompt by 'psql' and then '\connect ulpa_local' to the created database.
        or access ulpa_local prompt by 'ulpa_local'.
	  7 set the database in '\config\settings\common.py'.
	    take my setting as an example:
		DATABASES = {
        # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
        'default': env.db("DATABASE_URL", default="postgres://postgres:3180295@localhost:5432/ulpa_local"),
        }
        here,1234567 is my password , localhost:5432 is the normal settting and ulpa_local is my local database. 

 
Thirdly, we need to install pip, virtualenv as decribed as before after ubuntu is installed in Oracle VirtualBox VM.
to install pip, https://www.rosehosting.com/blog/how-to-install-pip-on-ubuntu-16-04/ is a good reference.
Then, It is virtualenv. steps are listed to get the local project running:
      1  install the virtualenv package: pip install virtualenv
      2  create the environment with virtualenv: virtualenv my_environment
	  3  activate your virtual environment: open the file where you create your virtualenv, then source my_environment/bin/activate
	  4  you are using the virtualenv---my_environment,open a terminal at the project root and install the requirements for local development: 'pip install -r requirements/local.txt'
	  5  create neccessary tables automatically in the local database by migrations: 'python manage.py makemigrations' and 'python manage.py migrate'. you may need to insert data by yourself.
	  6  get running: python manage.py runserver
	  7  stop the running project by ‘Ctrl+C’ and If you want to leave  the virtualenv, entering 'deactivate' is ok.

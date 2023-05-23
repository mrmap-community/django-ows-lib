Development
===========

Please feel free to contribute to this project. The following list describes just the basics to start development. 
Cause some of the used components need further django tools like caches, the dev environment needs a functional django project.
It makes sense, to use a virtual environment. The documentation is actually for Debian 11 

1. Create the virtual environment
---------------------------------

We use venv:

.. code-block:: bash

    $ python -m venv django-ows-lib-dev
    $ source django-ows-lib-dev/bin/activate 


2.  Clone the project
---------------------

You can clone the current development version from github into your dev folder:

.. code-block:: bash

    $ cd django-ows-lib-dev
    $ git clone https://github.com/mrmap-community/django-ows-lib



3.  Install dependencies
------------------------

Dependencies in this project are organized by seperated requirement files under the ``.requirements`` folder.

To install all dependencies to contribute to this project run the command below:

.. code-block:: bash

    $ cd django-ows-lib/
    $ pip install -r requirements.txt
    $ cd ..

.. note::

    The libs are now available in your venv.



4. Create a dummy Django project and app to be able to use and test django-ows-lib
-----------------------------------------------------------------------------------

.. code-block:: bash

    $ python -m django --version
    $ django-admin startproject djangoowslibdev
    $ cd djangoowslibdev
    $ python manage.py startapp owslibtest



5. Create the folder structure to be able to use django commands
----------------------------------------------------------------

.. code-block:: bash

    $ mkdir owslibtest/management
    $ mkdir owslibtest/management/commands
    $ touch owslibtest/management/__init__.py
    $ touch owslibtest/management/commands/__init__.py

.. note:: https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/



6. Register the owslibtest app in the projects settings.py
----------------------------------------------------------

.. code-block:: python

    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'owslibtest',
    ]



7. Create a the python file which can be invoked via django command
-------------------------------------------------------------------

.. code-block:: bash

    $ vi owslibtest/management/commands/test_ows_lib.py

.. code-block:: python

    from django.core.management.base import BaseCommand, CommandError

    class Command(BaseCommand):
        help = "test script for ows management"

        def handle(self, *args, **options):
            self.stdout.write("Hello django-ows-lib!", ending="\n")



8. Running the test from the django project folder
--------------------------------------------------

.. code-block:: bash

    $ python manage.py test_ows_lib

.. note:: It should give back "Hello django-ows-lib!"



9. Install the local lib into the venv to make ows_lib available to the test script
-----------------------------------------------------------------------------------

.. code-block:: bash

    $ pip install ../django-ows-lib/



10. Do the first test - e.g. try to invoke a CSW and parse the result 
---------------------------------------------------------------------
.. code-block:: bash

    $ vi owslibtest/management/commands/test_ows_lib.py

.. code-block:: python

    from django.core.management.base import BaseCommand, CommandError
    from ows_lib.xml_mapper.utils import get_parsed_service
    import requests
    from ows_lib.client.utils import get_client

    class Command(BaseCommand):
        help = "test script for ows management"
        
        def handle(self, *args, **options):
            self.stdout.write("Requesting a CSW via django-ows-lib:", ending="\n")
            r = requests.get('https://gdk.gdi-de.org/geonetwork/srv/ger/csw?request=GetCapabilities&service=CSW&version=2.0.2')
            capabilities_object = get_parsed_service(r.content)  
            client = get_client(capabilities_object)
            get_record_request = client.get_record_by_id_request('2b009ae4-aa3e-ff21-870b-49846d9561b2')
            response = client.send_request(get_record_request)
            # give back getrecordbyid response
            self.stdout.write(str(response.content), ending="\n")

.. code-block:: bash

    $ python manage.py test_ows_lib

.. note:: It should give back "Requesting a CSW via django-ows-lib:" and the GetRecordById respones



11.  Running tests
------------------

As other django based projects we test it with the default django `test command <https://docs.djangoproject.com/en/4.2/topics/testing/overview/#running-tests>`_.

.. code-block:: bash

    $ python manage.py test

.. note::

    Run the above command from the root of the project folder.


12. Build docs
--------------

The documentation are build with `sphinx <https://sphinx-tutorial.readthedocs.io/cheatsheet/#cheat-sheet>`_.

To build the docs local change to the ``docs`` subfolder and run the command below.

.. code-block:: bash

    $ make html

The documentation is present under the subfolder ``build/index.html``


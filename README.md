# Create Database

1. Import Database from dump file to local base
2. Create smartLocAPI/settings_local.py (for example, smartLocAPI/settings_local.py.sample)

# How to start a project

In the project directory, you can run:

1.  Create _new virtual environment_

```
python -m venv env
```

2. Activated a _virtual environment_

```
source env/bin/activate
```

3. Install required lib, after you’ve created and activated a virtual environment

```
python -m pip install -r requirements.txt
```

4. Check actual data

```
python manage.py migrate
```

5. Start project

```
python manage.py runserver 8000
```

6. Now that the server’s running, visit http://127.0.0.1:8000/ or http://localhost:8000/ with your web browser.

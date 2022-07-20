# Book Catalogue Application

### How to run

1. Open terminal -> Go to `code` folder

2. Add ENV variables in the terminal

```
export FLASK_APP=book_api
export FLASK_ENV=development
export DATABASE_URL=sqlite:///${PWD}/app.db
export SECRET_KEY=secret_key_change_as_you_wish_make_it_long_123
```

3. Install dependencies using below command

`pip install -r requirements.txt`

4. Run the application using below command

`python app.py`

5. Go to `http://127.0.0.1:5000`

6. Click on login button and login using below creds -

```
username: admin
password: password
```

You can create your own new account also by going to login -> `New User? Click to Register!` 

7. It will show the list of all the saved books. You can delete a book from the table by clicking on `delete` button.

8. To add a new book search an ISBN and submit it. A new book will be added to the table.
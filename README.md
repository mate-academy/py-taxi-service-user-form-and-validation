# Taxi service user form and validation

Read [the guideline](https://github.com/mate-academy/py-task-guideline/blob/main/README.md) before starting.
- Make sure that you change the settings for [html-files](https://github.com/mate-academy/py-task-guideline/blob/main/html_settings/README.MD).
- Use the following command to load prepared data from fixture to test and debug your code:
  
`python manage.py loaddata taxi_service_db_data.json`

- After loading data from fixture you can use following superuser (or create another one by yourself):
  - Login: `admin.user`
  - Password: `1qazcde3`

Feel free to add more data using admin panel, if needed.

In this task, you will implement a custom form and django built-in forms to create,
update or delete content from the site.

1. Implement:
    - `Create`, `Delete` views for `Driver`, 
2. On the driver list page create a button that leads to the driver creation page.
3. Create a driver's license update page. The form - `DriverLicenseUpdateForm`
on this page must check that license:
    - Consist only of 8 characters
    - First 3 characters are uppercase letters
    - Last 5 characters are digits
    
    Also, don't forget to validate the license number on user creation as well.

4. On the driver detail page add buttons that lead to the driver's license updating page and
driver deletion page.
5. On car creation page switch to checkboxes widget for assigning drivers to car.
6. On the car detail page add button `Assign me to this car`. This button adds 
current user to car drivers. When current user is already a driver of this car, 
there should be `Delete me from this car` button that deletes user from car drivers.

The car detail page should look like this:
![image](https://mate-academy-images.s3.eu-central-1.amazonaws.com/django-forms-1.png)
![image](https://mate-academy-images.s3.eu-central-1.amazonaws.com/django-forms-2.png)

NOTE: Attach screenshots of all created or modified pages to pull request. It's important to attach images not links to them.

### Note: Check your code using this [checklist](checklist.md) before pushing your solution.

# Note
Follow these steps if you need to use `crispy_forms` v2.0 with Python 3.11:

1. Add `CRISPY_TEMPLATE_PACK` to `settings.py`.

```python
CRISPY_TEMPLATE_PACK="bootstrap4"
```

2. Add these apps to `INSTALLED_APPS` and install them corresponding to the `CRISPY_TEMPLATE_PACK` bootstrap version.

```python
INSTALLED APPS = [
   ...,
   "crispy_bootstrap4",
   "crispy_forms",
]
```

# Сheck Your Code Against the Following Points

## Don't Push db files

Make sure you don't push db files (files with `.sqlite`, `.db3`, etc. extension).

## Don't forget to attach all screenshots of created/modified pages

## Code Efficiency

1. Use `UserCreationForm` while creating user.

Good example:

```python
class DriverCreationForm(UserCreationForm):
    pass
```

Bad example:

```python
class DriverCreationForm(forms.ModelForm):
    pass
```

1/2. Validate `license_number` while creating and updating users.
3. Don't forget to add `/` at the end of the URLs.

Good example:

```python
path(
    "manufacurers/create/", 
    ManufacturerCreateView.as_view(), 
    name="manufacturer-create"
),
```

Bad example:

```python
path(
    "manufacurers/create", 
    ManufacturerCreateView.as_view(), 
    name="manufacturer-create"
),
```

1/4. Use `get_user_model()` instead of `Driver`.

## Code Style

1. Make sure you've added a blank line at the end to all your files including `.css`, `.html` and `.gitignore`.
2. Make sure you use 2 whitespaces indentations in your `.html` files.
3. Add `Cancel` button apart from `Delete` one. The `Cancel` button will lead to the previous page the user was on.
4. Group imports using `()` if needed.

Good example:

```python
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    UserPassesTestMixin, 
    PermissionRequiredMixin,
)
```

Bad example:

```python
from django.contrib.auth.mixins import LoginRequiredMixin, \
    UserPassesTestMixin, PermissionRequiredMixin
```

Another bad example:

```python
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    UserPassesTestMixin, PermissionRequiredMixin,
)
```

1/5. Use `-` to split words in URL identification parameter `name`, not the `_`.

Good example:

```python
urlpatterns = [
    path("buses/", BusListView.as_view(), name="bus-list"),
]
 ```

Bad example:

```python
urlpatterns = [
    path("buses/", BusListView.as_view(), name="bus_list"),
]
 ```

## Clean Code

Add comments, prints, and functions to check your solution when you write your code.
Don't forget to delete them when you are ready to commit and push your code.

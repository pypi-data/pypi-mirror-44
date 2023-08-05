# Django Materialize Nav
This library was created to make django work with materializecss. 


## Setup
Install the library.


```python
# project/settings.py

INSTALLED_APPS = [
    "materialize_nav",
    ...
]

```

### Setup Context Processors
Materialize nav comes with a context processor to use some settings to change the default base styling.
```python
# Context Processor to work with settings
TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
                'materialize_nav.context_processors.get_context',
            ],
        },
    },
]

```

Alternative way to get the standard context for views
```python
# views.py

from materialize_nav.context_processors import get_context


def show_page(request):
    # Get the context with the style settings
    context = get_context(site_name='demo', title='Basic Content', primary_color='teal')
    
    context["object"] = "MyObject"
    return render(request, "my_page.html", context)
```


## Style
The base template can be used by extending the materialize base nav.

```html
{% extends "materialize_nav/base.html" %}


{% block nav_items %}
    <li><a href="sass.html">Sass</a></li>
    <li><a href="badges.html">Components</a></li>
    <li><a href="collapsible.html">JavaScript</a></li>
{% endblock %}


{% block sidenav_items %}
    {# This makes the sidenav items reusable in other templates #}
    {% include "my_app/sidenav_items.html" %}
{% endblock %}


{% block contents %}
<div class="row">
    <div class="col s12 m9 l10">
        <p>My Content goes here</p>
    </div>
</div>
{% endblock %}
```

### Styling controls

Materialize nav comes with several style options used in the template context variables listed below.

  * site_name
  * title
  * HIDE_CONTAINER
  * SHOW_SIDENAV
  * FIXED_SIDENAV
  * PRIMARY_COLOR
  * SECONDARY_COLOR
  * PRIMARY_COLOR_LIGHT
  * PRIMARY_COLOR_DARK
  * SUCCESS_COLOR
  * ERROR_COLOR
  * LINK_COLOR
  
If you went through the `Setup Context Processors` step then you can modify several settings to change the default style.
This is an alternative to manually providing all of the template context variables.

```python
# settings.py

MATERIALIZE_SITE_NAME = None  # Display this name in the navbar as the main name
MATERIALIZE_TITLE = None  # This is the page title displayed as the browser tab name

MATERIALIZE_HIDE_CONTAINER = False  # If True make the page take up the full width
MATERIALIZE_SHOW_SIDENAV = True  # If True have a menu button available to open up the side navigation menu
MATERIALIZE_FIXED_SIDENAV = False  # If True and SHOW_SIDENAV make the side navigation menu always showing

MATERIALIZE_PRIMARY_COLOR = 'materialize-red lighten-2'
MATERIALIZE_SECONDARY_COLOR = 'teal'
MATERIALIZE_PRIMARY_COLOR_LIGHT = '#e51c23'
MATERIALIZE_PRIMARY_COLOR_DARK = None
MATERIALIZE_SUCCESS_COLOR = None
MATERIALIZE_ERROR_COLOR = None
MATERIALIZE_LINK_COLOR = None

```

### Styling process
There are two methods for changing the default coloring for Materialize CSS.

  * The old method is to use the templatetag `include_dynamic_css` which would use the django template system to generate 
    a style tag with the proper css classes overridden.

  * The new method only requires using the `base.html`. It includes the `materialize_nav/materialize_nav_colors.js` 
    file which uses javascript to create a style tag to edit the proper css classes. This method should require less 
    work from django to change the style.


## Goals

My original goal was to create an easier way to use materialize css with django. When I first started forms did not 
format properly and I thought navigation was a pain. Unfortunately, my original approach made this library a strong 
coupled to your django app which was a terrible design decision. I am trying to simplify this library to help style 
django apps quickly and without a lot of settings.

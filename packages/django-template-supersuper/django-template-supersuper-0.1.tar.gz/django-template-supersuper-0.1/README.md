# django-template-supersuper

Adds "super_super" method to block nodes in Django templates.

## What?

Now you can do `{{ block.super_super }}` in your templates!

## Why?

Here is a made-up scenario. Note how the child template clears the `very_kewl`
block.

`foreign_app/base.html:`

```
<!doctype HTML>

<html><head>
<!-- blah blah -->

{% block very_kewl %}
    <marquee><b><i><u>this is very kewl</marquee></b></i></u>
    <!-- disclaimer: this is not valid HTML! -->
{% endblock very_kewl %}

</html>
```


`foreign_app/actual_page.html:`

```
{% extends 'base.html' %}

{# very many other stuff, part 1 #}

{% block very_kewl %}{% endblock %}

{# very many other stuff, part 2 #}
```

Now if you want to keep that "very kewl" content on your page, you can simply 
do:

`project_template_dir/foreign_app/actual_page.html:`

```
{% extends 'foreign_app/actual_page.html' %}

{% block very_kewl %}{{ block.super_super }}{% endblock %}
```

That's it! That "very kewl" content will be rendered in the block. 
The `block.super_super` method works like `block.super` except that it skips 
one level in the template inheritance chain (or however that thing is called).



## How?

1. `pip install `.... coming soon :grin:
2. Add `'template_supersuper',` to `INSTALLED_APPS`
3. Profit!


## No, HOW?

Honestly, I don't know what I'm doing here.

The new method is monkeypatched to `BlockNode` class. It should work ok, but 
no guarantees. Also, please report any issues via GitHub issues.  

Flask-Ext
=========

Some extensions of Flask.

Subdomain
---------

- Configure ``app`` attributes

```
app.static_url_path = '/static'
app.static_folder = 'static'
app.add_url_rule(app.static_url_path + '/<path:filename>',
                 endpoint='static',
                 view_func=app.send_static_file)
```

- Configure ``settings.py``

```
SERVER_NAME = 'project_name.test:5000'
SESSION_COOKIE_DOMAIN = "." + SERVER_NAME
```

- Configure ``views.py``

```
blueprint = Blueprint('portal', __name__, subdomain='<subdomain>')
add_subdomain_support(blueprint)
```

- Configure ``RequireJS`` and ``Layer``

```
<script>
    requirejs.config({
        baseUrl: '{{ '%s%s' | format('http://', config.SERVER_NAME) }}'
    });
</script>
```

```   
<script>
    require(['layer'], function(layer){
        layer.config({
            path: "{{ '%s%s%s' | format('http://', config.SERVER_NAME, '/static/plugins/layer-3.1.1/') }}"
        });
    });
</script>
```

* Notice: You can use ``g.subdomain`` to get current subdomain.
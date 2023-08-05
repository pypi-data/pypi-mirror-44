# Django Ubigeo Perú

django-ubigeo-peru, es una app que te permitira implementar facilmente los ubigeos de la RENIEC en tus django app.

## Instalar

En tu settings.py

```python
    INSTALLED_APPS = (
        ....
        'ubigeo',
    )
```


En tu urls.py

```python
    urlpatterns = patterns('',
        ....
        (r'^ubigeo/', include('ubigeo.urls')),
    )
```

En tu forms.py
```
from django import forms
from ubigeo.fields import UbigeoField
from mymodels import Model


class IncidentForm(forms.ModelForm):

    location = UbigeoField(required=False)
    class Meta:
        model = Model
        fields = "__all__"
```
Puedes usar los parametros:
attrs_1 para atributos html para regiones
attrs_2 para atributos html para provincias
attrs_3 para atributos html para distritos
with_international para seleccionar con valores internacionales

## TODO
- Refactor Javascript functions to recieve a selector as an argument in the example aplication.

## Licencia
See LICENSE

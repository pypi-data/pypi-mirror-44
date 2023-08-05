## Filters

Filters are function that can be written by user and that modify the content of a Model, a Measure, or  spherical harmonics data.

Filter functions can be divided into three categories :

##### 1. Filters on Model

These filters take a Model object as input and return a Model object as output.

```python
from webgeodyn.filters import modelfilter
@modelfilter
def my_filter(model,other,optional,arguments):
    # model is a Model object, the filter should return a Model object.
    return modified_model
```

##### 2. Filters on Measure

These filters take a Measure object as input and return a Measure object as output.

```python
from webgeodyn.filters import measurefilter
@measurefilter
def my_filter(measure,other,optional,arguments):
    # measure is a Measure object, the filter should return a Measure object.
    return modified_measure
```

##### 1. Filters on spherical harmonics coefficient

These filters take a 2D (resp. 3D) array as an input, and return 2D (resp. 3D) array.

These filters are declared using the ```@coeffilter``` decorator.

```python
from webgeodyn.filters import coeffilter
@coeffilter
def my_filter(coefs,other,optional,arguments):
    # coefs :
    #   2D array [time,schmidtSemiNormalized spher. harm. coef]
    #   or 3D array [time,schmidtSemiNormalized spher. harm. coef]
    # other,optional,arguments :
    #   arguments that can be defined to configure the filter.
    #
    #   if coefs is 2D (resp. 3D) modified_coefs must be 2D (resp 3D.)
    return modified_coefs
```

If the filter can't handle 3D array with realisations, ```@coeffilter_norealisations``` decorator should be used.
```python
from webgeodyn.filters import coeffilter_norealisations
@coeffilter_norealisations
def my_filter(coefs,other,optional,arguments):
    # coefs :
    #   2D array only [time,schmidtSemiNormalized spher. harm. coef]
    return modified_coefs
```
This decorator will allow looping on the different realisations of the Model and calling the filter for each one.


### Calling filters

Thanks to the decorators, all the filters are called on a Model object.

```python
from webgeodyn.filters.filename import my_filter
from webgeodyn.models import Models

models = Models()
models.loadModel("/path/to/model/data/"),"Test Model","dataFormat")
my_filter(models["Test Model"])
```

**WARNING** The model object is directly modified by the filter (i.e. the data is replaced) unless you specify ```copy=True``` argument when calling the filter

#### Copying

The Model can be copied before applying filter, avoiding to rewrite the data inside the Model.

```python
newModel = my_filter(models["Test Model"],copy=True)
```

#### Applying filter to some measures only

```@measurefilter``` and ```@coeffilter``` are by default applied to all measures in the Model. But it can be applied to only given measures.

```python
my_filter(models["Test Model"],measureName=["MF","SV"])
```

This will apply the filter to measures named "MF" and "SV"

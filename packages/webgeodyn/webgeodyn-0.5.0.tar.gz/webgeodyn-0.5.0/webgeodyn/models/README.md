## Models

#### Models object

Models is a simple dictionary object, listing Model objects.

```python
models = Models()
models.loadModel("/path/to/data/","my model","dataFormat")
# Model is now loaded and accessible using:
models["my model"]
```

#### Model object

A Model object contains different measure data (e.g. magnetic field, secular variation, streamfunctions ...)

```python
model = Model("/path/to/data/","dataFormat")
# model.measures contains a dictionnary of measures
# Measures are either GHData or TSData
# It is possible to access all their properties :
#   model.measures["MF"].lmax
#   model.measures["MF"].data
#   model.measures["MF"].computeRThetaPhiData(r,thlist,phlist)
#   ...
```

All measures share the same time array that is given in

```python
model.times
```

To have information on how to construct a Model from data files, please read the [In/Out README.md file](webgeodyn/inout/README.md).

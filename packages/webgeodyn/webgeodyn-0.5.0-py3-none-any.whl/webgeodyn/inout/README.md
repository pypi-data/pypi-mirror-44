## Data Input/Output

### Files inside inout folder

This folder contains readers/writers functions for input/output of data files.

Each .py file correspond to a format. (e.g. ```zforecast.py``` implements the "zforecast" format)

A format name is to be used when load a Model.

```python
models = Models()
model = models.loadModel("/path/to/data/","modelName","dataFormat")
model = saveDataToFile("/path/to/data/",dataformat="dataFormat")
```

This command will use (if exists) the ```inout/dataformat.py``` file to read the data.

### Function template

Inside the .py files, webgeodyn is looking for ```load``` and ```save``` functions.

```load``` and ```save``` should have the following behavior :
```python
def load(dataDirectory, dataModel, keepRealisations=True):
  # 1 -
  # Load the data from dataDirectory
  #
  # 2 -
  # if keepRealisations:
  #   Make a 3D data array
  #   [time, semiNormalisedSchmidt spherical harmonics coef, realisation]
  # else:
  #   Make a 2D data array
  #   [time, semiNormalisedSchmidt spherical harmonics coefs]
  #
  # 3 -
  # add measures to the dataModel object by using the following
  dataModel.addMeasure(measureName,measureType,lmax,units,measureData,times=times)

  # measureName : Any measure name
  # measureType : "MF" or "SV" or "U"
  # lmax : (int) spherical harmonics order
  # units : (string) e.g. "nT"
  # measureData : 2D (without realisation) or 3D (with realisations) array
  # times : 1D array containing times values in year


def save(dataDirectory, dataModel, forceOverwrite=False):
  # Use dataModel to save files to dataDirectory
  # If forceOverwrite is set to True, file should be overwritten if exists
  # If forceOverwrite is set to False, an error should be raised if files exists
```

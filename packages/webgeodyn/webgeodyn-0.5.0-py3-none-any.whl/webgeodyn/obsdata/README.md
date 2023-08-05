## Observatory data

Reads observatory data from *.40 and *.10 files.

```observatory.py``` contains classes structure to manage ObservatoryGroups (CHAMP,SWARM,Magnetic observatories) and Observatory (r,theta,phi observatory with MF and SV data)
```obsdata.py``` contains class to interface with ```server.py``` and return data when needed. It also reads data from .40 and .10 files.

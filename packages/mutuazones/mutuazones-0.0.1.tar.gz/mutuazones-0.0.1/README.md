## Objetivo
Permite definir de una forma unificada el acceso a las zonas definidas en la arquitectrura de analítica avanzada de Mutua Tienerfeña.

Se han definido las siguientes zonas de trabajo.

* **lz** - Landing Zone. Son los datos que llegan desde el operacional. Pendiente de ser revisados y formatados para la silver.
* **sz** - Silver Zone. Son los datos limpios, preparados para poder cruzarse utilizarse en los correspondientes modelos.
* **gz** - Golden Zone. Son los datos asociados a los resutlados de los modelos definitivos.

## Forma de uso

En los cuadernos de python, se debe realizar lo siguiente.

Para acceder a los dataframes (pandas) almacenados en una zona<lz>:

```python
from mutuazones import lz

lz.getSavedFrames()
```

Para guardar nuevos data frames en una zona<sz> 

```python
from mutuazones import sz

df_clientes = sz.loadDataFrame('clientes')
 ...
sz.saveDataFrame('clientes_con_coche')
```
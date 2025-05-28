## Desde una terminal de anaconda

### Para exportar
<code>conda env export > tfm.yml</code>

### Para importar creando
<code>conda env create -f tfm.yml</code>
### Para importar actualizando el entorno existente
<code>conda env create -f tfm.yml --prune</code>

### Para eliminar el entorno existente previamente si no deja actualizar con --prune según la versión de conda
<code>conda env delete --name tfm</code>




# 🗃️🗃️🗃️ Iré generando un yml nuevo cuando requiera instalar nuevos paquetes.

## Versión actual:  <span style="color:red;background-color:white;">28/05/2025 19:42 horas</span>  

Motivo: Instalo skops para poder exportar el modelo de ml de skl 


## Desde una terminal de anaconda

### Para exportar
<code>conda env export > tfm.yml</code>

### Para importar creando
<code>conda env create -f tfm.yml</code>

### Para instalar con pip el requirements.txt
<code>pip install -r requirements.txt</code>

### Para importar actualizando el entorno existente
<code>conda env create -f tfm.yml --prune</code>

### Para eliminar el entorno existente previamente si no deja actualizar con --prune según la versión de conda
<code>conda env remove --name tfm</code>

### Para generar el requirements.txt con conda. 
<code>conda list -e > requirements.txt</code>

### Para generar el requirements.txt con pip (puede ser dentro de conda con en el env activado)
<code>pip freeze > requirements.txt</code>



# 🗃️🗃️🗃️ Iré generando un yml nuevo cuando requiera instalar nuevos paquetes.

## Versión actual:  <span style="color:red;background-color:white;">29/05/2025 06.51 horas</span>  

Motivo: Instalo skops para poder exportar el modelo de ml de skl y añado algunas instrucciones a las notas
29/05 añado pyodbc


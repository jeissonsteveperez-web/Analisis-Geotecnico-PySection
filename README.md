# ANÁLISIS GEOTÉCNICO DE ESTABILIDAD DE TALUDES

## Proyecto de Programación II

Aplicación desarrollada en Python para el análisis académico de una
cuña de falla planar en un talud, integrando el cálculo de propiedades
geométricas mediante PySection con un modelo simplificado de estabilidad
geotécnica.

---

# INFORMACIÓN DEL PROYECTO

**Autor:** Jeison Steven Perez

**Programa:** Ingeniería Civil

**Universidad:** Universidad Distrital Francisco José de Caldas

**Facultad:** Facultad Tecnológica

**Asignatura:** Programación II

**Ciudad:** Bogotá D.C., Colombia

**Año:** 2026

---

# 1. DESCRIPCIÓN DEL PROYECTO

El presente proyecto consiste en el desarrollo de una aplicación
computacional orientada a la ingeniería civil, específicamente al área
de geotecnia.

El programa permite realizar un análisis simplificado de una cuña de
falla planar en un talud a partir de parámetros geométricos y
geotécnicos suministrados por el usuario.

La aplicación integra el cálculo de propiedades geométricas de la
sección con un modelo de análisis de estabilidad de taludes.

Entre los principales resultados obtenidos se encuentran:

- Área de la cuña.
- Coordenada X del centroide.
- Coordenada Y del centroide.
- Longitud del plano de falla.
- Peso de la cuña.
- Componente normal del peso.
- Componente tangencial del peso.
- Resistencia por cohesión.
- Resistencia por fricción.
- Resistencia total al corte.
- Factor de seguridad.
- Condición calculada de estabilidad.

Adicionalmente, el programa genera automáticamente:

- Una representación gráfica del talud.
- La cuña de deslizamiento.
- El plano de falla.
- La ubicación del centroide.
- Los principales resultados del análisis.
- Un informe técnico en formato PDF.

---

# 2. OBJETIVO

Desarrollar una aplicación computacional en Python que permita
integrar herramientas de programación con conceptos de ingeniería
civil para realizar el análisis simplificado de una cuña de falla
planar en un talud.

El proyecto busca aplicar los conocimientos adquiridos en la
asignatura de Programación II al desarrollo de una herramienta
relacionada con la ingeniería geotécnica.

---

# 3. ¿CÓMO FUNCIONA EL PROGRAMA?

El funcionamiento general de la aplicación es:

1. El usuario ejecuta el programa.
2. El programa solicita los parámetros geométricos del talud.
3. Solicita las propiedades geotécnicas del suelo.
4. Solicita la condición de agua en la grieta.
5. Se construye matemáticamente la geometría de la cuña.
6. Se calculan sus propiedades geométricas.
7. Se determina la posición del centroide.
8. Se calculan las fuerzas principales.
9. Se determina la resistencia disponible.
10. Se calcula el factor de seguridad.
11. Se genera una representación gráfica.
12. Se genera automáticamente un informe PDF.

---

# 4. REQUISITOS DEL SISTEMA

Para ejecutar el proyecto se necesita:

- Windows 10 o superior.
- Python 3.
- Conexión a Internet durante la primera instalación de las
  dependencias.

Las librerías utilizadas por el proyecto son:

- NumPy.
- Matplotlib.
- ReportLab.

No es necesario instalarlas manualmente si se utiliza el archivo:

`ejecutar_programa.bat`

Este archivo se encarga de instalar o verificar automáticamente
las dependencias necesarias, sin embargo debe selecionar el archivo " ejecutar_programa", dar click derecho, elegir propiedades y desbloquear el archivo, posteriormente ejecutar, entorno python debe estar instalado anteriormente, finlamnete puede ejecutar el programa, sin necesidad de un entorno de desarrollo

---

# 5. INSTALACIÓN DE PYTHON

## 5.1. ¿Ya tiene Python instalado?

Si Python ya está instalado en el computador, puede pasar directamente
al capítulo 6.

## 5.2. Si Python no está instalado

Descargue Python desde su página oficial:

https://www.python.org/downloads/

Durante la instalación es MUY IMPORTANTE activar la opción:

`Add Python to PATH`

Posteriormente seleccione:

`Install Now`

Cuando finalice la instalación, cierre cualquier terminal que estuviera
abierta y vuelva a abrirla.

---

# 6. DESCARGAR EL PROYECTO

El proyecto puede descargarse directamente desde GitHub.

En la página del repositorio:

1. Seleccione el botón `Code`.
2. Seleccione `Download ZIP`.
3. Guarde el archivo.
4. Descomprima el archivo ZIP.
5. Abra la carpeta resultante.

También puede utilizar Git si conoce el funcionamiento de esta
herramienta.

---

# 7. ESTRUCTURA DEL PROYECTO

La carpeta principal contiene los siguientes archivos:

```text
pysections/
│
├── main.py
├── slope_wedge.py
├── sections.py
├── report.py
│
├── requirements.txt
├── ejecutar_programa.bat
│
├── README.md
├── LICENSE
│
├── cuna_talud.png
└── mi_seccion_cajon.jpg
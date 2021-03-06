# -*- coding: utf-8 -*-
"""P1-Regresion.ipynb


## Descripción del problema
La liga de [fútbol americano](https://es.wikipedia.org/wiki/F%C3%BAtbol_americano) NFL recopila estadísticas sobre las jugadas de todos los partidos en un portal que se conoce como [NextGenStats](https://nextgenstats.nfl.com/). Dentro de los tipos de jugadas posibles en un partido de la NFL se encuentran las jugadas de carrera en las que el Quarterback entrega el balón en la mano del corredor.

> El problema de regresión a resolver consiste en predecir cuántas yardas será capaz de recorrer el corredor antes de que termine la jugada, en base a la información que se conoce en el momento en el que el Quaterback le entrega el balón:

![Hand-off](https://media.giphy.com/media/qxmaNC1N9tRTi/giphy.gif)

### El conjunto de datos
Para esta práctica usaremos un conjunto de datos recopilado de [NextGenStats](https://nextgenstats.nfl.com/) que se encuentra en el portal [Kaggle](https://www.kaggle.com/c/nfl-big-data-bowl-2020/data). Este conjunto de datos forma parte de una competición de _Machine Learning_ alojada por dicha web y que repartirá $75.000\$$ en premios para aquellos equipos que consigan los mejores resultados.

El conjunto de datos está formado por un único fichero CSV. Cada fila del archivo corresponde a la participación de un solo jugador en una sola jugada. El conjunto de datos está desnormalizado. Todas las columnas están contenidas en un gran conjunto de datos que agrupado por el identificador de la jugada `PlayId`.

Las características (o _features_) de este conjunto de datos son las siguientes:

* `GameId` - identificador único del partido
* `PlayId` - identificador único de la jugada
* `Team` - indica si el equipo juega como local o visitante
* `X` - posición del jugador con respecto al eje largo. Ver figura a continuación.
* `Y` - posición del jugador con respecto al eje corto. Ver figura a continuación.
* `S` - velocidad en $yardas/segundo$
* `A` - aceleración en $yardas/segundo^2$
* `Dis` - yardas recorridas desde la anterior observación
* `Orientation` - orientación en grados del jugador
* `Dir` - ángulo en grados del movimiento del jugador
* `NflId` - identificador único del jugador
* `DisplayName` - nombre el jugador
* `JerseyNumber` - dorsal
* `Season` - año de la temporada
* `YardLine` - yarda de inicio de la jugada
* `Quarter` - cuarto del partido (el $5$ representa la prórroga)
* `GameClock` - tiempo de jugada
* `PossessionTeam` - equipo que tiene la posesión
* `Down` - intento (o _down_)
* `Distance` - yardas necesarias para conseguir un primer _down_
* `FieldPosition` - mitad del campo en el que transcurre la jugada
* `HomeScoreBeforePlay` - indica si el equipo local puntuó en la jugada anterior
* `VisitorScoreBeforePlay` - indica si el equipo visitante puntuó en la jugada anterior
* `NflIdRusher` - id del jugador que realiza la carrera
* `OffenseFormation` - formacion ofensiva
* `OffensePersonnel` - agrupación posicional del equipo ofensivo
* `DefendersInTheBox` - número de jugadores en primera línea de defensa
* `DefensePersonnel` - agrupación posicional del equipo ofensivo
* `PlayDirection` - dirección de la jugada
* `TimeHandoff` - tiempo UTC del momento de entrega del balón
* `TimeSnap` - tiempo UTC del inicio de la jugada
* `Yards` - **yardas ganadas en la jugada (TARGET)**
* `PlayerHeight` - altura del jugador (ft-in)
* `PlayerWeight` - peso del jugador (lbs)
* `PlayerBirthDate` - fecha de nacimiento (mm/dd/yyyy)
* `PlayerCollegeName` - universidad del jugador
* `HomeTeamAbbr` - abreviatura del nombre del equipo local
* `VisitorTeamAbbr` - abreviatura del nombre del equipo visitante
* `Week` - número de jornada
* `Stadium` - estadio
* `Location` - ciudad
* `StadiumType` - tipo de estadio
* `Turf` - tipo de césped (artificial, natural, etc.)
* `GameWeather` - descripción de las condiciones meteorológicas
* `Temperature` - temperatura (grados Farenheit)
* `Humidity` - humedad
* `WindSpeed` - velocidad del viento en $millas/hora$
* `WindDirection` - dirección del viento


![Coordenadas X e Y del Dataset](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F3258%2F7542d363a19fa3eea77708e6b90bc420%2FFig1.png?generation=1570562067917019&alt=media)

---
"""





"""## Desarrollo de la práctica

Esta práctica ha sido desarrollada por:

* Miguel Hernández Roca
* Mohammed Makhfi Boulaich

### Biblioteca
"""

# Librerías utilizadas en el desarrollo de la práctica
import pandas as pd
import numpy as np
import datetime
import sklearn
import time
import re

from dateutil import parser as dp
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import median_absolute_error

from sklearn.metrics import make_scorer
from sklearn import preprocessing
from sklearn import linear_model
from sklearn import compose


from pandas import plotting

# Configuración de pandas
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

"""### Carga del conjunto de datos
La carga del conjunto de datos se realiza mediante la URL del mismo:
"""

datos = pd.read_csv('https://drive.upm.es/index.php/s/tmMKB7kvNXWvuAm/download')

"""### Análisis exploratorio de datos"""

datos.hist(figsize = (16,18))

datos.describe()

"""#### Correlaciones

En análisis de correlaciones nos permite conocer el efecto que tiene una columna sobre otra. Nos permite, por ejemplo, eliminar columnas.
"""

# Análisis de correlación entre 'Yards' y 'Temperature'
Yards_Temperature = datos[['Yards', 'Temperature']]
sns.heatmap(pd.crosstab(Yards_Temperature.Yards, Yards_Temperature.Temperature))

# Visualizar la tabla de correlaciones
corr_data = datos.apply(lambda x: x.factorize()[0]).corr()
corr_data

# Mostrar sólo aquellas correlaciones mayores que 0.5
ind = corr_data[corr_data[corr_data.columns] > 0.5]
ind

"""#### Búsqueda de filas con errores

Algunas columnas deben tener un tipo específico de datos. Pongamos 'WindSpeed' como ejemplo. WindSpeed debe ser de tipo numérico y, sin embargo, es de tipo objeto.
"""

# Visualizar el tipo de datos que admiten las columnas
print(datos.dtypes)

# La función ''.unique()' nos permite detectar inconsistencias
datos['FieldPosition'].unique()
datos['OffenseFormation'].unique()
datos['OffensePersonnel'].unique()
datos['DefensePersonnel'].unique()
datos['PlayDirection'].unique()
datos['TimeHandoff'].unique()
datos['TimeSnap'].unique()
datos['PlayerHeight'].unique()
datos['PlayerBirthDate'].unique()
datos['PlayerCollegeName'].unique()
datos['Position'].unique()
datos['HomeTeamAbbr'].unique()
datos['VisitorTeamAbbr'].unique()
datos['Stadium'].unique()
datos['Location'].unique()
datos['StadiumType'].unique()
datos['Turf'].unique()
datos['GameWeather'].unique()
datos['WindSpeed'].unique()
datos['WindDirection'].unique()

# La función 'isna().sum()' nos permite calcular el número de entradas nulas de una columna determinada
datos['FieldPosition'].isna().sum()
datos['OffenseFormation'].isna().sum()
datos['StadiumType'].isna().sum()
datos['GameWeather'].isna().sum()
datos['WindSpeed'].isna().sum()
datos['WindDirection'].isna().sum()

# Comprobar mediante una expresión regular que el tiempo está introducido correctamente en todas las filas de la tabla
sum = 0
for elem in datos['GameClock'] :
  x = re.findall("\d\d:\d\d:\d\d", str(elem))
  if x:
    sum += 1
print(sum == len(datos['GameClock']))

"""#### Refactorización de columnas

### Transformaciones de datos
"""

# Convertir el tiempo de formato ISO 8601 a segundos
def isoFormatToSeconds(colName):
  parsed_t = []
  t_in_seconds = []
  for x in datos[colName].index:
    parsed_t.append(dp.parse(datos.loc[x, colName]))
    t_in_seconds.append(parsed_t[x].strftime('%s'))
  datos[colName] = t_in_seconds

isoFormatToSeconds('TimeHandoff')
isoFormatToSeconds('TimeSnap')

# Convertir el tiempo en formato HH:MM:SS a segundos
def timeToSeconds(colName):
  parsed_t = []
  t_in_seconds = []
  for x in datos[colName].index:
    parsed_t.append(time.strptime(datos.loc[x, colName],'%H:%M:%S'))
    t_in_seconds.append(datetime.timedelta(hours=parsed_t[x].tm_hour,minutes=parsed_t[x].tm_min,seconds=parsed_t[x].tm_sec).total_seconds())
  datos[colName] = t_in_seconds

timeToSeconds('GameClock')

# Extraer valores numéricos de la columna WindSpeed
values = []
dropIndex = []
for index, elem in enumerate(datos['WindSpeed']):
  x = re.findall("\d+", str(elem))
  if x:
    values.append(x[0])
  else:
    dropIndex.append(index)
datos = datos.drop(datos.index[dropIndex])
datos['WindSpeed'] = values

# Unificar la terminología utilizada en WindDirection
values = []
dropIndex = []
for index, elem in enumerate(datos['WindDirection']):
  elem = str(elem)
  elem = elem.upper()
  SE = re.findall("SE+|SO.*EA.*", elem)
  SW = re.findall("SW+|SO.*WE.*", elem)
  NE = re.findall("NE+|NO.*EA.*", elem)
  NW = re.findall("NW+|NO.*WE.*", elem)
  N = re.findall("^N{1}$|^NORTH$", elem)
  E = re.findall("^E{1}$|^EAST$", elem)
  S = re.findall("^S{1}$|^SOUTH$", elem)
  W = re.findall("^W{1}$|^WEST$", elem)
  if SE:
    values.append('SE')
  elif SW:
    values.append('SW')
  elif NE:
    values.append('NE')
  elif NW:
    values.append('NW')
  elif N:
    values.append('N')
  elif E:
    values.append('E')
  elif S:
    values.append('S')
  elif W:
    values.append('W')
  else:
    dropIndex.append(index)
datos = datos.drop(datos.index[dropIndex])
datos['WindDirection'] = values

# Obtener la edad del jugador a partir de su fecha de nacimiento y cambiar nombre de columna
datos["PlayerBirthDate"]= datos["PlayerBirthDate"].astype('datetime64[Y]')
thisyear= datetime.datetime.now().year
datos['PlayerBirthDate'] = thisyear - datos["PlayerBirthDate"].dt.year
datos.rename(columns={'PlayerBirthDate':'PlayerAge'})

# La altura del jugador es un valor de tipo numérico
datos["PlayerHeight"]= datos["PlayerHeight"].astype('str')
datos['PlayerHeight']= datos['PlayerHeight'].str.replace("-",".")
datos["PlayerHeight"]= datos["PlayerHeight"].astype('float')

# La velocidad del viento es un valor de tipo numérico
datos["WindSpeed"]= datos["WindSpeed"].astype('float')

"""Son 3 las transformaciones que aplicaremos:


1.   Las columnas cuyo histograma no se asemeja a una normal, utilizaremos el **MinMaxScaler**.
2.   Las que sí se asemejan a una normal las transformamos a una **normal** (0,1).
3.   Las columnas cuyos valores son categóricos utilizaremos el **OneHotEncoding**.

Es importante mencionar que, del conjunto de datos original, se eliminarán un número significativo de *filas* por razones como:

*   **FieldPosition**: las filas con valores nulos serán eliminadas porque no hay una manera adecuada de rellenarlas.

No solo filas. Algunas *columnas* también serán eliminadas:

* **DisplayName**: Si el modelo da demasiado peso al nombre de un jugador, al entrenarlo ocurrirá overfitting.
* **GameWeather**: La columna presenta unos niveles de inconsistencia importantes.
"""

# Procedemos a eliminar toda fila que contiene al menos un valor nulo
datos = datos.dropna()

column_transformer = sklearn.compose.ColumnTransformer(transformers=[
    ("drop", "drop", [10,11,23,44,31]),
    ("scale", sklearn.preprocessing.StandardScaler(),[3,4,5,7,14,16,21,22,26,29,30,32,33,34,45,46,47]),
    ("min-max", sklearn.preprocessing.MinMaxScaler(),[0,1,6,8,9,12,18,19,39]),
    ("one-hot", sklearn.preprocessing.OneHotEncoder(), [2,13,15,17,20,24,25,27,28,35,36,37,38,40,41,42,43,48])
]);

datosT = column_transformer.fit_transform(datos)
datosT.shape

# Almacenamos la columna que queremos predecir en una variable
yards = datos["Yards"]

"""### Procesamiento de datos"""

linear_regression = linear_model.LinearRegression()
linear_regression.fit(datosT, yards)

datos.shape

linear_regression.coef_

y_hat = linear_regression.predict(datosT)

mean_squared_error(yards, y_hat)

x_train, x_test, y_train, y_test = train_test_split(datosT, yards, test_size=0.2, random_state=0)

linear_regression = linear_model.LinearRegression()
linear_regression.fit(x_train, y_train)

y_hat = linear_regression.predict(x_test)
mean_squared_error(y_test, y_hat)

for x in range(1,10) :
  ridge_regression = linear_model.Ridge(alpha=x/100)
  ridge_regression.fit(x_train, y_train)
  y_hat = ridge_regression.predict(x_test)
  print(median_absolute_error(y_test, y_hat))
  print("alpha value is x",x)

#cross validation
linear_regression = linear_model.LinearRegression()
scorer = make_scorer(score_func=mean_squared_error, greater_is_better=False)
scores = cross_val_score(linear_regression, datosT, yards, cv=5, scoring='neg_median_absolute_error')
scores
scores.mean()

#cross validation

ridge_regression = linear_model.Ridge(alpha=0.1)
scores = cross_val_score(ridge_regression, datosT, yards, cv=5, scoring='neg_median_absolute_error')
scores
print(scores.mean())

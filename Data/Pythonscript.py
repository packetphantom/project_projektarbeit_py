#!/usr/bin/env python
# coding: utf-8

# # 911 Anrufe Projekt - Aufgabe
# 
# Für dieses Meilensteinprojekt analysieren wir daren von Anrufen die bei der
# amerikanischen Polizei (am. Rufnummer: 911) eingehen. 
# Dieser Datensatz wird bei [Kaggle](https://www.kaggle.com/mchirico/montcoalert) 
# bereitgestellt. Er beinhaltet die folgenden Felder:
# 
# * lat: String Variable, Breitengrad
# * lng: String Variable, Längengrad
# * desc: String Variable, Beschreibung des Notrufs
# * zip: String Variable, Postleitzahl
# * title: String Variable, Titel
# * timeStamp: String Variable, Zeit: YYYY-MM-DD HH:MM:SS
# * twp: String Variable, Gemeinde
# * addr: String Variable, Addresse
# * e: String Variable, Dummy Variable (immer 1)
# # 
# ## Daten und Vorbereitungen

# %% Imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %% Lese das "911.csv" als DataFrame mit Namen df ein.**

df = pd.read_csv("Daten_Quelle.csv")

# %% Schaue dir die Infos zum DataFrame an.**

df.info()

# %% Schaue dir den Tabellenkopf an.**

df.head()

# %% Was sind die Top 5 Postleitzahlen (en. zipcodes) mit Notrufen?**

df["zip"].value_counts().head(5)


# %% Was sind die Top 5 Gemeinden (en. township (twp)) mit Notrufen?**

df["twp"].value_counts().head(5)


# %% Schaue dir die "title" Spalte an; wie viele einzigartige Einträge gibt es?**

df["title"].nunique()

# %% Neue Features hinzufügen
# 
# **In der Titelspalte, sind "Gründe/Zuständigkeiten" vor dem Titelcode spezifiziert. 
# Diese lauten "EMS", "Fire" und "Traffic". Nutze `.apply()` 
# mit einer selbsterstellten lambda Funktion, um eine neue Spalte namens "Reason" 
# (dt. Grund) zu erstellen, die diesen String enthält. **
# 
# Zum Beispiel, wenn der Titel "EMS: BACK PAINS/INJURY" lautet, dann soll in 
# der Spalte für den Grund "EMS" stehen.

# string_lst = 'EMS: BACK PAINS/INJURY'
# liste = string_lst.split(':')[0]
# print(liste)

df['Reason'] = df['title'].apply(lambda title: title.split(':')[0])
df.head()


# %% Was ist der häufigste Grund für Notrufe (basiert auf der neuen Spalte)?**

df['Reason'].value_counts().head()


# %%Nutze jetzt Seaborn um ein `countplot` der Gründe für Notrufe zu erstellen.**

sns.countplot(x='Reason', hue='Reason', data=df) #palette="viridis", legend=False)
plt.show()


# %% Jetzt werden wir uns mehr auf die Zeitinformationen konzentrieren. 
# Welchen Datentyp haben die Objekte in der *timestamp* Spalte?**

type(df['timeStamp'].iloc[0])
# print(type('timeStamp'))

# %% Das Ergebnis der vorherigen Aufgabe sollte zeigen, dass diese 
# Zeitinformation noch als String vorliegt. Nutze `pd.to_datetime`
# ([Dokumentation]
# (http://pandas.pydata.org/pandas-docs/stable/generated/pandas.to_datetime.html)), 
# um diese Spalte vom String zum DateTime Datentyp zu ändern.

df['timeStamp'] = pd.to_datetime(df['timeStamp'])
type(df['timeStamp'].iloc[0])


# %% Jetzt können wir spezifische Attribute des DateTime-Objekts abrufen, 
# indem wir sie aufrufen. Zum Beispiel:**
# 
#     time = df['timeStamp'].iloc[0]
#     time.hour
#     
# Durch Jupyters *Tab-Funktion* lassen sich alle Attribute erkunden, 
# die wir auf "time" anwenden könnten.
# 
# %% Unsere Zeitinformationen liegen jetzt als DateTime Objekt vor. 
# Nutze .apply() um 3 neue Spalten mit Namen "Hour" (dt. Stunde), "Month" 
# (dt. Monat) und "Day of Week" (dt. Wochentag). Dazu bietet sich am besten die 
# "timeStamp" Spalte an. Falls Schwierigkeiten beim Coden auftreten kannst du 
# auf die Lösung zurückgreifen.**

df['Hour'] = df['timeStamp'].apply(lambda time: time.hour)
df['Minute'] = df['timeStamp'].apply(lambda time: time.minute)
df['Month'] = df['timeStamp'].apply(lambda time: time.month)
df['Day of Week'] = df['timeStamp'].apply(lambda time: time.dayofweek)
# df.drop('Day of Week', axis=1, inplace=True) lösche Spalte
df.head()

# %% Achte darauf, dass der "Day of Week" eine Zahl von 0 bis 6 ist. 
# Nutze die `.map()` Methode mit folgendem Dictionary, um daraus Strings zu machen:
    
dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
df['Day of Week'] = df['Day of Week'].map(dmap)
df.head()

# %% Jetzt nutze Searborn, um ein `countplot` zu erstellen. Es soll für jeden 
# Wochentag farblich unterscheiden, was der Grund für den Notruf war.**

sns.countplot(x="Day of Week", data=df, hue='Reason',palette='viridis')
# Um die Legende neu anzuordnen
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()

# %% *Tue jetzt das gleiche für jeden Monat.**

color_p = sns.set_palette(sns.color_palette("Paired"))
sns.countplot(x='Month', hue='Reason', data=df, palette='dark')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()

 
# %% Erstelle jetzt ein groupby-Objekt namens "byMonth", indem du den DataFrame 
# nach der Monatsspalte und nutze die `count()` Methode zur Aggregation. 
# Anschließend nutze die `head()` Methode auf den zurückgegebenen DataFrame.

byMonth = df.groupby('Month').count()
byMonth.head(12)

# %% Erstelle eine einfaches Diagramm des DataFrames der den Anzahl (en. count) 
# von Anrufen pro Monat zeigt.

byMonth['twp'].plot()
plt.show()

# %% Jetzt versuche Seaborn's `lmplot()`, um eine lineare Annäherung auf die 
# Anrufe pro Monat zu legen.
# *Hinweis: Denke daran, dass der Index möglicherweise zu einer Spalte 
# gesetzt werden muss.

sns.lmplot(x='Month', y='twp', data = byMonth.reset_index())
plt.show()


# %% Erstelle eine neue Spalte namens "Date" (dt. Datum), die das Datum aus 
# der timeStamp Spalte beinhaltet. Dazu wirst du die `.date()` Methode nutzen müssen.

df.drop('Date', axis=1, inplace=True) # lösche Spalte
df.head()

# %%

df['Date'] = df['timeStamp'].apply(lambda t: t.date)
df.head()


# %% Gruppiere jetzt über diese Date Spalte und aggregiere mit `count()`. 
# Erstelle dann ein Diagramm der Anzahl an Notrufen.

df.groupby('Date').count()['twp'].plot()
plt.tight_layout()

# %% Erstelle dieses Diagramm nun erneut, aber trenne insgesamt drei Diagramme 
# für jeden Grund von Notruf.

df[df['Reason']=='Traffic'].groupby('Date').count()['twp'].plot()
plt.title('Traffic')
plt.tight_layout()


# %%

df[df['Reason']=='Fire'].groupby('Date').count()['twp'].plot()
plt.title('Fire')
plt.tight_layout()

# %%

df[df['Reason']=='EMS'].groupby('Date').count()['twp'].plot()
plt.title('EMS')
plt.tight_layout()


# %% Jetzt können wir mit Heatmaps und Seaborn weitermachen. 
# Dazu müssen wir unseren DataFrame etwas restrukturieren, sodass die Stunden 
# zu den Spalten werden und der "Day of Week" der Index. 
# Es gibt dazu viele Möglichkeiten. Ich empfehle eine Kombination aus `groupby` 
# und der `unstack` 
# ([zur Dokumentation]
# (http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.unstack.html))

dayHour = df.groupby(by=['Day of Week','Hour']).count()['Reason'].unstack()
dayHour.head()


# %% Erstelle jetzt eine HeatMap unter Verwendung des neuen DataFrames.

plt.figure(figsize=(12,6))
sns.heatmap(dayHour,cmap='viridis')
plt.show()

# %% Erstelle jetzt eine Clustermap unter Verwendung des neuen DataFrames.
sns.clustermap(dayHour,cmap='viridis')
plt.show()

# %% Wiederhole diesen Vorgang nun unter Verwendung des Monats als Spaltenunterteilung.

dayMonth = df.groupby(by=['Day of Week','Month']).count()['Reason'].unstack()
dayMonth.head()


# %% Heatmap

plt.figure(figsize=(12,6))
sns.heatmap(dayMonth,cmap='viridis')
plt.show()

# %% Clustermap

sns.clustermap(dayMonth,cmap='viridis')
plt.show()
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as shc

year = 2019
url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, features="html.parser")
soup.findAll('tr', limit=2)
headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
headers = headers[1:]
headers
rows = soup.findAll('tr')[1:]
player_stats = [[td.getText() for td in rows[i].findAll('td')]
            for i in range(len(rows))]

forbidden =[0,1,3]
for x in player_stats:
    i=0
    while i<len(x):
        if i in forbidden or x[i] == '':
            pass
        else:
            x[i] = float(x[i])
        i+=1

stats = pd.DataFrame(player_stats, columns = headers)
stats.head(10)

data = stats.drop(columns="Pos")
data = data.drop(columns="Tm")
nan_value = float("NaN")
data.replace("", nan_value, inplace=True)
data.dropna(subset = ["2P%"], inplace=True)
data.dropna(subset = ["FT%"], inplace=True)
data.dropna(subset = ["3P%"], inplace=True)
data.dropna(subset = ["FG%"], inplace=True)
data.dropna(subset = ["eFG%"], inplace=True)
data = data.dropna()
data = data[data['G'] > 50]
data = data[data['PTS'] > 10]
data = data[data['MP'] > 10]

ds = data.drop(columns ="Player")
ds = ds.drop(columns ='G')
ds = ds.drop(columns = 'GS')

namesarray = data['Player'].to_numpy()

plt.figure(figsize=(10, 7), dpi = 300)
plt.title("Redefining positions")
dend = shc.dendrogram(shc.linkage(ds, method='ward'), labels=namesarray)
plt.show()

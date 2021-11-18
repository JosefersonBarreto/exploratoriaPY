

################################## script ######################################
################ Análise Exploratória em Python ################################



#Realizar uma análise exploratória affim de responder algumas questões , para estem fim usaremos os dados  públicos disponíveis no  IMDB sobre as avaliações dos filmes . 


#1- Quais São as Categorias de Filmes Mais Comuns no IMDB?

#2- Qual o Número de Títulos Por Gênero?

#3- Qual o Número de Filmes Produzidos Por País?



#4- Quais São os Top 10 Melhores Filmes?


#5- Quais São os Top 10 Piores Filmes?


# Escolhendo o diretório  e chamando a liguagem python

#Para podermos utilizar a liguagem pyhon  no Rmarkdown vamos chamar o pacote "**reticulate**"



knitr::opts_chunk$set(echo = TRUE, warning=FALSE)

library(reticulate)
#py_install("IPython")





# Carregando pacotes 
#carregar os pacotes python necessários  


# Imports


import re
import time
import sqlite3
import pycountry
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
from IPython.display import display
from sklearn.feature_extraction.text import CountVectorizer
import warnings
warnings.filterwarnings("ignore")
sns.set_theme(style = "whitegrid")


# fazendo  download do banco de dados  publico do  IMDB

#As seguintes linhas de comando abaixo  faz o download do banco de dados do IMDB  , para  utilizar remova as "#" 
# depois de baixado,coloque a  "#" novamente.
 #É possível utilizar os comandos abaixo  pelo o próprio CMD,caso queira .


#!imdb-sqlite


   
# Conectando  o banco dedos SQlite

#Para conectar ao artquivo "db"  vamos utilizar o comando "**sqlite3.connect()**"da do pacote  **sqlite3** , além disso , para podermos utilizar o arquivo SQl temos que indicar o caminho onde o arquivo "db" está localizado 
          

# Conecta no banco de dados
conn = sqlite3.connect("C:/Users/josef/Documents/PythonFundamentos-master/Cap06/Notebooks/imdb.db")





#  Gerando o data frame 

# O comando "**pd.read_sql_query**" do pacote "pandas"  gera o nosso  data frame
# onde os argumentos  "SElECT  AS " ,"FROM"   ,"WHERE"   são argumentos da linguagem  SQL para seleção e "conn"  é a variavél criada anteriomente     que está conectada ao  servidor Sql .  

import pandas as pd
import sqlite3







# Extrai a lista de tabelas
tabelas = pd.read_sql_query("SELECT NAME AS 'Table_Name' FROM sqlite_master WHERE type = 'table'", conn)




# visualiza o  tipo  do objeto 
 visualiza o tipo de objeto que nosso caso é um DataFrame 

# Tipo do objeto
#type(tabelas)





   


## Visualiza o resultado


# Visualiza o resultado
tabelas.head()



## Covertendo  o nosso DataFrame em lista 

#O comando "**values.tolist()**"  é responsável pela conversão  de DataFrame para lista.


# Vamos converter o dataframe em uma lista
tabelas = tabelas["Table_Name"].values.tolist()



# criando um loop 

# O loop vai funcionar da seguinte forma , para cada tabela na lista de tabelas ,vamos buscar os detalhes da tabela,logo,fazemos  uma "consulta" ,na sequência buscaremos os "resultados" ,  o próximo passo  imprime(print) 
#o nome da  tabela e o resultado **display(resultado)**  além disso , imprimimos uma quebra de linha  para que sejá visivél todas as tabelas .
 



# Vamos percorrer a lista de tabelas no banco de dados e extrair o esquema de cada uma


for tabela in tabelas:
    consulta = "PRAGMA TABLE_INFO({})".format(tabela)
    resultado = pd.read_sql_query(consulta, conn)
    print("Esquema da tabela:", tabela)
    display(resultado)
    print("-"*100)
    print("\n")
 
   







  
    
  
    
    

## 1- Quais São as Categorias de Filmes Mais Comuns no IMDB?


#Primeiramente vamos realizar uma consulta a nossa fonte de dados  , para isso vamos utilizar uma instrução Sql 
#**SELECT type** onde "type" é a categoria ,"COUNT(*)"  numero de registros ,   **FROM titles** ,ou seja, para a tabela "titles"  agrupando por tipo **GROUP BY type**.

# Cria a consulta SQL
consulta1 = '''SELECT type, COUNT(*) AS COUNT FROM titles GROUP BY type''' 




# Extraindo os resultados 

#vamos retornar o conjunto de resultados da string de consulta  pelo comando **pd.read_sql_query()**,nesse caso, 
#vamos executar a consulta(consulta1)   da nossa conexão(conn).


# Extrai o resultado
resultado1 = pd.read_sql_query(consulta1, conn)




# Visualizando os resultados 
# para   visualizar os resultados vamos utilizar o comando display() , caso dê erro , execute a seguinte linha de comandos no carregamento de pacotes python **from IPython.display import display**.


# Visualiza o resultado
display(resultado1)


   
#    calculando o percentual para cada tipo 

 #resultado1 irá receber uma nova variável(percentual)  que nada mais é que cada total de registros dividido pela soma 
 #de registros multiplicado por 100 


# Vamos calcular o percentual para cada tipo
resultado1['percentual'] = (resultado1['COUNT'] / resultado1['COUNT'].sum()) * 100


Exibindo o resultado  

# Visualiza o resultado
display(resultado1)




# Vamos criar um gráfico com apenas 4 categorias:  
# Vamos criar um gráfico   com 4 categorias , sendo 3 delas referente  as categorias com mais títulos  e  1 categoria com todo o restante (others). Antes vamos criar um dicionario vazio onde irá fica armazenado os valores das categorias restantes , depois vamos  filtrar o percentual do (resultado1) que foram menor do que 5% 
#depois vamos gravar o resultado em **others["percentual"]**.


# Vamos criar um gráfico com apenas 4 categorias:
# As 3 categorias com mais títulos e 1 categoria com todo o restante

# Cria um dicionário vazio
others = {}

# Filtra o percentual em 5% e soma o total
others['COUNT'] = resultado1[resultado1['percentual'] < 5]['COUNT'].sum()

# Grava o percentual
others['percentual'] = resultado1[resultado1['percentual'] < 5]['percentual'].sum()

# Ajusta o nome
others['type'] = 'others'




## visualisando 

# Visualiza
others





## Próximo passo 

#Vamos filtrar os resuldos maiores que 5%, em seguida vamos adicionar "others" ao 
#**resultado1**  e por último vamos ordenar (resultado1)  por  "**COUNT**"




# Filtra o dataframe de resultado
resultado1 = resultado1[resultado1['percentual'] > 5]

# Append com o dataframe de outras categorias
resultado1 = resultado1.append(others, ignore_index = True)


# Ordena o resultado
resultado1 = resultado1.sort_values(by = 'COUNT', ascending = False)

#renomeando 
resultado1 = resultado1.rename(columns={'type': 'tipo','COUNT':'contagem'})




# Visualiza
resultado1.head()





 #Logo , a categoria mais comum no IMDB é **tvEpisode**  com 73% , na segunda posição aparece   a categria   **short**

#com 10%.



## Ajustandos os labels 

#Para ajustar os Labels vamos utilizar list comprehension
#onde que para cada índice  do DataFrame do **resultado1** retorno  a categoria(**tipo**)
#e o **percentual**  .

    

# Ajusta os labels
labels = [str(resultado1['tipo'][i])+' '+'['+str(round(resultado1['percentual'][i],2)) +'%'+']' for i in resultado1.index]



## Executando o gráfico de  rosca 

 #Para o mapeamento das cores   vamos utilizar o "set3", depois criamos a figura , em seuida  criamos o gráfico
# atráves  do comando **plt.pie()**
 
 
 #pequena descrição sobre alguns argumentos :
 
# figsize= determina o tamanho da figura 
 
 
 #radius=   raio  dá circunferência 
 
 
 

 
 
 

# Plot

# Mapa de cores
# https://matplotlib.org/stable/tutorials/colors/colormaps.html
cs = cm.Set3(np.arange(100))

# Cria a figura
f = plt.figure(figsize = (8,8))
#f.set_size_inches(4,4)
#f.set_size_inches(6, 6, forward=True) 
# Pie Plot

plt.pie(resultado1['contagem'], labeldistance = 0.5, radius = 1.2, colors = cs, wedgeprops = dict(width = 0.4))
plt.legend(labels = labels, loc = 'center', prop = {'size':14})
plt.title("Distribuição de Títulos", loc = 'center', fontdict ={'fontsize':16,'fontweight':10})

plt.show()

    

    


## 2- Qual o Número de Títulos Por Gênero?



# Cria a consulta SQL
consulta2 = '''SELECT genres, COUNT(*) FROM titles WHERE type = 'movie' GROUP BY genres''' 


# Resultado
resultado2 = pd.read_sql_query(consulta2, conn)
# Visualiza o resultado
display(resultado2)




# Visualiza o resultado
display(resultado2)











# Converte as strings para minúsculo
resultado2['genres'] = resultado2['genres'].str.lower().values


# remove os valores 


# Remove valores NA (ausentes)
temp = resultado2['genres'].dropna()



# Vamos criar um vetor usando expressão regular para filtrar as strings

# https://docs.python.org/3.8/library/re.html
padrao = '(?u)\\b[\\w-]+\\b'

# https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
vetor = CountVectorizer(token_pattern = padrao, analyzer = 'word').fit(temp)


#type(vetor)





   

# criando a matriz


# Aplica a vetorização ao dataset sem valores NA
bag_generos = vetor.transform(temp)




type(bag_generos)









# Retorna gêneros únicos
generos_unicos =  vetor.get_feature_names()


## Criando  um DataFrame 
Através dos comando **pd.DataFrame()** vamos criar um  data frame 


# Cria o dataframe de gêneros
generos = pd.DataFrame(bag_generos.todense(), columns = generos_unicos, index = temp.index)




# Visualiza
generos.info()







## Removendo a coluna "n"


# Drop da coluna n
generos = generos.drop(columns = 'n', axis = 0)


## calculando o percentual 
 
# Calcula o percentual
generos_percentual = 100 * pd.Series(generos.sum()).sort_values(ascending = False) / generos.shape[0]

generos_percentual.head(10)







## Plotando o gráfico






# Plot
plt.figure(figsize = (16,10))
sns.barplot(x = generos_percentual.values, y = generos_percentual.index, orient = "h", palette = "terrain")
plt.ylabel('Gênero')             
plt.xlabel("\nPercentual de Filmes (%)")
plt.title('\nNúmero (Percentual) de Títulos Por Gênero\n')
plt.show()




 


  





    





    

    


## 3- Qual o Número de Filmes Produzidos Por País?
A região onde cada fime foi produzido está na tabela akas,logo ,vamos fazer uma consulta  ao nosso banco de dados usando os conceitos vistos na questão 1  e 2 :


vamos contar  numero de flmes ,buscando os dados na tabela "akas" junto com a tabela"titles"  
 **as.title_id = titles.title_id** é a junção das tabelas 


# Consulta SQL
consulta3 = '''
            SELECT region, COUNT(*) Number_of_movies FROM 
            akas JOIN titles ON 
            akas.title_id = titles.title_id
            WHERE region != 'None'
            AND type = \'movie\'
            GROUP BY region
            ''' 



## dataframe 

montando o nosso DataFrame como nas questões anteriores 


# Resultado
resultado3 = pd.read_sql_query(consulta3, conn)

display(resultado3)






      

  
  
  








   








   



## criando duas listas auxiliares


# Listas auxiliares
nomes_paises = []
contagem = []



## criando um loop


# Loop para obter o país de acordo com a região
for i in range(resultado3.shape[0]):
    try:
        coun = resultado3['region'].values[i]
        nomes_paises.append(pycountry.countries.get(alpha_2 = coun).name)
        contagem.append(resultado3['Number_of_movies'].values[i])
    except: 
        continue






##  Preparando o DataFrame 

# Prepara o dataframe
df_filmes_paises = pd.DataFrame()
df_filmes_paises['country'] = nomes_paises
df_filmes_paises['Movie_Count'] = contagem






# Ordenando os resultados 
o argumento **ascending** ordena os resultados , caso use "**true**" ele vai do menor para o maior , logo temos que usar "**false**"


# Ordena o resultado
df_filmes_paises = df_filmes_paises.sort_values(by = 'Movie_Count', ascending = False)

# Visualizando
df_filmes_paises.head(10)







## Plotando o gráfico 


    
  
    


# Plot

# Figura
plt.figure(figsize = (20,12))

# Barplot
sns.barplot(y = df_filmes_paises[:20].country, x = df_filmes_paises[:20].Movie_Count, orient = "h")

# Loop
for i in range(0,20):
    plt.text(df_filmes_paises.Movie_Count[df_filmes_paises.index[i]]-1,
             i + 0.30,
             round(df_filmes_paises["Movie_Count"][df_filmes_paises.index[i]],2))

plt.ylabel('País')             
plt.xlabel('\nNúmero de Filmes')
plt.title('\nNúmero de Filmes Produzidos Por País\n')
plt.show()



    


## 4- Quais São os Top 10 Melhores Filmes?



# Consulta SQL
consulta4 = '''
            SELECT primary_title AS Movie_Name,genres, rating
            FROM 
            titles JOIN ratings
            ON  titles.title_id = ratings.title_id
            WHERE titles.type = 'movie' AND ratings.votes >= 25000
            ORDER BY rating DESC
            LIMIT 10          
            ''' 




# Resultado
top10_melhores_filmes = pd.read_sql_query(consulta4, conn)

#visualizando
display(top10_melhores_filmes)












plt.figure(figsize = (20,10))

sns.barplot(top10_melhores_filmes['rating'],top10_melhores_filmes['Movie_Name'], palette = "terrain",orient = "h")

plt.title('\n top 10 melhores filmes \n')
plt.xlabel('notas')
#
plt.show()

  
  

## 5- Quais São os Top 10 Piores Filmes?





# Consulta SQL
consulta5 = '''
            SELECT primary_title AS Movie_Name, genres, rating
            FROM 
            titles JOIN ratings
            ON  titles.title_id = ratings.title_id
            WHERE titles.type = 'movie' AND ratings.votes >= 25000
            ORDER BY rating ASC
            LIMIT 10
            ''' 




# Resultado
top10_piores_filmes = pd.read_sql_query(consulta5, conn)





display(top10_piores_filmes)














plt.figure(figsize = (20,10))

sns.barplot(top10_piores_filmes['rating'],top10_piores_filmes['Movie_Name'], palette = "terrain",orient = "h")

plt.title('\n top 10 piores filmes \n')
plt.xlabel('notas')
#
plt.show()





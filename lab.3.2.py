import matplotlib.pyplot as plt
from statsmodels.datasets import copper
from matplotlib.patches import Patch


df_c = copper.load_pandas().data


df_c['TIME'] = df_c['TIME'].apply(lambda x: x + 1950)
df_c = df_c.loc[10:20]  

legend_elements_1 = [
    Patch(facecolor='blue', edgecolor='black', label = 'Мировое потребление металов'),  
]

legend_elements_2 = [
    Patch(facecolor='blue', edgecolor='orange', label = 'Медь'),  
    Patch(facecolor='orange', edgecolor='black', label = 'Алюминий')
]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))


ax1.plot(df_c['TIME'], df_c['WORLDCONSUMPTION'], color='blue')
ax1.set_title('Задание 2: Динамика 1961–1970')
ax1.set_xlabel('Год')
ax1.set_ylabel('в 1000 метрических тоннах')
ax1.legend(handles=legend_elements_1)
ax1.grid(True, alpha=0.3)


ax2.plot(df_c['TIME'], df_c['COPPERPRICE'], label='Медь', color='blue')
ax2.plot(df_c['TIME'], df_c['ALUMPRICE'], label='Алюминий', color='orange')

ax2.set_title('Задание 2: Динамика 1961–1970')
ax2.set_xlabel('Год')
ax2.set_ylabel('цена cпоправкой на $')
ax2.legend(handles=legend_elements_2)
ax2.grid(True, alpha=0.3)


plt.tight_layout()
plt.show()
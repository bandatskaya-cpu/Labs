import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from sklearn.datasets import load_diabetes
import pandas as pd


diabetes = load_diabetes(scaled=False)
df = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)
df['target'] = diabetes.target

x = df['age']
y = df['bmi']
target = df['target']


colors = []
for t in target:
    if t < 100:
        colors.append('blue')      
    elif t <= 200:
        colors.append('green')     
    else:
        colors.append('red')      

plt.figure(figsize=(10, 6))
plt.scatter(x, y, c=colors, alpha=0.7, edgecolors='black', s=50)
plt.xlabel('Age', fontsize=12)
plt.ylabel('BMI', fontsize=12)
plt.title('Scatter Plot: Age vs BMI (Diabetes Dataset)', fontsize=14)

legend_elements = [
    Patch(facecolor='blue', edgecolor='black', label='target < 100'),
    Patch(facecolor='green', edgecolor='black', label='100 ≤ target ≤ 200'),
    Patch(facecolor='red', edgecolor='black', label='target > 200')
]
plt.legend(handles=legend_elements)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
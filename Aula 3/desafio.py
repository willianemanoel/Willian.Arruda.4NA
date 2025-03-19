# Importando as bibliotecas necessárias
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score, roc_curve, auc
import matplotlib.pyplot as plt
import numpy as np

# Carregar o conjunto de dados Wine
data = load_wine()
X = data.data  # Características (features)
y = data.target  # Rótulos (labels)

# Dividir os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Normalizar os dados
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Usando o KNN com k=5
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

# Previsões com os dados de teste
y_pred = knn.predict(X_test)

# Avaliar o modelo
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

# Mostrar as métricas
print("Acurácia:", accuracy)
print("Matriz de Confusão:")
print(conf_matrix)
print("Precisão:", precision)
print("Recall:", recall)
print("F1-Score:", f1)

# Curva ROC (para problemas multiclasse)
# Usando a abordagem "one vs rest" para cálculo da curva ROC

# Inicializando as variáveis para a curva ROC
fpr = {}
tpr = {}
roc_auc = {}

# Calculando a curva ROC para cada classe (usando a abordagem "one vs rest")
n_classes = len(np.unique(y))  # Número de classes
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_test == i, knn.predict_proba(X_test)[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

# Plotando a Curva ROC
plt.figure(figsize=(10, 6))
colors = ['darkorange', 'blue', 'green']  # Adicionando cores para cada classe

for i in range(n_classes):
    plt.plot(fpr[i], tpr[i], color=colors[i], lw=2, label='Classe {0} (AUC = {1:0.2f})'.format(i, roc_auc[i]))

plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Taxa de Falsos Positivos')
plt.ylabel('Taxa de Verdadeiros Positivos')
plt.title('Curva ROC - KNN')
plt.legend(loc='lower right')
plt.show()

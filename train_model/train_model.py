import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder
from sklearn.naive_bayes import CategoricalNB
from sklearn.metrics import accuracy_score
import joblib  # para salvar o modelo e encoder

# Carregar dados
carros = pd.read_csv("./train_model/car.csv", sep=",")

# Converter colunas em categóricas
for col in carros.columns.drop('class'):
    carros[col] = carros[col].astype('category')

# Codificar features
encoder = OrdinalEncoder()
X_encoded = encoder.fit_transform(carros.drop('class', axis=1))

# Codificar target
y = carros['class'].astype('category').cat.codes

# Dividir treino/teste
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.3, random_state=42
)

# Treinar modelo
modelo = CategoricalNB()
modelo.fit(X_train, y_train)

# Avaliar acurácia
y_pred = modelo.predict(X_test)
acuracia = accuracy_score(y_test, y_pred)
print(f"Acurácia no teste: {acuracia:.2f}")

# Salvar modelo e encoder
joblib.dump(modelo, "./app/modelo_nb.joblib")
joblib.dump(encoder, "./app/encoder.joblib")
joblib.dump(carros['class'].astype(
    'category').cat.categories, "./app/class_categories.joblib")

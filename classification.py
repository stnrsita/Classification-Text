import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler

# Fungsi untuk membaca data dari CSV dan memisahkan fitur dan label
def load_data(file_path):
    df = pd.read_csv(file_path, header=None)
    X = df.iloc[:, :-1].values
    y = df.iloc[:, -1].values
    return X, y

# Baca data dari CSV
X_train, y_train = load_data("training_features.csv")
X_test, y_test = load_data("testing_features.csv")

# Normalisasi data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Hyperparameter tuning untuk SVM
svm_params = {
    'C': [0.1, 1, 10, 100],
    'gamma': [1, 0.1, 0.01, 0.001],
    'kernel': ['rbf', 'linear']
}
svm_grid = GridSearchCV(SVC(), svm_params, refit=True, verbose=2, cv=5)
svm_grid.fit(X_train, y_train)
print("Best SVM Parameters:", svm_grid.best_params_)
svm_best = svm_grid.best_estimator_
y_pred_svm = svm_best.predict(X_test)
print("SVM Classification Report:")
print(classification_report(y_test, y_pred_svm))
print("SVM Accuracy:", accuracy_score(y_test, y_pred_svm))

# Hyperparameter tuning untuk KNN
knn_params = {
    'n_neighbors': range(1, 31),
    'weights': ['uniform', 'distance']
}
knn_grid = GridSearchCV(KNeighborsClassifier(), knn_params, refit=True, verbose=2, cv=5)
knn_grid.fit(X_train, y_train)
print("Best KNN Parameters:", knn_grid.best_params_)
knn_best = knn_grid.best_estimator_
y_pred_knn = knn_best.predict(X_test)
print("KNN Classification Report:")
print(classification_report(y_test, y_pred_knn))
print("KNN Accuracy:", accuracy_score(y_test, y_pred_knn))
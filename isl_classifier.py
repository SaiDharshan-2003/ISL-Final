import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from keras.callbacks import EarlyStopping, ReduceLROnPlateau

# Load dataset
data = pd.read_csv('keypoint.csv', header=None)
data[0] = data[0].astype(str)

# Features and labels
X = data.iloc[:, 1:]
enc = LabelEncoder()
y = enc.fit_transform(data[0])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Callbacks
es = EarlyStopping(monitor='val_loss', mode='min', patience=10, restore_best_weights=True, verbose=1)
lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, verbose=1)

# Model architecture
model = keras.Sequential([
    layers.Dense(1470, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.5),
    layers.Dense(832, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.5),
    layers.Dense(428, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.5),
    layers.Dense(264, activation='relu'),
    layers.BatchNormalization(),
    layers.Dropout(0.5),
    layers.Dense(35, activation='softmax')
])

# Compile model
model.compile(
    loss="sparse_categorical_crossentropy",
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    metrics=["accuracy"]
)

# Train model
model.fit(
    X_train, y_train,
    epochs=200,
    batch_size=64,
    validation_split=0.2,
    callbacks=[es, lr_scheduler],
    verbose=1
)

# Evaluate model
model.evaluate(X_test, y_test, verbose=0)

# Predictions and metrics
y_val_pred = model.predict(X_test)
y_val_pred_classes = np.argmax(y_val_pred, axis=1)
acc = accuracy_score(y_test, y_val_pred_classes)
prec = precision_score(y_test, y_val_pred_classes, average='macro')
rec = recall_score(y_test, y_val_pred_classes, average='macro')
f1 = f1_score(y_test, y_val_pred_classes, average='macro')

print("Accuracy:", acc)
print("Precision:", prec)
print("Recall:", rec)
print("F1-score:", f1)

# Save model
model.save("model.h5")


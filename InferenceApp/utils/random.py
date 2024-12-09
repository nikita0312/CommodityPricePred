import tensorflow as tf

model_path = "models/lstm_model.keras"
model = tf.keras.models.load_model(model_path)
print(model.input_shape)

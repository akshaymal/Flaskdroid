import numpy as np
import tensorflow as tf

from keras import layers

class DLModel():
    def __init__(self):
        self.number_of_classes = 10
        self.input_shape = (28,28,1)
        self.model = tf.keras.Sequential(
            [
                tf.keras.Input(shape=self.input_shape),
                layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Flatten(),
                layers.Dropout(0.5),
                layers.Dense(self.number_of_classes, activation="softmax"),
            ]
        )

    def input_data(self, x_train, y_train, x_test, y_test, input_shape):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.input_shape = input_shape


    def preprocess_data(self, custom_data=None, input=None):
        if custom_data is None:
            # Scale images to the [0, 1] range
            self.x_train = self.x_train.astype("float32") / 255
            self.x_test = self.x_test.astype("float32") / 255

            self.x_train = np.expand_dims(self.x_train, -1)
            self.x_test = np.expand_dims(self.x_test, -1)

            self.y_train = tf.keras.utils.to_categorical(self.y_train, self.number_of_classes)
            self.y_test = tf.keras.utils.to_categorical(self.y_test, self.number_of_classes)
        else:
            if input:
                custom_data = custom_data.astype("float32") / 255
                custom_data = np.expand_dims(custom_data, -1)
            else:
                custom_data = tf.keras.utils.to_categorical(custom_data, self.number_of_classes)
            return custom_data


    def train(self, model_path):
        model_exists = False
        try:
            model = tf.keras.models.load_model(model_path)
            model_exists = True
        except:
            print("Model doesn\'t exists. Training it.")
            model_exists = False
        if model_exists:
            self.model = model
        else:
            batch_size = 128
            epochs = 15
            self.model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
            self.model.fit(self.x_train, self.y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)


            self.model.save(model_path)


        # score = self.model.evaluate(self.x_test, self.y_test, verbose=0)
        # print("Test loss:", score[0])
        # print("Test accuracy:", score[1])

    def test(self, model_path):
        print("Loading saved model:")
        model_v = tf.keras.models.load_model(model_path)

        print("Evaluating model on test set:")
        score = model_v.evaluate(self.x_test, self.y_test, verbose=0)
        print("Test loss:", score[0])
        print("Test accuracy:", score[1])


    def get_model(self):
        return self.model
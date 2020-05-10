import keras
from keras import backend as K
from keras.layers import Dense, Embedding
from keras.layers import Input, Flatten, Dropout, Activation
from keras.layers import Conv1D, MaxPooling1D
from keras.models import Model
from keras.models import Sequential


class EmoNet:
    def __init__(self, model=None):
        self.model = model if model else create_emonet_model()
        self._compile()

    def _compile(self):
        self.model.compile(optimizer=keras.optimizers.RMSprop(learning_rate=0.0005, rho=0.9),
                           loss='sparse_categorical_crossentropy',
                           metrics=['accuracy'])

    def fit(self, X_train, X_test, y_train, y_test, batch_size, epochs):
        if X_test is not None:
            val_data = (X_test, y_test)
        else:
            val_data = None

        return self.model.fit(
            X_train, y_train,
            batch_size=batch_size, epochs=epochs,
            validation_data=val_data
        )

    def predict(self, X_test):
        return self.model.predict_classes(X_test)

    def save(self, path):
        self.model.save(path)

    def __repr__(self):
        self.model.summary()
        return ""

    @staticmethod
    def from_file(path):
        model = keras.models.load_model(path)
        return EmoNet(model)


def add_conv_block(model, out_chan, kernel, dropout, pool_size, in_shape):
    model.add(Conv1D(out_chan, kernel, padding='same', input_shape=in_shape))
    model.add(Activation('relu'))
    model.add(Dropout(dropout))
    model.add(MaxPooling1D(pool_size=(pool_size)))


def create_emonet_model():
    model = Sequential()
    add_conv_block(model, 128, 5, 0.1, 2, (40, 1))
    add_conv_block(model, 128, 5, 0.1, 2, (10, 128))
    model.add(Flatten())
    model.add(Dense(8))
    model.add(Activation('softmax'))
    return model

# The full CNN code!
#https://victorzhou.com/blog/keras-cnn-tutorial/
#https://keras.io/layers/convolutional/
#https://stackoverflow.com/questions/44822999/tensorflow-typeerror-value-passed-to-parameter-input-has-datatype-uint8-not-in
####################
#1280 x 720

import numpy as np
import mnist
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from keras.utils import to_categorical

#Format Data


train_images = mnist.train_images()
#print(train_images[1])
train_labels = mnist.train_labels()
#print(train_labels[5])
test_images = mnist.test_images()
#print(test_images.shape)
test_labels = mnist.test_labels()

# Normalize the images (60000, 28, 28)
# train_images[0][0][0] = -0.5
train_images = (train_images / 255) - 0.5
test_images = (test_images / 255) - 0.5


# Reshape the images (60000, 28, 28, 1)
# train_images[0][0][0] = [-0.5]
train_images = np.expand_dims(train_images, axis=3)
test_images = np.expand_dims(test_images, axis=3)

num_filters = 8
filter_size = 3
pool_size = 2
a = True
if a:
# Build the model.
  model = Sequential([
    Conv2D(num_filters, filter_size, input_shape=(28, 28, 1)),
    MaxPooling2D(pool_size=pool_size),
    Flatten(),
    Dense(10, activation='softmax'),
  ])

  # Compile the model.
  model.compile(
    'adam',
    loss='categorical_crossentropy',
    metrics=['accuracy'],
  )

  # Train the model.
  model.fit(
    train_images,
    to_categorical(train_labels),
    epochs=3,
    validation_data=(test_images, to_categorical(test_labels)),
  )

  # Save the model to disk.
  model.save_weights('cnn.h5')

  # Load the model from disk later using:
  # model.load_weights('cnn.h5')

  # Predict on the first 5 test images.
  predictions = model.predict(test_images[:5])
  print('test')
  # Print our model's predictions.
  print(np.argmax(predictions, axis=1)) # [7, 2, 1, 0, 4]

  # Check our predictions against the ground truths.
  print(test_labels[:5]) # [7, 2, 1, 0, 4]
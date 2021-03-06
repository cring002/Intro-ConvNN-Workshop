from keras.models import Model
from keras.layers import Input, Dense, Flatten, Conv2D, MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
#Builds a ConvNet with 2 Conv layers (8 and then 16 filters) 1 Max pooling, 1 dense 64 neuron layer and then 2 outputs
def ConvNet(shape):
  model_input = Input(shape)
  layers = Conv2D(8, (3,3), activation='relu', padding = 'same')(model_input)
  layers = Conv2D(16, (3,3), activation='relu', padding = 'same')(layers)
  layers = MaxPooling2D((2, 2), strides=(2, 2))(layers)
  layers = Flatten()(layers)
  layers = Dense(64, activation='relu')(layers)
  layers = Dense(2, activation='softmax')(layers)
  model = Model(model_input, layers)
  model.compile(optimizer='sgd', loss='categorical_crossentropy', metrics=['accuracy'])
  return model
#Builds a data generator for the supplied dir
def getDataGenerator(_dir,  img_width, img_height, batch_size):
  datagen = ImageDataGenerator(rescale=1./255)
  generator = datagen.flow_from_directory(_dir,  target_size=(img_width, img_height), batch_size=batch_size, class_mode='categorical') 
  return generator
#Main func - Do the training!
def main():
  batch_size = 5
  epochs = 10
  img_width = img_height = 128
  #Get a data generator for the train and test data
  train_generator = getDataGenerator("data/train", img_width, img_height, batch_size)
  test_generator = getDataGenerator("data/test", img_width, img_height, batch_size)
  #Initalise a model
  model = ConvNet((img_width,img_height,3))
  #Fit the data to the model to the training data
  model.fit_generator(train_generator, epochs=epochs )
  #Test the model on the test data
  test_results = (model.evaluate_generator(test_generator))
  print("Loss on Test Data: %f, Accuracy on Test Data: %f" % (test_results[0],test_results[1]))

if __name__ == '__main__':
  main()
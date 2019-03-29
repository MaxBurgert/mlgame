import os
import random
import gym
import numpy as np
import gym_block_world
import matplotlib.pyplot as plt
from keras import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import Adam
from tensorflow.contrib.learn.python.learn.estimators._sklearn import train_test_split

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

env = gym.make('block_world-v0')
env.reset()

goal_steps = 40
score_requirement = 0
initial_games = 20000


def model_data_preparation():
    training_data = []
    accepted_scores = []
    for game_index in range(initial_games):
        score = 0
        game_memory = []
        previous_observation = []
        for step_index in range(goal_steps):
            action = random.randrange(0, 4)
            observation, reward, done, info = env.step(action)

            if len(previous_observation) > 0:
                game_memory.append([previous_observation, action])

            previous_observation = observation
            score += reward
            if done:
                break

        if score >= score_requirement:
            accepted_scores.append(score)
            for data in game_memory:
                if data[1] == 0:
                    output = [1, 0, 0, 0]
                elif data[1] == 1:
                    output = [0, 1, 0, 0]
                elif data[1] == 2:
                    output = [0, 0, 1, 0]
                elif data[1] == 3:
                    output = [0, 0, 0, 1]
                training_data.append([data[0], output])

        env.reset()

    print(accepted_scores)
    print('Average Score:', sum(accepted_scores) / len(accepted_scores))
    return training_data


def build_model(input_size, output_size):
    model = Sequential()
    model.add(Dense(128, input_dim=input_size, activation='relu'))
    model.add(Dropout(0.25, noise_shape=None, seed=None))
    model.add(Dense(52, activation='relu'))
    model.add(Dense(52, activation='relu'))
    model.add(Dense(52, activation='relu'))
    model.add(Dense(52, activation='relu'))
    model.add(Dropout(0.2, noise_shape=None, seed=None))
    model.add(Dense(output_size, activation='softmax'))
    model.compile(loss='mse', optimizer=Adam(), metrics=['accuracy'])

    return model


def train_model(training_data):
    X = np.array([i[0] for i in training_data]).reshape(-1, len(training_data[0][0]))
    y = np.array([i[1] for i in training_data]).reshape(-1, len(training_data[0][1]))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = build_model(input_size=len(X[0]), output_size=len(y[0]))

    history = model.fit(X_train, y_train, batch_size=512, epochs=200, verbose=0, validation_data=(X_test, y_test),
                        shuffle=True)
    return model, history


def visualize():
    # Plot training & validation accuracy values
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()

    # Plot training & validation loss values
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper right')
    plt.show()


training_data = model_data_preparation()
trained_model, history = train_model(training_data)
visualize()

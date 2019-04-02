import argparse
import os
import numpy as np

from keras.models import model_from_json


def test_net(model_name: str, data_name: str):
    """
    Compares the predictions from the chess given neural net model to
    the actual results of the games, and prints the percent of the boards
    that the model predicted correctly.

    :param model_name: the name of the model to load.
                       - There should be files '{model_name}.h5' and '{model_name}.json'
                        to specify the configuration and weights of the model.
                       - The model should be able to take in data representing a chess board
                        and return a value between -1 and 1 predicting whether black or white
                        will win.
    :param data_name: the name of the data to test the model on.
                        There should be files 'x_{data_name}.npy' and 'y_{data_name}.npy'.
    """
    # Load in the model
    file_dir = os.path.dirname(__file__)
    model_path = os.path.join(file_dir, model_name)
    with open(model_path + ".json", "r") as file:
        model = model_from_json(file.read())
    model.load_weights(model_path + ".h5")

    # Load in the data
    x = np.load(os.path.join(file_dir, f"x_{data_name}.npy"))
    y = np.load(os.path.join(file_dir, f"y_{data_name}.npy"))

    # Predict all of the data in the validation set to get an idea of how the
    # model is doing.
    predictions = model.predict(x)  # Has shape nx1

    predictions = predictions.reshape(y.shape)

    # Compare predictions to the actual labels (creates an n array of booleans)
    correct = ((predictions > 0) & (y > 0)) | ((predictions < 0) & (y < 0))

    # Print the percentage of predictions that were correct
    print(sum(correct) / correct.shape[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "model_name",
        help="the name of the model to test. There should be <model_name>.json "
        "and <model_name>.h5 files in app/neural_net/",
    )
    parser.add_argument(
        "data_name",
        help="the name of the data to use. There should "
        "be x_<data_name>.npy and y_<data_name>.npy files in app/neural_net/",
    )

    args = parser.parse_args()
    test_net(args.model_name, args.data_name)
def normalise_dataset(self, data):
    return np.sum(data[0] / data[1], axis=1)
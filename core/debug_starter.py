from core.services import DefaultDatasetCreator, DefaultModelType, DefaultModelCreator


class DebugStarter:
    def __init__(self, model: str):
        if model == "forest":
            model_type = DefaultModelType.FOREST
        elif model == "neuro":
            model_type = DefaultModelType.MLP
        elif model == "boost":
            model_type = DefaultModelType.XGBOOST
        else:
            model_type = DefaultModelType.FOREST

        self._dataset_creator = DefaultDatasetCreator()
        self._model_creator = DefaultModelCreator(model_type)

    def get_dataset_and_model(self):
        dataset = self._get_dataset()
        model = self._get_model()

        return dataset, model

    def _get_dataset(self):
        dataset = self._dataset_creator.get_dataset()

        return dataset

    def _get_model(self):
        X = self._dataset_creator.get_X()
        y = self._dataset_creator.get_y()
        model = self._model_creator.fit_model(X, y)

        return model

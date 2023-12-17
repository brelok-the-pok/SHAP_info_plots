from app.services.pickle_service import PickleService
from app.services.model_explainer import ModelExplainer

def test_data_load():
    service = PickleService()

    mono_object = service.get_dataset_and_model(r"D:\AMI\data\obj_v2")

    assert mono_object.model is not None
    assert mono_object.dataset is not None

def test_model_explainer():
    service = PickleService()

    mono_object = service.get_dataset_and_model(r"D:\AMI\data\obj_v2")

    explainer = ModelExplainer(mono_object.model)
    explainer.calculate_for_dataset(mono_object.dataset, mono_object.dataset.columns[0])

    assert len(explainer.get_n_most_important_columns(2)) == 2
    assert explainer.get_ice_importance() is not None
    assert explainer.get_ice_predictions() is not None
    assert explainer.get_centered_importance() is not None




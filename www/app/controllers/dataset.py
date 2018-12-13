from app.domain.dataset import dataset_gateways
import os.path

class DatasetController:
    def __init__(self, mapper, storage_path):
        self.__mapper = mapper
        self.__storage_path = storage_path

    def list(self):
        return [self.__ds_to_dict(ds) for ds in self.__mapper.all()]

    def __ds_to_dict(self, ds):
        return {'rating': ds.rating(), 'summary': ds.summary(), 'domain': ds.domain(), 'stat': ds.stats()}

    def upload(self, ds_path):
        ul_path = os.path.join(self.__storage_path, ds_path)
        return '', 200

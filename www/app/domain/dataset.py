import os
import os.path
import json
import csv

META_FILENAME='.dataset'

def dataset_gateways(path):
    for name in os.listdir(path):
        ds_path =os.path.join(path, name)
        if name != '.' and name !='..' and os.path.isdir(ds_path):
            try:
                with open(os.path.join(ds_path, META_FILENAME)) as ds_file_meta:
                    meta = json.load(ds_file_meta)
                    data_files = [fn for fn in os.listdir(ds_path) if fn != '.' and fn != '..' and fn != META_FILENAME and os.path.isfile(fn)]
                    yield dict(path=ds_path,
                               url=meta['url'],
                               desc=meta['desc'],
                               rating=meta['rating'],
                               summary=meta['summary'],
                               domain=meta['domain'],
                               stat=meta['stat'],
                               files=data_files)
            except Exception as e:
                raise DatasetReadError(str(e))


def csv_reader_gateway(file_name):
    with open(file_name) as f:
        reader = csv.reader(f)
        yield next(reader)


def writer_gateway(file_name, chunk):
    with open(file_name, mode='r+b') as f:
        f.write(chunk)


def write_meta(dataset):
    os.makedirs(dataset.path(), mode=0o700, exist_ok=True)
    meta_fn = os.path.join(dataset.path(), META_FILENAME)
    with open(meta_fn, 'w+') as f:
        json.dump(dataset.to_dict(), f)


class DatasetReadError(RuntimeError):
    def __init__(self, *args, **kwargs):
        super().__init__(self, args, kwargs)


class Dataset:
    def __init__(self, path, url, desc, rating, summary, domain, stat, files):
        self._url = url
        self._desc = desc
        self._path = path
        self._rating = rating
        self._summary = summary
        self._domain = domain
        self._stat = stat
        self._files = files

    def url(self):
        return self._url

    def description(self):
        return self._desc

    def path(self):
        return self._path

    def rating(self):
        return self._rating

    def summary(self):
        return self._summary

    def domain(self):
        return self._domain

    def stat(self):
        return self._stat

    def files(self):
        return self._files

    def set(self, **kwargs):
        def set_prop(prop):
            if prop in kwargs.keys():
                setattr(self, '_' + prop, kwargs[prop])

        set_prop('url')
        set_prop('desc')
        set_prop('path')
        set_prop('rating')
        set_prop('summary')
        set_prop('domain')
        set_prop('stat')
        set_prop('files')

    def to_dict(self):
        return dict(url=self.url(),
                    desc=self.description(),
                    rating=self.rating(),
                    summary=self.summary(),
                    domain=self.domain(),
                    stat=self.stat(),
                    files=self.files())


class DatasetMapper:
    def __init__(self, path, factory):
        self.__all = {gw['path']: factory.reconstitue(gw['path'], gw['url'], gw['desc']) for gw in dataset_gateways(path)}
        self.__factory = factory

    def all(self):
        return self.__all

    def insert(self, entity):
        pass


class DatasetFactory:
    def create(self, path='', url='', desc='', rating='0', summary='', domain='', stat=''):
        return Dataset(path, url, desc, rating, summary, domain, stat)

    def reconstitute(self, path, url, desc, rating, summary, domain, stat):
        return Dataset(path, url, desc, rating, summary, domain, stat)





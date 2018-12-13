import pytest
import unittest
from unittest.mock import MagicMock, Mock, patch, mock_open
from pytest import fixture, yield_fixture, mark

import os
import os.path
import json
import io


from app.domain.dataset import Dataset, dataset_gateways, META_FILENAME, DatasetReadError


@patch('os.path.isdir', Mock(return_value=True))
@patch('os.path.isfile', Mock(return_value=True))
@mark.parametrize('ds_path, dirs, json_load_rv', [('/path/to/datasets',
                                                   ['dataset1', 'dataset2'],
                                                   [{'url': 'http://host/datasets/dataset1', 'desc': 'dataset1 description', 'rating': 0, 'summary': 'Summary', 'domain': 'Domain', 'stat': 'Stat'},
                                                    {'url': 'http://host/datasets/dataset2', 'desc': 'dataset2 description', 'rating': 1, 'summary': 'Summary', 'domain': 'Domain', 'stat': 'Stat'}])])
def test_gateway_must_read_datasets_meta_info(ds_path, dirs, json_load_rv):
    with patch('os.listdir', Mock(return_value=dirs)), patch('builtins.open', mock_open()) as open_mock:
        with patch('json.load', Mock(side_effect=json_load_rv)):
            ds_name = (dir for dir in dirs)
            ds_meta = (meta for meta in json_load_rv)
            for ds in dataset_gateways(ds_path):
                dataset_name = next(ds_name)
                dataset_meta = next(ds_meta)
                open_mock.assert_called_with(os.path.join(ds_path, dataset_name, META_FILENAME))
                assert ds['path'] == os.path.join(ds_path, dataset_name)
                assert ds['url'] == dataset_meta['url']
                assert ds['desc'] == dataset_meta['desc']


@patch('os.path.isdir', Mock(return_value=True))
@patch('os.path.isfile', Mock(return_value=True))
@mark.parametrize('ds_path, dirs', [('/path/to/datasets',
                                    ['dataset1', 'dataset2'])])
def test_gateway_must_throw_if_read_error(ds_path, dirs):
    with patch('os.listdir', Mock(return_value=dirs)), patch('builtins.open', mock_open()):
        with pytest.raises(DatasetReadError):
            next(dataset_gateways(ds_path))


def test_dataset_must_set_property():
    sut = Dataset('', '', '', '', '', '', '', '')
    path = '/path/to/dataset'
    url = 'dataset-url'
    desc = 'dataset description'
    rating = 'rating'
    summary = 'summary'
    domain = 'domain'
    stat = 'stat'
    files = ['a-file', 'another-file']
    sut.set(path=path, url=url, desc=desc, rating=rating, summary=summary, domain=domain, stat=stat, files=files)

    assert sut.path() == path
    assert sut.url() == url
    assert sut.description() == desc
    assert sut.rating() == rating
    assert sut.summary() == summary
    assert sut.domain() == domain
    assert sut.stat() == stat
    assert sut.files() == files


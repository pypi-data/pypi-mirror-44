from elasticsearch import Elasticsearch
from math import ceil
from es_builder.query_builder import EsQueryBuilder, EsAggsBuilder, EsSearchResultParse
import logging.handlers
from es_builder.utils import merge_str, generator_list

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
logger = logging.getLogger('eslog')
logger.setLevel('DEBUG')
logger.addHandler(console)
es_cli = Elasticsearch('10.0.5.251:12200')


class Base(object):
    def __init__(self):
        self.cli = es_cli
        self.index = ''
        self.doc_type = ''
        self.test_index = ''
        self.primary_keys = ''

    def get_index(self):
        # if not config.is_product() and self.test_index:
        #     return self.test_index
        return self.index

    def get_doc_type(self):
        return self.doc_type

    def search(self, query):
        logger.info("esSearch: %s, %s, %s", self.get_index(),
                    self.get_doc_type(), query)
        return self.cli.search(self.get_index(), self.get_doc_type(), query,
                               request_timeout=60)

    def bulk(self, body):
        logger.info("esBulk: %s, %s, %s", self.get_index(), self.get_doc_type(),
                    len(body) / 2)
        result = self.cli.bulk(body)
        if result['errors']:
            logger.error("esBulk: %s, %s, %s, %s", self.get_index(),
                         self.get_doc_type(), len(body) / 2, result)

    def script_update(self, docs, primary_keys=None):
        if not primary_keys:
            primary_keys = self.primary_keys
        if not primary_keys:
            raise Exception('not found primary keys')
        body = []
        for _ in docs:
            _id = _[primary_keys] if isinstance(primary_keys,
                                                str) else merge_str(
                *(_[_key] for _key in primary_keys), dividing='_')
            body.append({
                'update': {
                    '_id': _id, '_type': self.get_doc_type(),
                    '_index': self.get_index()
                }
            })
            body.append({'script': _.get('script')})
        if len(body) > 0:
            self.bulk(body)

    def page_update(self, docs, size=500, print_progress=False):
        count = len(docs)
        temp = 1
        for _ in generator_list(docs, size):
            self.update(_)
            temp += 1
            if print_progress:
                print('%d/%d' % (temp * size, count))

    def update(self, docs, primary_keys=None, upsert=True):
        if not primary_keys:
            primary_keys = self.primary_keys
        if not primary_keys:
            raise Exception('not found primary keys')

        for _docs in generator_list(docs, 500):
            body = []
            for _ in _docs:
                _id = _[primary_keys] if isinstance(primary_keys,
                                                    str) else merge_str(
                    *(_[_key] for _key in primary_keys), dividing='_')
                body.append({
                    'update': {
                        '_id': _id, '_type': self.get_doc_type(),
                        '_index': self.get_index()
                    }
                })
                body.append({'doc': _, 'doc_as_upsert': upsert})
            if len(body) > 0:
                self.bulk(body)

    def appned(self, docs, field, primary_keys=None):
        if not primary_keys:
            primary_keys = self.primary_keys
        if not primary_keys:
            raise Exception('not found primary keys')

        for _docs in generator_list(docs, 500):
            body = []
            for _ in _docs:
                _id = _[primary_keys] if isinstance(primary_keys,
                                                    str) else merge_str(
                    *(_[_key] for _key in primary_keys), dividing='_')
                body.append({
                    'update': {
                        '_id': _id, '_type': self.get_doc_type(),
                        '_index': self.get_index()
                    }
                })
                body.append({
                    'script': {
                        "inline": "ctx._source.%s.addAll("
                                  "params.append)" % field,
                        'params': {'append': _.get(field)}
                    }
                })
            if len(body) > 0:
                self.bulk(body)

    def delete(self, doc_id):
        self.cli.delete(self.get_index(), self.get_doc_type(), doc_id)

    def delete_by_query(self, query):
        return self.cli.delete_by_query(self.get_index(), query,
                                        doc_type=self.doc_type,
                                        request_timeout=60)

    def exists(self, doc_id):
        return self.cli.exists(self.get_index(), self.get_doc_type(), doc_id)

    def batch_generator(self, query_builder=None, page_size=500, get_id=True):
        """
        批量获取列表
        :param page_size:
        :param query_builder:
        :param get_id:
        :return:
        """
        if query_builder is None:
            query_builder = EsQueryBuilder()
        result = EsSearchResultParse(
            self.search(query_builder.get_query(1, page_size)))
        count = result.get_count()
        yield result.get_list(get_id)
        page_max = int(ceil(count / page_size))
        for page in range(2, page_max + 1):
            yield EsSearchResultParse(
                self.search(query_builder.get_query(page, page_size))).get_list(
                get_id)

    def scroll_query(self, query_builder=None, page_size=500, scroll='5m',
                     print_progress=False, get_id=False):
        """
        scroll
        :param query_builder:
        :param page_size:
        :param scroll:
        :param print_progress:
        :param get_id:
        :return:
        """
        if query_builder is None:
            query_builder = EsQueryBuilder()
        result = EsSearchResultParse(self.cli.search(index=self.get_index(),
                                                     doc_type=self.get_doc_type(),
                                                     body=query_builder,
                                                     params={'scroll': scroll}))
        scroll_id = result.get_scroll_id()
        count = result.get_count()
        page_max = int(ceil(count / page_size))
        if print_progress:
            print(1, page_max, self.get_doc_type())
        yield result.get_list(get_id)
        for page in range(2, page_max + 1):
            if print_progress:
                print(page, page_max, self.get_doc_type())
            result = EsSearchResultParse(
                self.cli.scroll(scroll_id=scroll_id, params={'scroll': scroll}))
            scroll_id = result.get_scroll_id()
            yield result.get_list(get_id)
        self.cli.clear_scroll(scroll_id)

    def scroll(self, query_builder=None, page_size=500, scroll='5m',
               print_progress=False, get_id=False):
        """
        scroll
        :param query_builder:
        :param page_size:
        :param scroll:
        :param print_progress:
        :param get_id:
        :return:
        """
        if query_builder is None:
            query_builder = EsQueryBuilder()
        result = EsSearchResultParse(self.cli.search(index=self.get_index(),
                                                     doc_type=self.get_doc_type(),
                                                     body=query_builder.get_query(
                                                         1, page_size),
                                                     params={'scroll': scroll}))
        scroll_id = result.get_scroll_id()
        count = result.get_count()
        page_max = int(ceil(count / page_size))
        if print_progress:
            print(1, page_max, self.get_doc_type())
        yield result.get_list(get_id)
        for page in range(2, page_max + 1):
            if print_progress:
                print(page, page_max, self.get_doc_type())
            result = EsSearchResultParse(
                self.cli.scroll(scroll_id=scroll_id, params={'scroll': scroll}))
            scroll_id = result.get_scroll_id()
            yield result.get_list(get_id)
        self.cli.clear_scroll(scroll_id)

    def get_scroll_dict(self, key: str, fields=None,
                        es_builder=EsQueryBuilder()):
        if fields is None:
            fields = []
        if fields:
            fields.append(key)
        data = {}
        for _scroll in self.scroll(es_builder.source(fields),
                                   print_progress=True):
            for _ in _scroll:
                if _.get(key) is None:
                    continue
                data[_[key]] = _
        return data

    def get_scroll_list(self, fields: list, es_builder=EsQueryBuilder()):
        data = []
        for _scroll in self.scroll(es_builder.source(fields),
                                   print_progress=True):
            for _ in _scroll:
                data.append(_)
        return data

    def get_scroll_tuple_dict(self, key: list, fields=None,
                              es_builder=EsQueryBuilder()):
        if fields is None:
            fields = []
        if fields:
            fields += key
        data = {}
        for _scroll in self.scroll(es_builder.source(fields),
                                   print_progress=True):
            for _ in _scroll:
                _key = tuple([_.get(x) for x in key])
                data[_key] = _
        return data

    @classmethod
    def get_es_fields(cls):
        """
        获取所有的EsField（字段）
        :return:
        """
        return {x: {'name': x.name, 'type': x.es_type, 'comment': x.comment} for
                _, x
                in
                cls.__dict__.items() if type(x) == EsField}

    @classmethod
    def get_fields(cls):
        """
        获取所有的EsField（字段）
        :return:
        """
        return {x if not x.show_key else x.show_key: {
            'name': x.name, 'type': x.es_type, 'comment': x.comment
        } for _, x in
            cls.__dict__.items() if type(x) == EsField and x.es_type}

    @classmethod
    def get_fields_dict(cls):
        """
        获取EsField字段字典
        :return:
        """
        return {x: x for _, x in cls.__dict__.items() if type(x) == EsField}

    def get_filter_query(self, filter_data: dict):
        """
        获取过滤条件
        :param filter_data:
        :return:
        """
        query = self.get_default_query()
        for _key, _value in filter_data.items():
            if not _value:
                continue
            if type(_value) == list:
                query.terms(_key, _value)
            elif type(_value) == dict:
                query.range_e(_key,
                              _value['start'] if _value.get('start') else None,
                              _value['end'] if _value.get('end') else None)
            else:
                query.term(_key, _value)
        return query

    def get_default_query(self):
        """
        子类过滤会有一些过滤条件
        :return:
        """
        return EsQueryBuilder()

    def get_search_config(self):
        return self.get_fields()

    # 获取string类型的字段名
    def get_string_name(self):
        """
        获取前段显示的字段名称
        :return:
        """
        string_list = []
        _list = self.get_fields_dict()
        [string_list.append(_) for _ in _list if _list[_].content == 1]
        if not string_list:
            return {}
        es_builder = EsAggsBuilder()
        final_dict = {}
        # 聚合所有type为string类型的
        for _s in string_list:
            es_builder.terms(_s, _s)
        aggs_result = self.get_default_query().aggs(es_builder).search(
            self).get_aggregations()

        for _key, _ in aggs_result.items():
            name_list = []
            for _name in _['buckets']:
                name = _name.get('key')
                if not name:
                    name_list.append({"name": '', 'value': str(name)})
                else:
                    name_list.append({"name": name, "value": str(name)})
            final_dict.update({_key: name_list})
        final_dict.update(self.get_string_change_name())
        return final_dict

    def get_string_change_name(self):
        return {}

    def get_sum_dict(self, key, fields, query=None, add=None, count=False):
        if add is None:
            add = {}
        if query is None:
            query = self.get_default_query()
        agg_query = EsAggsBuilder()
        for _field in fields:
            agg_query.sum(_field, _field)

        result = {}
        for x in query.aggs(
                EsAggsBuilder().terms(key, key, 10000).aggs(agg_query)).search(
            self).get_aggregations()[key]['buckets']:
            result.setdefault(x.get('key'), {
                _field: round(x.get(_field, {}).get('value', 0), 2)
                for _field in fields
            })
            if count:
                result[x.get('key')]['count'] = x.get('doc_count', 0)
        if add:
            for _k, _v in add.items():
                _v.update(result.get(_k, {}))
            return add
        return result


class EsField(str):
    er_type = None
    comment = None
    name = None
    parameter = None

    def __new__(cls, value, *args, **kwargs):
        # explicitly only pass value to the str constructor
        return super(EsField, cls).__new__(cls, value)

    def __init__(self, value, es_type='', comment='', name='', parameter=None,
                 *args, **kwargs):
        # ... and don't even call the str initializer
        super().__init__()
        if parameter is None:
            parameter = {}
        self.es_type = es_type
        self.comment = comment
        self.name = name
        self.parameter = parameter
        # 是否需要搜索枚举
        self.content = kwargs.get('content')
        # 前端显示使用
        self.show_key = kwargs.get('show_key')

    def keyword(self):
        return self + '.keyword'

from sqlalchemy import create_engine
import json
import csv


class IndexedDict(object):
    """
    A dictionary that can be accessed by index. This object tries to emulate
    the behavior of a SqlAlchemy Row object.
    """

    def __init__(self, keys, values):
        self._keys = tuple(keys)
        self._values = tuple(values)

    def __getitem__(self, key):
        try:
            return self._values[key]
        except (IndexError, TypeError):
            idx = self._keys.index(key)
            return self._values[idx]

    def values(self):
        return self._values

    def to_dict(self):
        return dict(zip(self._keys, self._values))


class Extractor(object):

    def __init__(
            self, db_connection_string, param_file, query_file, output_file,
            query_param):
        self._db_connection_string = db_connection_string
        self._param_file = param_file
        self._query_file = query_file
        self._output_file = output_file
        self._query_param = query_param

    def perform_extraction(self):
        """
        query_param: whether we should query the params or just use the file as
        params
        """

        engine = create_engine(self._db_connection_string)
        conn = engine.connect()

        param_keys = []
        param_list = []
        # first need to check whether we need to get a list of IDs.
        if self._query_param:
            # need to find the list of IDs using the given query.
            with open(self._param_file, "rb") as param_query_file:
                the_query = param_query_file.read()
                result = conn.execute(the_query)
                param_keys = result.keys()
                for row in result:
                    param_list.append(IndexedDict(param_keys, row))
        else:
            with open(self._param_file, "rb") as param_query_file:
                csvreader = csv.reader(param_query_file)
                param_keys = csvreader.next()
                for row in csvreader:
                    param_list.append(IndexedDict(param_keys, row))

        # Now we have the param list, parse and execute the queries in the
        # query_file.
        with open(self._query_file, "r") as the_query_file:
            query_file_dict = json.load(the_query_file)

        with open(self._output_file, "wb") as the_output_file:
            csvwriter = csv.writer(the_output_file, lineterminator="\n")
            # write out the header
            csvwriter.writerow(param_keys + query_file_dict.keys())

            for indexed_dict in param_list:
                row = list(indexed_dict.values())
                for feat_name, feat_query in query_file_dict.iteritems():
                    result = conn.execute(
                        feat_query.format(**indexed_dict.to_dict()))
                    feat_value = result.fetchone()[0]
                    row.append(feat_value)
                    result.close()
                csvwriter.writerow(row)

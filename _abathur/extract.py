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


class Extractor(object):

    def __init__(
            self, db_connection_string, ident_file, query_file, output_file,
            query_ident):
        self._db_connection_string = db_connection_string
        self._ident_file = ident_file
        self._query_file = query_file
        self._output_file = output_file
        self._query_ident = query_ident

    def perform_extraction(self):
        """
        query_ident: whether we should query the IDs or just use the file as
        IDs
        """

        engine = create_engine(self._db_connection_string)
        conn = engine.connect()

        param_keys = []
        id_list = []
        # first need to check whether we need to get a list of IDs.
        if self._query_ident:
            # need to find the list of IDs using the given query.
            with open(self._ident_file, "rb") as ident_query_file:
                the_query = ident_query_file.read()
                result = conn.execute(the_query)
                param_keys = result.keys()
                for row in result:
                    id_list.append(IndexedDict(param_keys, row))
        else:
            with open(self._ident_file, "rb") as ident_query_file:
                csvreader = csv.reader(ident_query_file)
                param_keys = csvreader.next()
                for row in csvreader:
                    id_list.append(IndexedDict, row)

        # Now we have the ID list, parse and execute the queries in the
        # query_file.
        with open(self._query_file, "r") as the_query_file:
            query_file_dict = json.load(the_query_file)

        with open(self._output_file, "wb") as the_output_file:
            csvwriter = csv.writer(the_output_file, lineterminator="\n")
            # write out the header
            csvwriter.writerow(param_keys + query_file_dict.keys())

            for indexed_dict in id_list:
                row = list(indexed_dict.values())
                for feat_name, feat_query in query_file_dict.iteritems():
                    result = conn.execute(feat_query.format(ident=ident))
                    feat_value = result.fetchone()[0]
                    row.append(feat_value)
                    result.close()
                csvwriter.writerow(row)

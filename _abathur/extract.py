from sqlalchemy import create_engine
import json
import csv


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

        id_list = []
        # first need to check whether we need to get a list of IDs.
        if self._query_ident:
            # need to find the list of IDs using the given query.
            with open(self._ident_file, "rb") as ident_query_file:
                the_query = ident_query_file.read()
                result = conn.execute(the_query)
                for row in result:
                    id_list.append(row[0])
        else:
            with open(self._ident_file, "rb") as ident_query_file:
                for line in ident_query_file:
                    if line[-1] == "\n":
                        line = line[:-1]
                    id_list.append(line)

        # Now we have the ID list, parse and execute the queries in the
        # query_file.
        query_file_dict = json.load(self._query_file)
        with open(self._output_file, "wb") as the_output_file:
            csvwriter = csv.writer(the_output_file)
            # write out the header
            csvwriter.writerow(query_file_dict.keys())

            for ident in id_list:
                row = [ident, ]
                for feat_name, feat_query in query_file_dict.iteritems():
                    result = conn.execute(feat_query.format(ident=ident))
                    feat_value = result.fetchone()[0]
                    row.append(feat_value)
                    result.close()
                csvwriter.writerow(row)

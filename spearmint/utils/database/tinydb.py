import sys
import time
from tinydb import TinyDB, Query
import numpy as np
import json

from .abstractdb import AbstractDB
from spearmint.utils.compression import compress_nested_container, decompress_nested_container

class TinyDBHandler(AbstractDB):
    def __init__(self, database_path='db.json'):
        try:
            self.db = TinyDB(database_path)
        except Exception as e:
            raise Exception(f'Could not establish a connection to TinyDB. Error: {str(e)}')

    def save(self, save_doc, experiment_name, experiment_field, field_filters=None):
        """
        Saves a document into the database.
        Compresses any numpy arrays so that they can be saved to TinyDB.
        If field_filters is empty, updates an existing document if one exists, otherwise inserts a new one.
        If field_filters is not empty, and a document matches field_filters, it will be updated. Otherwise, a new document will be inserted.
        """
        if field_filters is None:
            field_filters = {}

        save_doc = compress_nested_container(save_doc)
        table = self.db.table(f'{experiment_name}_{experiment_field}')

        # If field_filters is provided, construct a query. Otherwise, use None to signify no specific query.
        query = None
        if field_filters:
            QueryObj = Query()
            for key, value in field_filters.items():
                if query is None:
                    query = (QueryObj[key] == value)
                else:
                    query &= (QueryObj[key] == value)

        if query is None:
            # If no specific query, check if the table already has any documents.
            existing_docs = table.all()
            if existing_docs:
                # Update the first document if one exists.
                doc_id = existing_docs[0].doc_id
                table.update(save_doc, doc_ids=[doc_id])
            else:
                # Insert a new document if the table is empty.
                table.insert(save_doc)
        else:
            # If a specific query is defined, search for matching documents.
            found_docs = table.search(query)
            if found_docs:
                # Update the first document found.
                doc_id = found_docs[0].doc_id
                table.update(save_doc, doc_ids=[doc_id])
            else:
                # Insert a new document if no matches are found.
                table.insert(save_doc)

    def load(self, experiment_name, experiment_field, field_filters=None):
        if field_filters is None:
            field_filters = {}

        table = self.db.table(f'{experiment_name}_{experiment_field}')
        
        # Constructing the query from field_filters
        QueryObj = Query()
        query = None
        for key, value in field_filters.items():
            if query is None:
                query = (QueryObj[key] == value)
            else:
                query = query & (QueryObj[key] == value)
        
        if query is not None:
            results = table.search(query)
        else:
            results = table.all()  # or table.search(QueryObj) for all records if no filters are provided

        if len(results) == 0:
            return None
        elif len(results) == 1:
            return decompress_nested_container(results[0])
        else:
            return [decompress_nested_container(result) for result in results]

    def remove(self, experiment_name, experiment_field, field_filters={}):
        table = self.db.table(f'{experiment_name}_{experiment_field}')
        table.remove(field_filters)

    def remove_experiment(self, experiment_name):
        # TinyDB does not support dropping tables directly; remove file if needed
        raise NotImplementedError("TinyDB does not support dropping tables directly from the database object.")

    def remove_collection(self, experiment_name, experiment_field):
        self.db.drop_table(f'{experiment_name}_{experiment_field}')

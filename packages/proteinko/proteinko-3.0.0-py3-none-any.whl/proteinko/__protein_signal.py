"""
Copyright (c) 2018 Stefan Stojanovic

"""

import numpy as np
from scipy.stats import norm
import warnings
import pandas as pd
from proteinko.schemas import *
import io
import base64


class ProteinSignal:

    schemas = {'hydropathy':
                   pd.read_csv(io.BytesIO(base64.b64decode(hydropathy))),
               'acceptors':
                   pd.read_csv(io.BytesIO(base64.b64decode(acceptor))),
               'donors':
                   pd.read_csv(io.BytesIO(base64.b64decode(donor))),
               'pI':
                   pd.read_csv(io.BytesIO(base64.b64decode(pI))),
               'volume':
                   pd.read_csv(io.BytesIO(base64.b64decode(volume)))}

    scale = 0.8
    vector_length = 100
    normalize = False

    def __init__(self, scale=0.8, vector_length=100, normalize=False):
        self.scale = scale
        self.vector_length = vector_length
        self.normalize = normalize

    def __normalize_range(self, array, x, y):
        """
        Normalize array of values to arbitrary range. For protewave use case
        array is normalized to [-1, 1] range. This is to reflect opposite values
        of amino acid properties.

        :param array: Array or list-like to be normalized
        :param x: Lower bound of the range
        :param y: Upper bount of the range
        
        :return: numpy array with normalized values
        """
        array = np.array(array)
        array = (array - min(array)) / (max(array) - min(array))
        return array * (np.abs(x - y)) + min([x, y])

    def __prepare_schema(self, schema):
        """
        Prepare schema for processing with get_signal function. Mainly just
        convert letters to uppercase and replace zero values with small
        non-zero values.

        :param schema: Initialized pd DataFrame with schema

        :return: Processed pd DataFrame
        """
        schema['amino_acid'] = schema['amino_acid'].str.upper()
        schema['value'] = self.__normalize_range(schema['value'], -1, 1)
        schema.replace(0, 0.0001, inplace=True)
        return schema

    def get_signal(self, sequence, schema):

        sequence = sequence.upper()

        schema = self.schemas[schema]
        schema = self.__prepare_schema(schema)

        map_length = len(sequence) * 100
        span = map_length / len(sequence)
        vector = np.zeros(int(map_length + 2 * span))

        for i, AA in enumerate(sequence):
            row = schema[schema['amino_acid'] == AA]
            if len(row) != 1:
                warnings.warn('Ambiguous schema for amino acid {}. Value '
                              'will be set to mean value.'.format(AA),
                              Warning)
                AA_value = np.mean(schema['value'])
            else:
                AA_value = float(row['value'])

            x = np.linspace(norm.ppf(0.01), norm.ppf(0.99), int(3 * span))
            pdf = norm.pdf(x, scale=self.scale) * AA_value
            vector[int(i * span):int((i + 3) * span)] += pdf

        # Now trim vector
        vector = vector[int(span):int(-span)]
        return_vector, offset = [], 0
        step = int(len(vector) / self.vector_length)

        for i in range(self.vector_length):
            tick = vector[offset]
            offset += step
            return_vector.append(tick)

        if self.normalize:
            return_vector = (return_vector - np.min(return_vector)) / (
                    np.max(return_vector) - np.min(return_vector))
        return return_vector

    def add_schema(self, path, AA_col, value_col, key, sep=',', header=None,
                   comment=None):
        """
        Add custom amino acid residue schema from file.

        :param path: Path to file with amino acid list and values
        :param AA_col: Column index for amino acid residue in the file
        :param value_col: Column index for values in the file
        :param key: Key by which schema will be stored
        :param sep: Separator by which values are separated in the file
        :param header: Header row of the file (0 if first row in file)
        :param comment: Comment lines ti skip (usually "#" or None)

        :return: None. Processed dataframe will be stored and ready to be used
                 by the provided key.
        """
        csv = pd.read_csv(path, sep=sep, header=header, comment=comment)
        df = pd.DataFrame()
        df['amino_acid'] = csv.iloc[:, AA_col]
        df['value'] = csv.iloc[:, value_col]
        self.schemas[key] = df
        return None

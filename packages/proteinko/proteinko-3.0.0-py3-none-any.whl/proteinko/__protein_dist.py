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


class Proteinko:

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

    def __normalize_range(self, array, norm_range):
        """
        Normalize array of values to arbitrary range. For protewave use case
        array is normalized to [-1, 1] range. This is to reflect opposite values
        of amino acid properties.

        :param array: Array or list-like to be normalized
        :param x: Lower bound of the range
        :param y: Upper bount of the range
        
        :return: numpy array with normalized values
        """
        x = norm_range[0]
        y = norm_range[1]
        array = np.array(array)
        array = (array - min(array)) / (max(array) - min(array))
        return array * (np.abs(x - y)) + min([x, y])

    def __prepare_schema(self, schema, norm_range):
        """
        Prepare schema for processing with get_signal function. Mainly just
        convert letters to uppercase and replace zero values with small
        non-zero values.

        :param schema: Initialized pd DataFrame with schema

        :return: Processed pd DataFrame
        """
        schema['amino_acid'] = schema['amino_acid'].str.upper()
        schema['value'] = self.__normalize_range(schema['value'], norm_range)
        schema.replace(0, 0.0001, inplace=True)
        return schema

    def get_dist(self, sequence, schema, sigma=0.8, vlen=None,
                   trim=False, normed=False, scale=100, norm_range=(-1,1)):

        vector_length = vlen
        trim_vector = trim
        normalize_vector = normed

        sequence = sequence.upper()
        schema = self.schemas[schema]
        schema = self.__prepare_schema(schema, norm_range)
        S_vector = np.zeros(int(scale * len(sequence) + 2 * scale))

        for i, AA in enumerate(sequence):
            row = schema[schema['amino_acid'] == AA]
            if len(row) != 1:
                warnings.warn('Ambiguous schema for amino acid {}. Value '
                              'will be set to mean value.'.format(AA),
                              Warning)
                AA_value = np.mean(schema['value'])
            else:
                AA_value = float(row['value'])

            x = np.linspace(norm.ppf(0.01), norm.ppf(0.99), int(3 * scale))
            pdf = norm.pdf(x, scale=sigma) * AA_value
            S_vector[int(i * scale):int((i + 3) * scale)] += pdf

        # Now trim first and last slice, if needed
        if trim_vector:
            S_vector = S_vector[int(scale):int(-scale)]

        # Scale vector to fixed length, if needed
        if vector_length:
            return_vector, offset = [], 0
            step = int(len(S_vector) / vector_length)
            for i in range(vector_length):
                tick = S_vector[offset]
                offset += step
                return_vector.append(tick)
            S_vector = return_vector

        if normalize_vector:
            S_vector = (S_vector - np.min(S_vector)) / (
                    np.max(S_vector) - np.min(S_vector))

        return S_vector

    def add_schema(self, path, amino_col, value_col, key, sep=',', header=None,
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

        :return: None
        """
        csv = pd.read_csv(path, sep=sep, header=header, comment=comment)
        df = pd.DataFrame()
        df['amino_acid'] = csv.iloc[:, amino_col]
        df['value'] = csv.iloc[:, value_col]
        self.schemas[key] = df
        return None

    def get_schemas(self):
        """
        Return list of valid schemas to use, including manually added schemas.
        :return: list
        """
        return [x for x in self.schemas]

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ecnet/utils/data_utils.py
# v.3.0.1
# Developed in 2019 by Travis Kessler <travis.j.kessler@gmail.com>
#
# Contains functions/classes for loading data, saving data, saving results
#

# Stdlib imports
from csv import reader, writer, QUOTE_ALL
from random import sample

# 3rd party imports
from numpy import asarray

# ECNet imports
from ecnet.utils.logging import logger


class DataPoint:

    def __init__(self):
        '''DataPoint object: houses row in CSV database, containing ID, set
        assignment, strings, groups, targets and inputs
        '''

        self.id = None
        self.assignment = None
        self.strings = []
        self.groups = []
        self.targets = []
        self.inputs = []


class PackagedData:

    def __init__(self):
        '''PackagedData object: contains lists of input and target data for data
        set assignments
        '''

        self.learn_x = []
        self.learn_y = []
        self.valid_x = []
        self.valid_y = []
        self.test_x = []
        self.test_y = []


class DataFrame:

    def __init__(self, filename):
        '''DataFrame object: handles data importing, set splitting, shuffling,
        packaging

        Args:
            filename (str): path to ECNet-formatted CSV database
        '''

        if '.csv' not in filename:
            filename += '.csv'
        try:
            with open(filename, newline='') as file:
                data_raw = list(reader(file))
        except FileNotFoundError:
            raise Exception('CSV database not found: {}'.format(filename))

        self._filename = filename

        self.data_points = []
        for point in range(2, len([sublist[0] for sublist in data_raw])):
            new_point = DataPoint()
            new_point.id = [sublist[0] for sublist in data_raw][point]
            for header in range(len(data_raw[0])):
                if 'STRING' in data_raw[0][header]:
                    new_point.strings.append(data_raw[point][header])
                elif 'GROUP' in data_raw[0][header]:
                    new_point.groups.append(data_raw[point][header])
                elif 'TARGET' in data_raw[0][header]:
                    new_point.targets.append(data_raw[point][header])
                elif 'INPUT' in data_raw[0][header]:
                    new_point.inputs.append(data_raw[point][header])
                elif 'ASSIGNMENT' in data_raw[0][header]:
                    new_point.assignment = data_raw[point][header]
                elif 'DATAID' in data_raw[0][header]:
                    new_point.id = data_raw[point][header]
            self.data_points.append(new_point)

        logger.log('debug', 'Found {} data entries'.format(
                   len(self.data_points)), call_loc='DF')

        self.string_names = []
        self.group_names = []
        self.target_names = []
        self.input_names = []
        for header in range(len(data_raw[0])):
            if 'STRING' in data_raw[0][header]:
                self.string_names.append(data_raw[1][header])
            if 'GROUP' in data_raw[0][header]:
                self.group_names.append(data_raw[1][header])
            if 'TARGET' in data_raw[0][header]:
                self.target_names.append(data_raw[1][header])
            if 'INPUT' in data_raw[0][header]:
                self.input_names.append(data_raw[1][header])
        self.num_strings = len(self.string_names)
        self.num_groups = len(self.group_names)
        self.num_targets = len(self.target_names)
        self.num_inputs = len(self.input_names)
        logger.log('debug', 'Input parameters/entry: {}'.format(
                   self.num_inputs), call_loc='DF')
        logger.log('debug', 'Target values/entry: {}'.format(self.num_targets),
                   call_loc='DF')

    def __len__(self):
        '''DataFrame length == number of DataPoints
        '''

        return len(self.data_points)

    def create_sets(self, random=False, split=None):
        '''Creates learning, validation and test sets

        Args:
            random (bool): if True, use random assignments for learn, validate,
                test sets
            split (list): [learn%, valid%, test%] if random == True
        '''

        self.learn_set = []
        self.valid_set = []
        self.test_set = []

        if random is True:
            logger.log('debug', 'Assigning entries to random sets',
                       call_loc='DF')
            rand_index = sample(range(len(self)), len(self))
            split_locs = [
                int(len(rand_index) * split[0]),
                int(len(rand_index) * (split[0] + split[1])),
            ]
            learn_index = rand_index[0: split_locs[0]]
            valid_index = rand_index[split_locs[0]: split_locs[1]]
            test_index = rand_index[split_locs[1]:]
            for idx in learn_index:
                self.data_points[idx].assignment = 'L'
                self.learn_set.append(self.data_points[idx])
            for idx in valid_index:
                self.data_points[idx].assignment = 'V'
                self.valid_set.append(self.data_points[idx])
            for idx in test_index:
                self.data_points[idx].assignment = 'T'
                self.test_set.append(self.data_points[idx])

        elif random is False:
            logger.log('debug', 'Assigning entries to explicit sets',
                       call_loc='DF')
            for point in self.data_points:
                if point.assignment == 'L':
                    self.learn_set.append(point)
                elif point.assignment == 'V':
                    self.valid_set.append(point)
                elif point.assignment == 'T':
                    self.test_set.append(point)

        else:
            raise ValueError('Unknown random boolean: {}'.format(random))

        logger.log('debug', 'Number of entries in learn set: {}'.format(
                   len(self.learn_set)), call_loc='DF')
        logger.log('debug', 'Number of entries in validation set: {}'.format(
                   len(self.valid_set)), call_loc='DF')
        logger.log('debug', 'Number of entries in test set: {}'.format(
                   len(self.test_set)), call_loc='DF')

    def create_sorted_sets(self, sort_string, split=[0.65, 0.25, 0.1]):
        '''Creates random learn, validate and test sets, ensuring data points with
        the supplied sort string are split proportionally between the sets

        Args:
            sort_string (str): database STRING value used to sort data points
            split (list): [learn%, valid%, test%] for set assignments
        '''

        logger.log('debug', 'Creating sorted sets using {} STRING'.format(
                   sort_string), call_loc='DF')

        try:
            string_idx = self.string_names.index(sort_string)
        except ValueError:
            raise Exception('{} not found in STRING names'.format(sort_string))
        self.data_points.sort(key=lambda x: x.strings[string_idx])

        string_vals = []
        string_groups = []

        for point in self.data_points:
            if point.strings[string_idx] not in string_vals:
                string_vals.append(point.strings[string_idx])
                string_groups.append([point])
            else:
                string_groups[-1].append(point)

        self.learn_set = []
        self.valid_set = []
        self.test_set = []

        for group in string_groups:
            split_locs = [
                int(len(group) * split[0]),
                int(len(group) * (split[0] + split[1])),
            ]
            for point in group[0: split_locs[0]]:
                point.assignment = 'L'
                self.learn_set.append(point)
            for point in group[split_locs[0]: split_locs[1]]:
                point.assignment = 'V'
                self.valid_set.append(point)
            for point in group[split_locs[1]:]:
                point.assignment = 'T'
                self.test_set.append(point)

        logger.log('debug', 'Number of entries in learn set: {}'.format(
                   len(self.learn_set)), call_loc='DF')
        logger.log('debug', 'Number of entries in validation set: {}'.format(
                   len(self.valid_set)), call_loc='DF')
        logger.log('debug', 'Number of entries in test set: {}'.format(
                   len(self.test_set)), call_loc='DF')

    def normalize(self):
        '''Normalize input data (min-max, between 0 and 1)'''

        for inp in range(len(self.data_points[0].inputs)):
            vals = [float(pt.inputs[inp]) for pt in self.data_points]
            v_min = min(vals)
            v_max = max(vals)
            for pt in self.data_points:
                if v_max - v_min == 0:
                    pt.inputs[inp] = 0
                else:
                    pt.inputs[inp] = (float(pt.inputs[inp]) - v_min) /\
                        (v_max - v_min)

    def shuffle(self, sets='all', split=[0.7, 0.2, 0.1]):
        '''Shuffles learning, validation and test sets or learning and
        validation sets

        Args:
            sets (str): 'all' or 'train' (learning + validation)
            split (list): [learn%, valid%, test%] used for new assignments
        '''

        logger.log('debug', 'Shuffling {} sets'.format(sets), call_loc='DF')

        if sets == 'all':
            self.create_sets(random=True, split=split)
        elif sets == 'train':
            lv_set = []
            lv_set.extend([p for p in self.learn_set])
            lv_set.extend([p for p in self.valid_set])
            rand_index = sample(
                range(len(self.learn_set) + len(self.valid_set)),
                (len(self.learn_set) + len(self.valid_set))
            )
            self.learn_set = lv_set[
                0: int(len(rand_index) * (split[0] / (1 - split[2]))) + 1
            ]
            self.valid_set = lv_set[
                int(len(rand_index) * (split[0] / (1 - split[2]))) + 1:
            ]
            logger.log('debug', 'Number of entries in learn set: {}'.format(
                   len(self.learn_set)), call_loc='DF')
            logger.log('debug', 'Number of entries in validation set: {}'
                       .format(len(self.valid_set)), call_loc='DF')
            logger.log('debug', 'Number of entries in test set: {}'.format(
                    len(self.test_set)), call_loc='DF')
        else:
            raise ValueError('Invalid sets argument: {}'.format(sets))

    def package_sets(self):
        '''Packages learn, validate and test sets for model hand-off

        Returns:
            PackagedData: object containing learn, validate and test inputs
                and targets
        '''

        pd = PackagedData()
        for point in self.learn_set:
            pd.learn_x.append(asarray(point.inputs).astype('float32'))
            pd.learn_y.append(asarray(point.targets).astype('float32'))
        for point in self.valid_set:
            pd.valid_x.append(asarray(point.inputs).astype('float32'))
            pd.valid_y.append(asarray(point.targets).astype('float32'))
        for point in self.test_set:
            pd.test_x.append(asarray(point.inputs).astype('float32'))
            pd.test_y.append(asarray(point.targets).astype('float32'))

        pd.learn_x = asarray(pd.learn_x)
        pd.learn_y = asarray(pd.learn_y)
        pd.valid_x = asarray(pd.valid_x)
        pd.valid_y = asarray(pd.valid_y)
        pd.test_x = asarray(pd.test_x)
        pd.test_y = asarray(pd.test_y)
        return pd

    def set_inputs(self, inputs):
        '''Removes all input variables except those supplied

        Args:
            inputs (list): input variable names, str
        '''

        logger.log('debug', 'Setting input parameters to {}'.format(inputs),
                   call_loc='DF')

        idxs = []
        for input in inputs:
            for cidx, current_input in enumerate(self.input_names):
                if input == current_input:
                    idxs.append(cidx)
        for point in self.data_points:
            new_inputs = []
            for i in idxs:
                new_inputs.append(point.inputs[i])
            point.inputs = new_inputs
        self.input_names = inputs
        self.num_inputs = len(inputs)
        self.create_sets()

    def save(self, filename):
        '''Saves the current state of the DataFrame to a new CSV database

        Args:
            filename (str): path to location where database is saved
        '''

        if '.csv' not in filename:
            filename += '.csv'

        rows = []
        type_row = ['DATAID', 'ASSIGNMENT']
        type_row.extend(['STRING' for _ in range(self.num_strings)])
        type_row.extend(['GROUP' for _ in range(self.num_groups)])
        type_row.extend(['TARGET' for _ in range(self.num_targets)])
        type_row.extend(['INPUT' for _ in range(self.num_inputs)])
        rows.append(type_row)

        title_row = ['DATAID', 'ASSIGNMENT']
        title_row.extend(self.string_names)
        title_row.extend(self.group_names)
        title_row.extend(self.target_names)
        title_row.extend(self.input_names)
        rows.append(title_row)

        data_rows = []
        for point in self.data_points:
            data_row = [point.id, point.assignment]
            data_row.extend(point.strings)
            data_row.extend(point.groups)
            data_row.extend(point.targets)
            data_row.extend(point.inputs)
            data_rows.append(data_row)
        rows.extend(sorted(data_rows, key=lambda x: x[0]))

        with open(filename, 'w') as csv_file:
            wr = writer(csv_file, quoting=QUOTE_ALL, lineterminator='\n')
            for row in rows:
                wr.writerow(row)

        logger.log('debug', 'DataFrame saved to {}'.format(filename),
                   call_loc='DF')


def save_results(results, dset, df, filename):
    '''Saves results obtained from ecnet.Server.use_model()

    Args:
        results (list): list of lists, where sublists are predicted data for
            each data point
        dset (str): 'learn', 'valid', 'train', 'test', None (all)
        df (DataFrame): data_utils.DataFrame object used for results file
            formatting
        filename (str): path to save location for results
    '''

    if '.csv' not in filename:
        filename += '.csv'

    rows = []
    type_row = ['DATAID', 'ASSIGNMENT']
    type_row.extend(['STRING' for _ in range(df.num_strings)])
    type_row.extend(['GROUP' for _ in range(df.num_groups)])
    type_row.extend(['TARGET' for _ in range(df.num_targets)])
    type_row.extend(['RESULT' for _ in range(len(results[0]))])
    rows.append(type_row)

    title_row = ['DATAID', 'ASSIGNMENT']
    title_row.extend(df.string_names)
    title_row.extend(df.group_names)
    title_row.extend(df.target_names)
    title_row.append('Result')
    rows.append(title_row)

    output_points = []
    if dset == 'train':
        output_points.extend(df.learn_set)
        output_points.extend(df.valid_set)
    elif dset == 'learn':
        output_points.extend(df.learn_set)
    elif dset == 'valid':
        output_points.extend(df.valid_set)
    elif dset == 'test':
        output_points.extend(df.test_set)
    elif dset is None:
        output_points.extend(df.learn_set)
        output_points.extend(df.valid_set)
        output_points.extend(df.test_set)
    else:
        raise ValueError('Unknown dset argument: {}'.format(dset))

    data_rows = []
    for idx, point in enumerate(output_points):
        data_row = [point.id, point.assignment]
        data_row.extend(point.strings)
        data_row.extend(point.groups)
        data_row.extend(point.targets)
        data_row.extend(results[idx])
        # if df.num_targets == 1:
        #     data_row.extend(r[idx][0] for r in results)
        # else:
        #     data_row.extend(r[idx] for r in results)
        data_rows.append(data_row)
    rows.extend(sorted(data_rows, key=lambda x: x[0]))

    with open(filename, 'w') as csv_file:
        wr = writer(csv_file, quoting=QUOTE_ALL, lineterminator='\n')
        for row in rows:
            wr.writerow(row)

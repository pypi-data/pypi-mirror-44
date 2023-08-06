#!/usr/bin/env python
from __future__ import print_function

import os
import sys
import traceback
import copy
import csv
import random
import math
from datetime import date, timedelta
from pprint import pprint
from decimal import Decimal
from collections import defaultdict

import numpy as np
from pyexcel_ods import get_data
from weka.arff import ArffFile, Nom, Num, Str, Date, MISSING
from weka.classifiers import EnsembleClassifier
from dateutil.parser import parse


class SkipRow(Exception):
    pass


BASE_DIR = os.path.split(os.path.realpath(__file__))[0]

NUMERIC = 'numeric'
DATE = 'date'

MN = 'mn_' # morning
NO = 'no_' # noon
EV = 'ev_' # evening
MONTHLY = '_monthly'
OTHERS = 'others'
# MANAGE = 'manage'

NA_CHANGE = ''
RELATIVE_CHANGE = 'rel'
ABSOLUTE_CHANGE = 'abs'
CHANGE_TYPES = (NA_CHANGE, RELATIVE_CHANGE, ABSOLUTE_CHANGE)

# The minimum number of days of data needed before a prediction can be made.
MIN_DAYS = 30

HEADER_ROW_INDEX = 0
TYPE_ROW_INDEX = 1
RANGE_ROW_INDEX = 2
# CONTROLLABLE_ROW_INDEX = 3
LEARN_ROW_INDEX = 3 # These columns are given to the classifiers to learn.
PREDICT_ROW_INDEX = 4 # These columns are individually looked at to predict an optimal change.
CHANGE_ROW_INDEX = 5 # 0=none, 1=relative change recommendation, 2=absolute value recommendation
DATA_ROW_INDEX = 6
TOLERANCE = 1.0
#CLASS_ATTR_NAME = 'score'
#CLASS_ATTR_NAME = 'score_change'
CLASS_ATTR_NAME = 'score_next'
DEFAULT_SCORE_FIELD_NAME = 'score'
DEFAULT_CLASSIFIER_FN = '/tmp/%s-last-classifier.pkl.gz'
DEFAULT_RELATION = '%s-training'


def attempt_cast_str_to_numeric(value):
    try:
        return float(value)
    except ValueError:
        return value


class Optimizer:
    
    def __init__(self, fn, **kwargs):

        if not fn.startswith('/'):
            fn = os.path.join(BASE_DIR, fn)
        assert os.path.isfile(fn), 'File %s does not exist.' % fn
        self.fn = fn
        self.fqfn_base = os.path.splitext(os.path.abspath(fn))[0]
        self.fn_base = os.path.splitext(os.path.split(fn)[0])[0]

        self.__dict__.update(kwargs)
        self.score_field_name = self.__dict__.get('score_field_name') or DEFAULT_SCORE_FIELD_NAME
        self.only_attribute = self.__dict__.get('only_attribute')
        self.stop_on_error = self.__dict__.get('stop_on_error') or False
        self.no_train = self.__dict__.get('no_train') or False
        self.all_classifiers = self.__dict__.get('all_classifiers') or False
        self.calculate_pcc = self.__dict__.get('calculate_pcc') or False
        self.yes = self.__dict__.get('yes', None)
        self.classifier_fn = self.__dict__.get('classifier_fn', DEFAULT_CLASSIFIER_FN) % self.fn_base
        self.relation = self.__dict__.get('relation', DEFAULT_RELATION) % self.fn_base

    def analyze(self, save=True):

        self.score_field_name = self.score_field_name or DEFAULT_SCORE_FIELD_NAME

        print('Retrieving data...')
        sys.stdout.flush()
        data = get_data(self.fn)['data']

        # Validate header rows.
        field_to_day_count = {} # {name: number of days of data}
        column_names = data[HEADER_ROW_INDEX]
        column_types = data[TYPE_ROW_INDEX]
        column_types_dict = dict(zip(column_names, column_types))
        column_ranges = dict(zip(column_names, data[RANGE_ROW_INDEX])) # min,max,step
        for _name in column_ranges.keys():
            if _name not in ('date') and column_ranges[_name]:
                column_ranges[_name] = list(map(float, column_ranges[_name].split(',')))
            else:
                column_ranges[_name] = None

        column_nominals = self.column_nominals = {} # {name: set(nominals)}
        assert len(column_names) == len(column_types)
        for column_name, ct in zip(column_names, column_types):
            assert ct in (DATE, NUMERIC) or (ct[0] == '{' and ct[-1] == '}'), 'Invalid type: %s' % ct
            if ct[0] == '{':
                column_nominals[column_name] = set(ct[1:-1].split(','))

        column_learnables = self.column_learnables = {}
        for _a, _b in zip(column_names, data[LEARN_ROW_INDEX]):
            if _a == DATE:
                column_learnables[_a] = 0
                continue
            try:
                column_learnables[_a] = int(_b)
            except Exception as exc:
                raise Exception('Error checking controllable for column %s: %s' % (_a, exc))
        print('column_learnables:', column_learnables)

        column_predictables = self.column_predictables = {}
        for _a, _b in zip(column_names, data[PREDICT_ROW_INDEX]):
            if _a == DATE:
                column_predictables[_a] = 0
                continue
            try:
                column_predictables[_a] = int(_b)
            except Exception as exc:
                raise Exception('Error checking predictable for column %s: %s' % (_a, exc))
        print('column_predictables:', column_predictables)

        column_changeables = self.column_changeables = {}
        for _a, _b in zip(column_names, data[CHANGE_ROW_INDEX]):
            if _a == DATE:
                column_changeables[_a] = NA_CHANGE
                continue
            try:
                assert _b in CHANGE_TYPES, 'Invalid change type for column %s: %s' % (_a, _b)
                column_changeables[_a] = _b
            except Exception as exc:
                raise Exception('Error checking changeable for column %s: %s' % (_a, exc))
        print('column_changeables:', column_changeables)

        # Load data rows and convert to ARFF format.
        row_errors = {} # {row_count: error}
        data = data[DATA_ROW_INDEX:]
        arff = ArffFile(relation=self.relation)
        arff.class_attr_name = CLASS_ATTR_NAME
        arff.relation = self.relation # 'optimizer-training'
        row_count = 0
        best_day = -1e999999999999, None # (score, data)
        best_date = -1e999999999999, None
        last_full_day = date.min, None # (date, data)
        date_to_score = {} # {date: score}
        # date_to_row = {} # {date: row}
        column_values = defaultdict(set)
        new_rows = []
        for row in data:
            row_count += 1
            try:
                if not row:
                    continue
                #print('row:', row_count, row)
                assert len(row) == len(column_names), "Row %i has length %i but there are %i column headers." % (row_count, len(row), len(column_names))
                assert len(row) == len(column_types)
                old_row = dict(zip(column_names, row))
                new_row = {}
                for row_value, column_name, ct in zip(row, column_names, column_types):

                    # Ignore impartially filled in row for the current day.
                    if column_name.startswith('next_day') or column_name.startswith('subscore'):
                        if row_value == '':
                            raise SkipRow
                        # Remove next_day_* attributes, since these are only used for calculating the score, not predicting it.
                        continue

                    if ct == DATE:
                        if row_count == 1 and not isinstance(row_value, date):
                            # Ignore invalid date on first row, since we purposefully leave this blank.
                            print('Warning: Invalid date "%s" on row %s.' % (row_value, row_count), file=sys.stderr)
                            raise SkipRow
                        if isinstance(row_value, str):
                            # If the cell data wasn't entered correctly, the date value might be stored as a string.
                            _row_value = parse(row_value)
                            if _row_value:
                                row_value = _row_value.date()
                                old_row[column_name] = row_value
                        assert isinstance(row_value, date), 'Invalid date "%s" on row %s.' % (row_value, row_count)
                        continue
                    elif ct == NUMERIC:
                        if row_value != '':
                            row_value = attempt_cast_str_to_numeric(row_value)
                            assert isinstance(row_value, (int, bool, float)), 'Invalid numeric value "%s" of type "%s" in column "%s" of row %i.' \
                                % (row_value, type(row_value), column_name, row_count)
                            new_row[column_name] = Num(row_value)
                        else:
                            # Otherwise, ignore empty cell values, which means the data is missing.
                            continue
                    elif ct[0] == '{':
                        if row_value != '':
                            assert str(row_value) in column_nominals[column_name], 'Invalid nominal value "%s" for column "%s". Legal values: %s' \
                                % (row_value, column_name, ', '.join(sorted(map(str, column_nominals[column_name]))))
                            new_row[column_name] = Nom(str(row_value))
                        else:
                            # Otherwise, ignore empty cell values, which means the data is missing.
                            continue
                    else:
                        raise NotImplementedError('Unknown type/column: %s/%s' % (ct, column_name))

                    column_values[column_name].add(new_row[column_name])
                    field_to_day_count.setdefault(column_name, 0)
                    field_to_day_count[column_name] += new_row[column_name] != '' and new_row[column_name] is not None

                new_row['date'] = old_row['date']
                # date_to_row[old_row['date']] = new_row
                assert isinstance(old_row['date'], date)
                date_to_score[old_row['date']] = new_row[self.score_field_name]
                print("new_row:'%s':value: %s" % (self.score_field_name, new_row[self.score_field_name].value))
                best_day = max(best_day, (new_row[self.score_field_name].value, new_row), key=lambda o: o[0])
                best_date = max(best_date, (new_row[self.score_field_name].value, old_row['date']), key=lambda o: o[0])
                last_full_day = max(last_full_day, (old_row['date'], new_row), key=lambda o: o[0])
                # date_to_row[new_row['date']] = new_row
                
                #arff.append(new_row)
                new_rows.append(new_row)
            except SkipRow:
                pass
            except Exception as exc:
                traceback.print_exc()
                row_errors[row_count] = traceback.format_exc()
                if self.stop_on_error:
                    raise

        # Re-score rows to calculate score change per day.
        # Note, we assume the features on the previous day are what predict the score on the next day,
        # so for each row, we discard its score and replace it with the score for the next day.
        # If not next day score is available, we skip that row entirely.
        assert new_rows, "No data!"
        modified_rows = [] # Rows containing a differential score.
        for new_row in new_rows:
            current_date = new_row['date']
            current_score = new_row[self.score_field_name]
            next_date = current_date + timedelta(days=1)
            assert isinstance(next_date, date)
            if next_date in date_to_score:
                next_score = date_to_score[next_date]
                print('current_date:', current_date)
                print('current_score.value:', current_score.value)
                print('next_date:', next_date)
                print('next_score.value:', next_score.value)
                assert current_date < next_date
                
                # CS 2018.9.26 Disabled because I think this may be stalling, when it doesn't see an incremental improvement.
                # Reverting to total score prediction.
                #
                # The prediction target is the change in day to day score, with the intent being to maximize this increase.
                # score_change = Num(next_score.value - current_score.value)
                # print('score_change:', score_change)
                # new_row[CLASS_ATTR_NAME] = score_change

                # The prediction target is the next day's score, with the intent being to maximize this score.
                new_row[CLASS_ATTR_NAME] = next_score

                # Exclude columns from the dataset that are marked as not being fields that should be fed to the learning algorithms.
                for _column, _controllable in column_learnables.items():
                    if not _controllable and _column in new_row:
                        del new_row[_column]

                print('new_row:', new_row)
                sys.stdout.flush()
                modified_rows.append(new_row)
                arff.append(new_row)

        if self.calculate_pcc:
            # https://en.wikipedia.org/wiki/Pearson_correlation_coefficient
            pcc_rows = []
            with open('pcc.csv', 'w') as fout:
                fieldnames = ['name', 'samples', 'pcc', 'utility']
                writer = csv.DictWriter(fout, fieldnames=fieldnames)
                writer.writerow(dict(zip(fieldnames, fieldnames)))
                for target_attr in column_names:
                    if column_types_dict[target_attr] != NUMERIC or not column_predictables.get(target_attr) or target_attr == CLASS_ATTR_NAME:
                        continue
                    _x = []
                    _y = []
                    for new_row in modified_rows:
                        try:
                            xv = float(new_row[CLASS_ATTR_NAME].value)
                            yv = float(new_row[target_attr].value)
                            _x.append(xv)
                            _y.append(yv)
                        except (KeyError, AttributeError):
                            continue
                    x = np.array(_x).astype(np.float32)
                    y = np.array(_y).astype(np.float32)
                    # print('x:', x)
                    pcc = np.corrcoef(x, y)[0, 1]
                    print('Pearson correlation for %s: %s' % (target_attr, pcc))
                    samples = len(_x)
                    if math.isnan(pcc):
                        continue
                    pcc_rows.append(dict(name=target_attr, pcc=pcc, samples=samples, utility=samples*pcc))
                pcc_rows.sort(key=lambda o: o['utility'])
                for pcc_row in pcc_rows:
                    writer.writerow(pcc_row)
            return

        # Cleanup training arff.
        print('attributes:', sorted(arff.attributes))
        arff.alphabetize_attributes()
        assert len(arff), 'Empty arff!' # pylint: disable=len-as-condition
        #print(last_full_day)
        # sys.exit()

        # Report any processing errors on each row.
        if row_errors:
            print('='*80)
            print('Row Errors: %s' % len(row_errors))
            for row_count in sorted(row_errors):
                print('Row %i:' % row_count)
                print(row_errors[row_count])
            print('='*80)
        else:
            print('No row errors.')
            
        # Ensure the base arff file has all nominals values, even if they weren't used.
        for name in column_nominals:
            if name in arff.attribute_data:
                arff.attribute_data[name].update(column_nominals[name])

        training_fn = os.path.join(BASE_DIR, self.fqfn_base + '.arff')
        print('training_fn:', training_fn)
        
        print('Writing arff...')
        with open(training_fn, 'w') as fout:
            arff.write(fout)
        print('Arff written!')

        # Train all Weka regressors on arff training file.
        if self.all_classifiers:
            classes = None
        else:
            classes = [
                'weka.classifiers.lazy.IBk',
                'weka.classifiers.lazy.KStar',
                'weka.classifiers.functions.MultilayerPerceptron',
            ]
        if self.no_train:
            assert os.path.isfile(self.classifier_fn), \
                'If training is disabled, then a classifier file must exist to re-use, but %s does not exist.' % self.classifier_fn
            print('Loading classifier from file %s...' % self.classifier_fn)
            classifier = EnsembleClassifier.load(self.classifier_fn)
            print('Classifier loaded.')
        else:
            classifier = EnsembleClassifier(classes=classes)
            classifier.train(training_data=training_fn, verbose=self.all_classifiers)
        #print('='*80)
        #print('errors:')
        #classifier.get_errors()
        print('='*80)
        print('best:')
        classifier.get_training_best()
        print('='*80)
        print('coverage: %.02f%%' % (classifier.get_training_coverage()*100))
        if self.all_classifiers:
            print('Aborting query with all classifiers.')
            sys.exit(0)

        # Find day with best score.
        print('='*80)
        best_day_score, best_day_data = best_day
        print('best_day_score:', best_day_score)
        print('best_day_data:')
        pprint(best_day_data, indent=4)
        print('best date:', best_date)
        print('last full day:', last_full_day)
        last_full_day_date = last_full_day[0]
        if self.yes is None and abs((last_full_day_date - date.today()).days) > 1:
            if input('Last full day is %s, which is over 1 day ago. Continue? [yn]:' % last_full_day_date).lower()[0] != 'y':
                sys.exit(1)

        # Generate query sets for each variable metric. Base them on the best day, and incrementally change them from there, to avoid drastic changes
        # which may have harmful medical side-effects.
        print('='*80)
        print('ranges:')
        for _name, _range in sorted(column_ranges.items(), key=lambda o: o[0]):
            #print(_name, ', '.join('%s=%s' for _k, _v in sorted(_range.items())))
            print(_name, _range)
        # pprint(column_ranges, indent=4)
        #_, best_data = best_day
        _, best_data = last_full_day
        queries = [] # [(name, description, data)]
        query_name_list = sorted(column_values)
        if self.only_attribute:
            query_name_list = [self.only_attribute]
        for name in query_name_list:

            if name == CLASS_ATTR_NAME:
                continue

            if name in column_predictables and not column_predictables[name]:
                continue
                
            print('Query attribute name:', name)
            if isinstance(list(column_values[name])[0], Nom):
                print('Nominal attribute.')
                # Calculate changes for a nominal column.
                #for direction in column_values[name]:
                #continue
                for direction in column_nominals[name]:
                    query_value = direction = Nom(direction)
                    new_query = copy.deepcopy(best_data)
                    new_query[name] = direction
                    best_value = best_data.get(name, sorted(column_nominals[name])[0])
                    if best_value != query_value:
                        description = '%s: change from %s -> %s' % (name, best_value, query_value)
                        print('\t%s' % description)
                        queries.append((name, description, new_query))
            else:
                # Calculate changes for a numeric column.
                print('Numeric attribute.')
                if not column_ranges.get(name):
                    print('Has no column ranges. Skipping.')
                    continue
                _min, _max, _step = column_ranges[name]
                assert _min < _max, 'Invalid min/max!'
                if self.only_attribute or name in ('bed'):
                    # Check every possible value.
                    _value = _min
                    while _value <= _max:
                        print('Checking query %s=%s.' % (name, _value))
                        
                        new_query = copy.deepcopy(best_data)
                        
                        # If our best day starting point is missing this metric, then use the mean.
                        _mean = None
                        if name not in new_query:
                            new_query[name] = sum(column_values[name], Num(0.0)) / len(column_values[name])
                            _mean = copy.deepcopy(new_query[name])
                        
                        # Skip the hold case.
                        if _value == best_data.get(name, _mean):
                            print('Hold case. Skipping.')
                            continue
                        
                        new_query[name].value = _value
                        if best_data.get(name, _mean) != new_query[name]:
                            print('\tallowable range min/max/step:', _min, _max, _step)
                            description = '%s: change from %s -> %s' % (name, best_data.get(name, _mean), new_query[name].value)
                            print('\t%s' % description)
                            assert _min <= new_query[name].value <= _max
                            queries.append((name, description, new_query))
                            
                        _value += _step
                else:
                    # Check only a relative change.
                    for direction in [-1, 1]:
                        new_query = copy.deepcopy(best_data)
                        
                        # If our best day starting point is missing this metric, then use the mean.
                        _mean = None
                        if name not in new_query:
                            new_query[name] = sum(column_values[name], Num(0.0)) / len(column_values[name])
                            _mean = copy.deepcopy(new_query[name])
                        
                        new_query[name].value += direction * _step
                        new_query[name].value = min(new_query[name].value, _max)
                        new_query[name].value = max(new_query[name].value, _min)
                        if best_data.get(name, _mean) != new_query[name]:
                            print('\tallowable range min/max/step:', _min, _max, _step)
                            description = '%s: change from %s -> %s' % (name, best_data.get(name, _mean), new_query[name])
                            print('\t%s' % description)
                            queries.append((name, description, new_query))
            
            # Re-evaluate the current state.
            new_query = copy.deepcopy(best_data)
            description = '%s: hold at %s' % (name, best_data.get(name, _mean))
            queries.append((name, description, new_query))

        if save:
            print('Saving classifier...')
            classifier.save(self.classifier_fn)
            print('Classifier saved to %s.' % self.classifier_fn)

        # Score each query.
        print('='*80)
        total = len(queries)
        i = 0
        final_recommendations = [] # [(predicted change, old score, new score, description, name)]
        final_scores = {} # {name: (best predicted change, description)}
        for name, description, query_data in queries:
            i += 1
            print('Running query %i of %i...' % (i, total))
            new_arff = arff.copy(schema_only=True)
            new_arff.relation = 'optimizer-query'
            query_data[CLASS_ATTR_NAME] = MISSING

            for _column, _controllable in column_learnables.items():
                if not _controllable and _column in query_data:
                    del query_data[_column]
                
            print('query_data:', sorted(query_data))
            new_arff.append(query_data)
            print('$'*80)
            print('predicting...')
            predictions = list(classifier.predict(new_arff, tolerance=TOLERANCE, verbose=1, cleanup=0))
            print('\tdesc:', description)
            print('\tpredictions:', predictions)
            #score_change = predictions[0].predicted - Decimal(str(old_score.value))
            score_change = predictions[0].predicted
            #print('\told score: %.02f' % old_score.value)
            #print('\tnew score: %.02f' % predictions[0].predicted)
            print('\tscore change: %.02f' % score_change)
            #final_recommendations.append((score_change, old_score.value, predictions[0].predicted, description, name))
            final_recommendations.append((score_change, 0, 0, description, name))
            final_scores.setdefault(name, (-1e999999999999, None))
            final_scores[name] = max(final_scores[name], (score_change, description))

        # Show top predictors.
        print('='*80)
        print('best predictors:')
        best_names = classifier.get_best_predictors(tolerance=TOLERANCE, verbose=True)
        print(best_names)
        seed_date = last_full_day[0]

        # Show final top recommendations by attribute.
        print('='*80)
        print('recommendations by attribute based on date: %s' % seed_date)
        final_recommendations.sort(key=lambda o: (o[4], o[0]))
        i = 0
        digits = len(str(len(final_recommendations)))
        for change, _old_score, _new_score, description, name in final_recommendations:
            i += 1
            best_score_change, best_description = final_scores[name]
            if description != best_description:
                continue
            print(('\t%0'+str(digits)+'i %s => %.06f') % (i, description, change))

        # Show final top recommendations by best change.
        final_recommendations.sort()

        print('='*80)
        print('Evening recommendations by change based on date: %s' % seed_date)
        print_recommendation(final_recommendations, final_scores, typ=EV)

        print('='*80)
        print('Morning recommendations by change based on date: %s' % seed_date)
        print_recommendation(final_recommendations, final_scores, typ=MN)

        print('='*80)
        print('Other recommendations by change based on date: %s' % seed_date)
        print_recommendation(final_recommendations, final_scores, typ=OTHERS)

        return final_recommendations, final_scores


def print_recommendation(recs, scores, typ=None):
    i = len(recs) + 1
    digits = len(str(len(recs)))
    for change, _old_score, _new_score, description, name in recs:
        i -= 1
        if typ:
            if typ == EV and EV not in name:
                continue
            elif typ == MN and MN not in name:
                continue
            elif typ == OTHERS and (EV in name or MN in name):
                continue
        best_score_change, best_description = scores[name]
        if description != best_description:
            continue
        print(('\t%0'+str(digits)+'i %s => %.06f') % (i, description, change))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Analyzes daily routine features to optimize your routine.')
    parser.add_argument('fn', help='Filename of ODS file containing data.')
    parser.add_argument('--only-attribute', default=None, help='If given, only predicts the effect of this one attribute. Otherwise looks at all attributes.')
    parser.add_argument('--stop-on-error', action='store_true', default=False, help='If given, halts at first error. Otherwise shows a warning and continues.')
    parser.add_argument('--no-train', action='store_true', default=False, help='If given, skips training and re-uses last trained classifier.')
    parser.add_argument('--score-field-name', default=None,
        help='The name of the field containing the score to maximize. Default is "%s".' % DEFAULT_SCORE_FIELD_NAME)
    parser.add_argument('--all-classifiers', action='store_true', default=False,
        help='If given, trains all classifiers, even the crappy ones. Otherwise, only uses the known best.')
    parser.add_argument('--calculate-pcc', action='store_true', default=False,
        help='If given, calculates the Pearson correlation coefficient for all attributes.')
    parser.add_argument('--yes', default=None, action='store_true',
        help='Enables non-interactive mode and assumes yes for any interactive yes/no prompts.')
    args = parser.parse_args()
    o = Optimizer(**args.__dict__)
    o.analyze()

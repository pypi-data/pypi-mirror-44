'''
Module that contains the various data types:

1. Target -- Mutable data store for a single Target value i.e. one training 
   example.
2. TargetCollection -- Mutable data store for Target data types.  i.e. A 
   data store that contains multiple Target instances.
'''

from collections.abc import MutableMapping
from collections import OrderedDict, defaultdict
import copy
import json
from pathlib import Path
import random as rand
from typing import List, Callable, Union, Dict, Tuple, Any, Optional, Set
import warnings

import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.model_selection import train_test_split
import seaborn as sns

from bella.tokenisers import whitespace
from bella.stanford_tools import constituency_parse

BELLA_DATASET_DIR: Path = Path.home().joinpath('.Bella', 'Datasets')

class Target(MutableMapping):
    '''
    Mutable data store for a single Target value. This should be used as the
    value for Target information where it contains all data required to be
    classified as Target data for Target based sentiment classification.

    Overrides collections.abs.MutableMapping abstract class.

    Reference on how I created the class:
    http://www.kr41.net/2016/03-23-dont_inherit_python_builtin_dict_type.html
    https://docs.python.org/3/library/collections.abc.html

    Functions changed compared to normal:

    1. __delitem__ -- Will only delete the `target_id` key.
    2. __eq__ -- Two Targets are the same if they either have the same `id` or \
    they have the same values to the minimum keys \
    ['spans', 'text', 'target', 'sentiment']
    3. __setitem__ -- Only allows you to add/modify the `predicted` key which \
    represents the predicted sentiment for the Target instance.
    '''

    def __init__(self, spans, target_id, target, text, sentiment, predicted=None,
                 sentence_id=None, category=None, augmented=None, 
                 transfer_data=None, original_target_id=None, 
                 original_sentence_id=None, epoch_number = set([-1])):
        '''
        :param target: Target that the sentiment is about. e.g. Iphone
        :param sentiment: sentiment of the target.
        :param text: The text context that the target and sentiment is within.
        :param target_id: Unique ID. Has to be Unique within the 
                          TargetCollection if it is put into a TargetCollection.
        :param spans: List of tuples where each tuple is of length 2 where they 
                      contain the exclusive range of an instance of Target word 
                      in the Text context. The reason it is a list if because 
                      the Target word can be mentioned more than once e.g. 
                      `The Iphone was great but the iphone is small`. The first 
                      Int in the tuple has to be less than the second Int.
        :param predicted: If given adds the predicted sentiment value.
        :param sentence_id: Unique ID of the sentence that the target is 
                            within. More than one target can have the same 
                            sentence.
        :param category: In some datasets there is category information where 
                         the target is assigned a category. This comes from 
                         the SemEval 2015 restaurant dataset.
        :param augmented: Whether or not the data comes from an augmented 
                          dataset or has been produced from an augmented 
                          function.
        :param transfer_data: Whether or not the data comes from a transfer 
                              dataset.
        :param original_target_id: If the augmented field is True then the 
                                   original_target_id has to exist, as this 
                                   will inform what the original target 
                                   was used to create this augmented target 
                                   data. 
        :param original_sentence_id: If the data has been augmented in such 
                                     a way that the sentence text has been 
                                     changed then this will store the sentence 
                                     ID that relates to the original text.
        :param epoch_number: The epochs which this target should be sampled
                             from. This is only applicable when using this with 
                             a custom sampler, it allows you to add when you 
                             may want this target to be sampled. It is a 
                             Set of integers as it will allow you to sample the 
                             target more than once.
        :type target: String
        :type sentiment: String or Int (Based on annotation schema)
        :type text: String
        :type target_id: String
        :type spans: list
        :type predicted: Same type as sentiment. Default None (Optional)
        :type sentence_id: String. Default None (Optional)
        :type category: String. Default None (Optional)
        :type augmented: bool. Default None (Optional)
        :type transfer_data: bool. Default None (Optional)
        :type original_target_id: String
        :type original_sentence_id: String
        :type epoch_number: Set of Integers
        :returns: Nothing. Constructor.
        :rtype: None
        '''
        if not isinstance(target_id, str):
            raise TypeError('The target ID has to be of type String and not {}'\
                            .format(type(target_id)))
        if not isinstance(target, str):
            raise TypeError('The target has to be of type String and not {}'\
                            .format(type(target)))
        if not isinstance(text, str):
            raise TypeError('The text has to be of type String and not {}'\
                            .format(type(text)))
        if not isinstance(sentiment, (str, int)):
            raise TypeError('The sentiment has to be of type String or Int and '\
                            'not {}'.format(type(sentiment)))
        if not isinstance(spans, list):
            raise TypeError('The spans has to be of type list and not {}'\
                            .format(type(spans)))
        else:
            if len(spans) < 1:
                raise TypeError('spans has to contain at least one tuple not '\
                                'None')
            else:
                for span in spans:
                    if not isinstance(span, tuple):
                        raise TypeError('Spans has to be a list of tuples not {}'\
                                        .format(type(span)))
                    if len(span) != 2:
                        raise ValueError('Spans must contain tuples of length'\
                                         ' 2 not {}'.format(spans))
                    if not isinstance(span[0], int) or \
                       not isinstance(span[1], int):
                        raise TypeError('spans must be made of tuple containing '\
                                        'two Integers not {}'.format(span))
                    if span[1] <= span[0]:
                        raise ValueError('The first integer in a span must be '\
                                         'less than the second integer {}'\
                                         .format(span))
        temp_dict = dict(spans=spans, target_id=target_id, target=target,
                         text=text, sentiment=sentiment, 
                         epoch_number=epoch_number)
        if sentence_id is not None:
            if not isinstance(sentence_id, str):
                raise TypeError('`sentence_id` has to be a String and not {}'\
                                .format(type(sentence_id)))
            temp_dict['sentence_id'] = sentence_id

        if category is not None:
            temp_dict['category'] = category
        if augmented is not None:
            temp_dict['augmented'] = augmented
            if original_target_id is None:
                aug_data_error = ('Cannot create a Target that is augmented '
                                  'without having the original target_id of the'
                                  ' target data that was augmented to create '
                                  'this target data')
                raise ValueError(aug_data_error)
            
        if original_target_id is not None:
            temp_dict['original_target_id'] = original_target_id
        if original_sentence_id is not None:
            if augmented != True:
                raise ValueError('Cannot add original sentence id to a Target'
                                 ' that has not been augmented.')
            temp_dict['original_sentence_id'] = original_sentence_id
        if transfer_data is not None:
            temp_dict['transfer_data'] = transfer_data

        self._storage = temp_dict
        if predicted is not None:
            self['predicted'] = predicted


    def __getitem__(self, key):
        return self._storage[key]

    def __iter__(self):
        return iter(self._storage)

    def __len__(self):
        return len(self._storage)

    def __delitem__(self, key):
        '''
        To ensure that the Target class maintains the minimum Keys and Values
        to allow an instance to be used in Target based machine learning. The
        key and associated values that can be deleted are limited to:

        1. target_id

        :param key: The key and associated value to delete from the store.
        :returns: Updates the data store by removing key and value.
        :rtype: None
        '''

        accepted_keys = set(['target_id'])
        if key not in accepted_keys:
            raise KeyError('The only keys that can be deleted are the '\
                           'following: {} the key you wish to delete {}'\
                           .format(accepted_keys, key))
        del self._storage[key]

    def __setitem__(self, key, value):
        '''
        :param key: key (Only store values for `predicted` key)
        :param value: Predicted sentiment value which has to be the same data \
        type as the `sentiment` value.
        :type key: String (`predicted` is the only key accepted at the moment)
        :type value: Int or String.
        :returns: Nothing. Adds the predicted sentiment of the Target.
        :rtype: None.
        '''

        if key != 'predicted':
            raise KeyError('The Only key that can be changed is the `predicted`'\
                           ' key not {}'.format(key))
        #raise_type = False
        #sent_value = self._storage['sentiment']
        #if isinstance(sent_value, int):
        #    if not isinstance(value, (int, np.int32, np.int64)):
        #        raise_type = True
        #elif not isinstance(value, type(sent_value)):
        #    raise_type = True

        #if raise_type:
        #    raise TypeError('Value to be stored for the `predicted` sentiment '\
        #                    'has to be the same data type as the sentiment '\
        #                    'value {} and not {}.'\
        #                    .format(sent_value, type(value)))
        self._storage[key] = value

    def __repr__(self):
        '''
        :returns: String returned is what user see when the instance is \
        printed or printed within a interpreter.
        :rtype: String
        '''

        return 'Target({})'.format(self._storage)

    def __eq__(self, other):
        '''
        Two Target instances are equal if they are both Target instances and
        one of the following conditions

        1. They have the same target_id (This is preferred)
        2. The minimum keys that all targets have to have \
        ['spans', 'text', 'target', 'sentiment'] are all equal.

        :param other: The target instance that is being compare to the current \
        target instance.
        :type other: Target
        :returns: True if they are equal else False.
        :rtype: bool
        '''

        if not isinstance(other, Target):
            return False
        if 'target_id' in self and 'target_id' in other:
            if self['target_id'] != other['target_id']:
                return False
        else:
            minimum_keys = ['spans', 'text', 'target', 'sentiment']
            for key in minimum_keys:
                if not self[key] == other[key]:
                    return False
        return True
    def __array__(self):
        '''
        Function for converting it to a numpy array
        '''
        return np.asarray(dict(self))

class TargetCollection(MutableMapping):
    '''
    Mutable data store for Target data types.  i.e. A data store that contains
    multiple Target instances. This collection ensures that there are no two
    Target instances stored that have the same ID this is because the storage
    of the collection is an OrderedDict.

    Overrides collections.abs.MutableMapping abstract class.

    Functions:

    1. add -- Given a Target instance with an `id` key adds it to the data 
       store.
    2. data -- Returns all of the Target instances stored as a list of Target 
       instances.
    3. stored_sentiments -- Returns a set of unique sentiments stored.
    4. sentiment_data -- Returns the list of all sentiment values stored in 
       the Target instances stored.
    5. add_pred_sentiment -- Adds a list of predicted sentiment values to the 
       Target instances stored.
    6. confusion_matrix -- Returns the confusion matrix between the True and 
       predicted sentiment values.
    7. subset_by_sentiment -- Creates a new TargetCollection based on the 
       number of unique sentiments in a sentence.
    8. to_json_file -- Returns a Path to a json file that has stored the 
       data as a sample json encoded per line. If the split argument is set 
       will return two Paths the first being the training file and the second 
       the test.
    9. categories_targets -- Returns two dictionaries. The first is a category
       to target list and the second is a target to category list. Their is 
       the option to have a coarse grained cateogires option.
    10. target_set -- Returns a set of all the targets within this dataset.
    11. subset_by_ids -- Returns a TargetCollection which is a subset of the 
        current one. Where the samples included in the subset are those with 
        a `target_id` that is within the ids List.
    12. dataset_metric_scores -- Given a metric like accuracy returns all of 
        the metric scores for the dataset. This assumes that the dataset has 
        the `predicted` sentiment slot assigned.
    13. subset_by_targets -- Will subset the data so that only data points that 
        contain the given targets are within the TargetCollection.

    Static functions:
    
    1. target_targets -- Returns a dictionary of targets as keys and values 
       are a list of realted targets.
    2. split_dataset -- Returns the given dataset into two, the train and test 
       based on the test_split fraction given.
    3. load_from_json -- Returns a TargetCollection given that the json file 
       has a valid Target dictionary on each line of the json file. The 
       json file can be created from `to_json_file` method.

    Attributes:
    1. grouped_sentences -- A dictionary of sentence_id as keys and a list of 
       target instances that have the same sentence_id as values.
    2. grouped_sentiments -- A dictionary where the keys are all possible 
       sentiment values, the value is a list of Target(s) that only have that 
       associated sentiment value.
    3. grouped_distinct_sentiments -- A dictionary where the keys are the 
       number of distinct sentiments that the targets have in the associated 
       value. A target has two distinct sentiments if the associated sentence 
       has contains targets that take on one of two sentiment where at least 
       one target has a different sentiment to the rest. The targets in the 
       values of this dictionary are stored as a list of Target
    '''

    def __init__(self, list_of_target=None, name: Optional[str]=None):
        '''
        :param list_of_target: An interator of Target instances e.g. a List of 
                               Target instances.
        :type list_of_target: Iterable. Default None (Optional)
        :returns: Nothing. Constructor.
        :rtype: None
        '''

        self._storage = OrderedDict()
        if list_of_target is not None:
            if not hasattr(list_of_target, '__iter__'):
                raise TypeError('The list_of_target argument has to be iterable')
            for target in list_of_target:
                self.add(target)
        self.name = name if name is not None else 'TargetCollection'
        self._grouped_sentences = None
        self._grouped_sentiments = None
        self._grouped_distinct_sentiments = None

    def __getitem__(self, key):
        return self._storage[key]

    def __setitem__(self, key, value):
        '''
        If key already exists will raise KeyError.

        :param key: key that stores the index to the value
        :param value: value to store at the keys location
        :type key: hashable object
        :type value: Target
        :returns: Nothing. Adds data to the collection
        :rtype: None.
        '''

        # Required to make sure the grouped_sentences, grouped_sentiments,
        # and grouped_distinct_sentiments get recomputed instead of cached.
        self._data_has_changed = True
        self._data_has_changed_gs = True
        self._data_has_changed_gds = True
        if not isinstance(value, Target):
            raise TypeError('All values in this store have to be of type '\
                            'Target not {}'.format(type(value)))
        if key in self._storage:
            raise KeyError('This key: `{}` already exists with value `{}` '\
                           'value that for the same key is `{}`'\
                           .format(key, self._storage[key], value))
        temp_value = copy.deepcopy(value)
        # As the id will be saved as the key no longer needed in the target
        # instance (value). However if the key does not match the `target_id`
        # raise KeyError
        if 'target_id' in value:
            if value['target_id'] != key:
                raise KeyError('Cannot add this to the data store as the key {}'\
                               ' is not the same as the `target_id` in the Target'\
                               ' instance value {}'.format(key, value))
            del temp_value['target_id']
        self._storage[key] = temp_value

    def __delitem__(self, key):
        del self._storage[key]

    def __iter__(self):
        return iter(self._storage)

    def __len__(self):
        return len(self._storage)

    def add(self, value):
        '''
        Adds the Target instance to the data store without having to extract
        out the target_id of the target if using __setitem__

        :Example:

        >>> target = Target([(10, 16)], '1', 'Iphone',
                            'text with Iphone', 0)
        >>> target_col = TargetCollection()
        # Add method is simpler to use than __setitem__
        >>> target_col.add(target)
        # Example of the __setitem__ method
        >>> target_col[target['target_id']] = target

        :param value: Target instance with a `target_id` key
        :type value: Target
        :returns: Nothing. Adds the target instance to the data store.
        :rtype: None
        '''

        if not isinstance(value, Target):
            raise TypeError('All values in this store have to be of type '\
                            'Target not {}'.format(type(value)))
        if 'target_id' not in value:
            raise ValueError('The Target instance given {} does not have a '\
                             'target_id'.format(value))
        self[value['target_id']] = value

    def data(self):
        '''
        :returns: a list of all the Target instances stored.
        :rtype: list
        '''

        _data = []
        for _id, target_data in self.items():
            data_dict = {**target_data}
            data_dict['target_id'] = _id
            _data.append(Target(**data_dict))
        return _data

    def data_dict(self):
        '''
        :returns: Same as the data function but returns dicts instead of \
        Targets
        :rtype: list
        '''

        _data = []
        for _id, target_data in self.items():
            data_dict = {**target_data}
            data_dict['target_id'] = _id
            _data.append(data_dict)
        return _data

    def stored_sentiments(self) -> Set[Any]:
        '''
        :returns: A set of all unique sentiment values of the target instances \
        in the data store.
        :rtype: set
        '''

        unique_sentiments = set()
        for target_data in self.values():
            unique_sentiments.add(target_data['sentiment'])
        return unique_sentiments

    def sentiment_data(self, mapper=None, sentiment_field='sentiment'):
        '''
        :param mapper: A dictionary that maps the keys to the values where the \
        keys are the current unique sentiment values of the target instances \
        stored
        :param sentiment_field: Determines if it should return True sentiment \
        of the Targets `sentiment` or to return the predicted value `predicted`
        :type mapper: dict
        :type sentiment_field: String. Default `sentiment` (True values)
        :returns: a list of the sentiment value for each Target instance stored.
        :rtype: list

        :Example of using the mapper:
        >>> target_col = TargetCollection([Target([(10, 16)], '1', 'Iphone',
                                                  'text with Iphone', 'pos')])
        >>> target_col.add(Target([(10, 15)], '2', 'Pixel',
                                  'text with Pixel', 'neg'))
        # Get the unique sentiment values for each target instance
        >>> map_keys = target_col.stored_sentiments()
        >>> print(map_keys)
        >>> ['pos', 'neg']
        >>> mapper = {'pos' : 1, 'neg' : -1}
        >>> print(target_col.sentiment_data(mapper=mapper))
        >>> 1, -1
        '''

        allowed_fields = set(['sentiment', 'predicted'])
        if sentiment_field not in allowed_fields:
            raise ValueError('The `sentiment_field` has to be one of the '\
                             'following values {} and not {}'\
                             .format(allowed_fields, sentiment_field))

        if mapper is not None:
            if not isinstance(mapper, dict):
                raise TypeError('The mapper has to be of type dict and not {}'\
                                .format(type(mapper)))
            allowed_keys = self.stored_sentiments()
            if len(mapper) != len(allowed_keys):
                raise ValueError('The mapper has to contain a mapping for each '\
                                 'unique sentiment value {} and not a subset '\
                                 'given {}'.format(allowed_keys, mapper.keys()))
            for map_key in mapper:
                if map_key not in allowed_keys:
                    raise ValueError('The mappings are not correct. The map '\
                                     'key {} does not exist in the unique '\
                                     'sentiment values in the store {}'\
                                     .format(map_key, allowed_keys))
            return [mapper[target_data[sentiment_field]]\
                    for target_data in self.values()]

        return [target_data[sentiment_field] for target_data in self.values()]

    def add_id_pred(self, id_pred):
        count = 0
        for targ_id in self:
            if targ_id in id_pred:
                self[targ_id]['predicted'] = id_pred[targ_id]
                count += 1
        if count != len(self):
            raise ValueError('We have only added {} predictions to {} targets'\
                             .format(count, len(self)))

    def add_pred_sentiment(self, sent_preds: Union[List[Any], np.ndarray], 
                           mapper: Optional[Dict[Any, Any]] = None) -> None:
        '''
        :param sent_preds: A list of predicted sentiments for all Target 
                           instances stored or a numpy array where columns are 
                           number of different predicted runs and the rows 
                           represent the associated Target instance.
        :param mapper: A dictionary mapping the predicted sentiment to 
                       alternative values e.g. Integer values to String values.
        :type sent_preds: list or numpy array
        :type mapper: dict
        :returns: Nothing. Adds the predicted sentiments to the Target 
                   instances stored.
        '''

        if len(sent_preds) != len(self):
            raise ValueError('The length of the predicted sentiments {} is not '\
                             'equal to the number Target instances stored {}'\
                             .format(len(sent_preds), len(self)))
        for index, target in enumerate(self.data()):
            predicted_sent = sent_preds[index]
            if mapper is not None:
                predicted_sent = mapper[predicted_sent]
            target_id = target['target_id']
            self._storage[target_id]['predicted'] = predicted_sent

    def confusion_matrix(self, plot=False, norm=False):
        '''
        :param plot: To return a heatmap of the confusion matrix.
        :param norm: Normalise the values in the confusion matrix
        :type plot: bool. Default False
        :type norm: bool. Default False
        :returns: A tuple of length two. 1. the confusion matrix \
        2. The plot of the confusion matrix if plot is True else \
        None.
        :rtype: tuple
        '''

        sentiment_values = sorted(self.stored_sentiments())
        true_values = self.sentiment_data()
        pred_values = self.sentiment_data(sentiment_field='predicted')
        conf_matrix = metrics.confusion_matrix(true_values, pred_values,
                                               labels=sentiment_values)
        if norm:
            conf_matrix = conf_matrix / conf_matrix.sum()
        conf_matrix = pd.DataFrame(conf_matrix, columns=sentiment_values,
                                   index=sentiment_values)
        ax = None
        if plot:
            if norm:
                ax = sns.heatmap(conf_matrix, annot=True, fmt='.2f')
            else:
                ax = sns.heatmap(conf_matrix, annot=True, fmt='d')
        return conf_matrix, ax

    def subset_by_sentiment(self, num_unique_sentiments):
        '''
        Creates a subset based on the number of unique sentiment values per
        sentence. E.g. if num_unique_sentiments = 2 then it will
        return all the Target instances where each target intance has at least
        two target instances per sentence and those targets can have only one
        of two sentiment values. This can be used to test how well a method
        can extract exact sentiment information for the associated target.

        NOTE: Requires that all Target instances stored contain a sentence_id.

        :param num_unique_sentiments: Integer specifying the number of unique \
        sentiments in the target instances per sentence.
        :type num_unique_sentiments: int
        :returns: A subset based on the number of unique sentiments per sentence.
        :rtype: TargetCollection
        '''

        all_relevent_targets = []
        for targets in self.grouped_sentences.values():
            target_col = TargetCollection(targets)
            if len(target_col.stored_sentiments()) == num_unique_sentiments:
                all_relevent_targets.extend(targets)
        return TargetCollection(all_relevent_targets)

    def subset_by_targets(self, target_set: Set[str]):
        '''
        Will subset the data so that only data points that contain the given 
        targets are within the TargetCollection.
        
        :param target_set: A list of targets to be used to sub-sample 
                           the data collection from.
        :returns: The current target collection with data points that only 
                  have targets that are from the target set.
        :rtype: TargetCollection
        '''

        target_data = []
        for data in self.data_dict():
            if data['target'].lower() in target_set:
                target_data.append(Target(**data))
        return TargetCollection(target_data)

    def subset_by_sentence_length(self, length_condition):

        all_relevent_targets = []
        for target in self.data():
            target_text = target['text']
            if length_condition(target_text):
                all_relevent_targets.append(target)
        return TargetCollection(all_relevent_targets)

    @staticmethod
    def load_from_json(json_path: Path) -> 'TargetCollection':
        '''
        Returns a TargetCollection given that the json file has a valid Target 
        dictionary on each line of the json file. The json file can be created 
        from `to_json_file` method.

        :param json_path: Path to the json file that has a valid Target that 
                          can be loaded as a json sequence on each new line.
        :returns: A TargetCollection of all targets that we stored in the 
                  json file.
        '''
        target_list = []
        with json_path.open('r') as json_file:
            for line in json_file:
                target = json.loads(line)
                target['spans'] = [tuple(span) for span in target['spans']]
                if 'epoch_number' in target:
                    target['epoch_number'] = set(target['epoch_number'])
                target = Target(**target)
                target_list.append(target)
        return TargetCollection(target_list)

    @staticmethod
    def split_dataset(data: 'TargetCollection', test_split: float, 
                      random: bool = False
                      ) -> Tuple['TargetCollection', 'TargetCollection']:
        '''
        It will split the data into training and test splits, where the amount of 
        data in the test is defined by the test_split fraction (amount of training 
        data will be 1 - test_split).

        :param data: data to split
        :param test_split: The amount of data to give to the test split.
        :param random: If the splitting should be random rather than the last 
                    test split of the data being test and the first 
                    (1 - test split) being the training data.
        :returns: The training data and test data as a tuple.
        '''
        target_data = data.data_dict()
        data_size = len(target_data)
        test_data_size = int(data_size * test_split)
        test_data = []
        train_data = []
        if random:
            start_index = rand.randint(0, data_size)
            end_index = start_index + test_data_size
            if end_index > data_size:
                index_diff = end_index - data_size
                start_index -= index_diff
                end_index = data_size
            test_data = target_data[start_index: end_index]
            train_data = target_data[end_index:]
            train_data.extend(target_data[: start_index])
        else:
            test_data = target_data[: test_data_size]
            train_data = target_data[test_data_size:]
        train_data = [Target(**t_data) for t_data in train_data]
        test_data = [Target(**t_data) for t_data in test_data]
        return (TargetCollection(train_data), TargetCollection(test_data))

    def to_json_file(self, dataset_name: Union[str, List[str]], 
                     split: Optional[float] = None, cache: bool = True, 
                     group_by_sentence: bool = False, random: bool = False
                     ) -> Union[Path, List[Path]]:
        '''
        Returns a Path to a json file that has stored the data as a sample json 
        encoded per line. If the split argument is set will return two Paths 
        the first being the training file and the second the test.

        The Path does not need to be specified as it saves it to the 
        `~/.Bella/datasets/.` directory within your user space under the 
        dataset_name.

        To split the bella.data_types.TargetCollection.split_dataset method is 
        used.

        :param dataset_name: Name to associate to the dataset e.g. 
                             `SemEval 2014 rest train`. If split is not None 
                             then use a List of Strings e.g. 
                             [`SemEval 2014 rest train`, 
                             `SemEval 2014 rest dev`]
        :param split: Whether or not to split the dataset into train, test 
                      split. If not use None else specify the fraction of 
                      the data to use for the test split.
        :param cache: If the data is already saved use the Cache. Default 
                      is to use the cached data.
        :param group_by_sentence: Whether the data should be grouped by sentence
                                  this will then produce json lines that can 
                                  contain more than one target in a sentence.
        :param random: Whether the splitting of the training and test should 
                       be random or not.
        '''
        def create_json_file(fp: Path, data: List[Dict[str, Any]]) -> None:
            '''
            Given the a list of dictionaries that represent the Target data 
            converts these samples into json encoded samples which are saved on 
            each line within the file at the given file path(fp)

            :param fp: File path that will store the json samples one per line
            :param data: List of dictionaries that represent the Target data.
            :return: Nothing that data will be saved to the file.
            '''                
            with fp.open('w+') as json_file:
                if group_by_sentence:
                    data = TargetCollection([Target(**d) for d in data])
                    data = data.grouped_sentences
                    for index, target_datas in enumerate(data.values()):
                        text = target_datas[0]['text']
                        sentiments = []
                        targets = []
                        spans = []
                        for target_data in target_datas:
                            sentiments.append(target_data['sentiment'])
                            spans.append(target_data['spans'])
                            targets.append(target_data['target'])
                        sentence_data = {'text': text, 'sentiments': sentiments,
                                         'targets': targets, 'spans': spans}
                        json_encoded_data = json.dumps(sentence_data)
                        if index != 0:
                            json_encoded_data = f'\n{json_encoded_data}'
                        json_file.write(json_encoded_data)
                else:
                    for index, target_data in enumerate(data):
                        if 'epoch_number' in target_data:
                            target_data['epoch_number'] = list(target_data['epoch_number'])
                        json_encoded_data = json.dumps(target_data)
                        if index != 0:
                            json_encoded_data = f'\n{json_encoded_data}'
                        json_file.write(json_encoded_data)
            
        # If splitting the data there has to be two dataset names else one name
        if split is None:
            assert isinstance(dataset_name, str)
        elif isinstance(split, float):
            assert isinstance(dataset_name, list)
            assert len(dataset_name) == 2
        
        BELLA_DATASET_DIR.mkdir(parents=True, exist_ok=True)

        dataset_names = dataset_name
        if not isinstance(dataset_name, list):
            dataset_names = [dataset_name]
        all_paths_exist = True
        dataset_paths = []
        for name in dataset_names:
            dataset_path = BELLA_DATASET_DIR.joinpath(name)
            if not dataset_path.exists():
                all_paths_exist = False
            dataset_paths.append(dataset_path)
        # Caching
        if cache and all_paths_exist:
            print(f'Using cache for the follwoing datasets: {dataset_names}')
            if split is None:
                return dataset_paths[0]
            return dataset_paths

        if split is None:
            create_json_file(dataset_paths[0], self.data_dict())
            return dataset_paths[0]
        # Splitting
        train, test = self.split_dataset(self, test_split=split, 
                                         random=random)
        create_json_file(dataset_paths[0], train.data_dict())
        create_json_file(dataset_paths[1], test.data_dict())
        return dataset_paths

    def categories_targets(self, filter: int = 2, coarse: bool = False
                           ) -> Tuple[Dict[str, List[str]], 
                                      Dict[str, List[str]]]:
        '''
        Returns two dictionaries. The first is a category to target list and 
        the second is a target to category list. Their is the option to have a 
        coarse grained cateogires option.
        '''
        if 'category' not in self.data()[0]:
            raise ValueError('The current TargetCollection must contain '
                             'targets that have a category key')

        temp_category_targets = defaultdict(set)
        for data in self.data():
            category = data['category']
            if coarse:
                category = category.split('#')[0]
            target = data['target']
            temp_category_targets[category].add(target)
        
        category_targets = {}
        target_categories = defaultdict(list)
        categories_filtered = []
        for category, targets in temp_category_targets.items():
            if len(targets) < filter:
                categories_filtered.append(category)
                continue
            category_targets[category] = list(targets)
            for target in targets:
                target_categories[target].append(category)
        # Which categories are filtered
        print(f'Filtered {len(categories_filtered)} categories which are:')
        for category in categories_filtered:
            print(category)

        return category_targets, dict(target_categories)

    @staticmethod
    def target_targets(target_set: set, 
                       category_targets: Dict[str, List[str]]
                       ) -> Dict[str, List[str]]:
        '''
        Returns a dictionary of targets as keys and values are a list of 
        realted targets.

        The related targets have all come from category_targets dictionary. 
        Where a target is related if it is in the same category. If it is in 
        multiple categories then all targets from each of those categories 
        are related.

        :param target_set: A list of targets that are candiate keys in the 
                           returned dictionary.
        :param category_targets: A dictionary of latent categories as keys 
                                 and related targets as values.
        :returns: Dictionary of targets and their related targets as values 
                  where the related targets have come from the category_targets
                  dictionary.
        '''
        target_rel_targets = {}
        for target in target_set:
            rel_targets = []
            for _, cat_targets in category_targets.items():
                if target in cat_targets or target.lower() in cat_targets:
                    rel_targets.extend(cat_targets)
                else:
                    lower_cat_targets = [cat_target.lower() 
                                         for cat_target in cat_targets]
                    if target.lower() in lower_cat_targets:
                        rel_targets.extend(cat_targets)
            if rel_targets:
                rel_targets = list(set(rel_targets))

                to_remove = set()
                for rel_target in rel_targets:
                    temp_rel_target = rel_target.lower()
                    if target.lower() == temp_rel_target:
                        to_remove.add(rel_target)
                for target_to_remove in to_remove:
                    rel_targets.remove(target_to_remove)
                if not to_remove:
                    raise ValueError('The target that maps to the list of '
                                     'related target should be in the related '
                                     'targets before being filtered out')
                target_rel_targets[target] = rel_targets
        return target_rel_targets

    def target_set(self, lower: bool = False) -> set:
        '''
        Returns a set of all the targets within this dataset.

        :param lower: Whether to return the targets lower cased.
        :returns: A set of all the targets within this dataset.
        '''
        targets = set()
        for data in self.data():
            target = data['target']
            if lower:
                target = target.lower()
            targets.add(target)
        return targets

    def subset_by_ids(self, ids: List[str]) -> 'TargetCollection':
        '''
        Returns a TargetCollection which is a subset of the current one. 
        Where the samples included in the subset are those with a `target_id`
        that is within the ids List.

        :param ids: A list of `target_id`s that are to be included in the 
                    subset
        :returns: A subset of the current TargetCollection where the subset 
                  only includes samples that have a `target_id` in the ids 
                  given.
        '''
        subset_data = []
        for data_id in ids:
            rel_data = dict(self[data_id].items())
            rel_data['target_id'] = data_id
            subset_data.append(Target(**rel_data))
        return TargetCollection(subset_data)

    def dataset_metric_scores(self, 
                              metric: Callable[[np.ndarray, np.ndarray], 
                                               float], 
                              **metric_kwargs) -> np.ndarray:
        '''
        Given a metric like accuracy returns all of the metric scores for the 
        dataset. This assumes that the dataset has the `predicted` sentiment 
        slot assigned.

        :param metric: Metric function e.g. f1_score
        :param metric_kwargs: Keyword arguments to provide to the metric 
                              function e.g. `average` = `macro`
        :returns: An array of metric results. One for each column in the 
                  predicted sentiment array.
        '''
        true_labels = self.sentiment_data()
        pred_matrix = self.sentiment_data(sentiment_field='predicted')
        score_vector = np.apply_along_axis(metric, 0, pred_matrix, 
                                           true_labels, **metric_kwargs)
        return score_vector


    # Not tested
    def targets_per_sentence(self):
        '''
        :returns: Dictionary of number of targets as keys and values the number \
        of sentences that have that many targets per sentence.
        :rtype: dict

        :Example:
        If we have 5 sentences that contain 1 target each and 4 sentences that
        contain 3 targets each then it will return a dict like:
        {1 : 5, 3 : 4}
        '''

        targets_sentence = {}
        for targets in self.grouped_sentences.values():
            num_targets = len(targets)
            targets_sentence[num_targets] = targets_sentence.get(num_targets, 0) + 1
        return targets_sentence

    # Not tested
    def avg_targets_per_sentence(self):
        return len(self) / self.number_sentences()
    # Not tested
    def number_sentences(self):
        return len(self.grouped_sentences)
    # Not tested
    def number_unique_targets(self):
        target_count = {}
        for target_instance in self.values():
            target = target_instance['target']
            target_count[target] = target_count.get(target, 0) + 1
        return len(target_count)

    def no_targets_sentiment(self):
        sentiment_targets = {}
        for target in self.values():
            sentiment = target['sentiment']
            sentiment_targets[sentiment] = sentiment_targets.get(sentiment, 0) + 1
        return sentiment_targets

    def ratio_targets_sentiment(self):
        no_sentiment_target = self.no_targets_sentiment()
        total_targets = sum(no_sentiment_target.values())
        ratio_sentiment_targets = {}
        for sentiment, no_targets in no_sentiment_target.items():
            ratio_sentiment_targets[sentiment] = round(no_targets / total_targets, 2)
        return ratio_sentiment_targets

    @property
    def grouped_sentences(self) -> Dict[str, List['Target']]:
        '''
        A dictionary of sentence_id as keys and a list of target instances that 
        have the same sentence_id as values.

        It stores a cache of this result and the cache will expire once the 
        data has changed within itself and then this value will have to be 
        recomputed.

        :returns: A dictionary of sentence_id as keys and a list of target 
                  instances that have the same sentence_id as values.
        '''

        # If the data has changed re-compute or if the data has never been 
        # compute, compute else return the cached results.
        if self._data_has_changed or self._grouped_sentences is None:
            self._data_has_changed = False
            sentence_targets = defaultdict(list)
            for target in self.data():
                if 'sentence_id' not in target:
                    raise ValueError(f'A Target id instance {target} does not '
                                     'have a sentence_id which is required.')
                sentence_id = target['sentence_id']
                sentence_targets[sentence_id].append(target)
            self._grouped_sentences = sentence_targets
            
        return self._grouped_sentences

    @property
    def grouped_sentiments(self) -> Dict[Any, List['Target']]:
        '''
        A dictionary where the keys are all possible sentiment values, the 
        value is a list of Target(s) that only have that associated sentiment 
        value.

        It stores a cache of this result and the cache will expire once the 
        data has changed within itself and then this value will have to be 
        recomputed.

        :returns: A dictionary of sentiment values as keys and a list of target 
                  instances that have the same sentiment value.
        '''

        # If the data has changed re-compute or if the data has never been 
        # compute, compute else return the cached results.
        if self._data_has_changed_gs or self._grouped_sentiments is None:
            self._data_has_changed_gs = False
            sentiment_targets = defaultdict(list)
            for target in self.data():
                sentiment_targets[target['sentiment']].append(target)
            self._grouped_sentiments = sentiment_targets
            
        return self._grouped_sentiments  

    @property
    def grouped_distinct_sentiments(self) -> Dict[Any, List['Target']]:
        '''
        A dictionary where the keys are the number of distinct sentiments that 
        the targets have in the associated value. A target has two distinct 
        sentiments if the associated sentence has contains targets that take 
        on one of two sentiment where at least one target has a different 
        sentiment to the rest. The targets in the values of this dictionary 
        are stored as a list of Target

        It stores a cache of this result and the cache will expire once the 
        data has changed within itself and then this value will have to be 
        recomputed.

        :returns: A dictionary of distinct sentiments per sentence as keys and 
                  a list of target instances that have the same distinct 
                  sentiments per sentence
        '''

        # If the data has changed re-compute or if the data has never been 
        # compute, compute else return the cached results.
        if self._data_has_changed_gds or self._grouped_distinct_sentiments is None:
            self._data_has_changed_gds = False
            distinct_sentiment_targets = defaultdict(list)
            for targets in self.grouped_sentences.values():
                target_col = TargetCollection(targets)
                num_unique_sentiments = len(target_col.stored_sentiments())
                distinct_sentiment_targets[num_unique_sentiments].extend(targets)
            self._grouped_distinct_sentiments = distinct_sentiment_targets
        return self._grouped_distinct_sentiments

    def group_by_sentence(self):
        '''
        This is now deprecated, please use grouped_sentences property.

        :returns: A dictionary of sentence_id as keys and a list of target \
        instances that have the same sentence_id as values.
        :rtype: defaultdict (default is list)
        '''

        dep_warning = ('This is now deprecated, please use grouped_sentences '
                       'property.')
        warnings.warn(dep_warning, DeprecationWarning)

        sentence_targets = defaultdict(list)
        for target in self.data():
            if 'sentence_id' not in target:
                raise ValueError('A Target id instance {} does not have '\
                                 'a sentence_id which is required.'\
                                 .format(target))
            sentence_id = target['sentence_id']
            sentence_targets[sentence_id].append(target)
        return sentence_targets

    def avg_constituency_depth(self):
        avg_depths = []
        for data in self.values():
            sentence_trees = constituency_parse(data['text'])
            tree_depths = [tree.height() - 1 for tree in sentence_trees]
            avg_depth = sum(tree_depths) / len(sentence_trees)
            avg_depths.append(avg_depth)
        return sum(avg_depths) / len(avg_depths)

    def avg_sentence_length_per_target(self, tokeniser=whitespace):
        all_sentence_lengths = []
        for data in self.values():
            all_sentence_lengths.append(len(tokeniser(data['text'])))
        return sum(all_sentence_lengths) / len(all_sentence_lengths)

    def word_list(self, tokeniser: Callable[[str], List[str]],
                  min_df: int = 0, lower: bool = True) -> List[str]:
        '''
        :param tokeniser: Tokeniser function to tokenise the text 
                          of each target/sample
        :param min_df: Optional. The minimum percentage of documents a 
                       token must occur in.
        :param lower: Optional. Whether to lower the text. 
        :return: A word list of all tokens that occur in this data collection 
                 given min_df.
        '''

        token_df = defaultdict(lambda: 0)
        num_df = 0
        for target in self.values():
            num_df += 1
            tokens = tokeniser(target['text'])
            for token in tokens:
                if lower:
                    token = token.lower()
                token_df[token] += 1
        min_df_value = int((num_df / 100) * min_df)
        word_list = [token for token, df in token_df.items()
                     if df > min_df_value]
        return word_list

    @staticmethod
    def combine_collections(*args):
        all_targets = []
        for collections in args:
            all_targets.extend(collections.data())
        return TargetCollection(all_targets)

    def __eq__(self, other):

        if len(self) != len(other):
            return False
        for key in self:
            if key not in other:
                return False
        return True

    def __repr__(self):
        '''
        :returns: String returned is what user see when the instance is \
        printed or printed within a interpreter.
        :rtype: String
        '''

        target_strings = ''

        self_len = len(self)
        if self_len > 2:
            for index, target in enumerate(self.data()):
                if index == 0:
                    target_strings += '{} ... '.format(target)
                if index == self_len - 1:
                    target_strings += '{}'.format(target)
        else:
            for target in self.data():
                target_strings += '{}, '.format(target)
        if target_strings != '':
            target_strings = target_strings.rstrip(', ')
        return 'TargetCollection({})'.format(target_strings)

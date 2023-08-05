#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
diego/study.py was created on 2019/03/21.
file in :relativeFile
Author: Charles_Lai
Email: lai.bluejay@gmail.com
"""
from typing import Union
from typing import Type
from typing import Tuple
from typing import Set
from typing import Optional
from typing import List
from typing import Dict
from typing import Callable
from typing import Any

from collections import defaultdict

from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.utils import validation
from sklearn.externals import joblib, six

from diego.depens import logging
from diego.preprocessor import AutobinningTransform, LocalUncertaintySampling
from diego.trials import Trial
from diego import trials as trial_module
from diego import basic
from diego.core import Storage
from diego import metrics as diego_metrics


import collections
import datetime
import math
import multiprocessing
import multiprocessing.pool
from multiprocessing import Queue
import pandas as pd
from six.moves import queue
import time
from sklearn.utils import check_X_y
from autosklearn.classification import AutoSklearnClassifier
from tpot import TPOTClassifier

ObjectiveFuncType = Callable[[trial_module.Trial], float]


def _name_estimators(estimators):
    """Generate names for estimators."""

    names = [type(estimator).__name__.lower() for estimator in estimators]
    namecount = defaultdict(int)
    for est, name in zip(estimators, names):
        namecount[name] += 1

    for k, v in list(six.iteritems(namecount)):
        if v == 1:
            del namecount[k]

    for i in reversed(range(len(estimators))):
        name = names[i]
        if name in namecount:
            names[i] += "-%d" % namecount[name]
            namecount[name] -= 1

    return list(zip(names, estimators))


class Study(object):
    """
    reference diego
    A study corresponds to an optimization task, i.e., a set of trials.

    Note that the direct use of this constructor is not recommended.

    This object provides interfaces to run a new , access trials'
    history, set/get user-defined attributes of the study itself.

    Args:
        study_name:
            Study's name. Each study has a unique name as an identifier.
        storage:

    """

    def __init__(
            self,
            study_name,  # type: str
            storage,  # type: Union[str, storages.BaseStorage]
            sample_method=None,
            sample_params=dict(),
            is_autobin=False,
            bin_params=dict(),
            export_model_path=None
    ):
        # type: (...) -> None

        self.study_name = study_name
        self.storage = get_storage(storage)
        self.sample_method = sample_method
        if sample_method == 'lus':
            self.sampler = LocalUncertaintySampling(**sample_params)
        else:
            self.sampler = None
        self.is_autobin = is_autobin
        if self.is_autobin:
            if len(bin_params) > 1:
                self.bin_params = bin_params
            else:
                self.bin_params = dict()
            self.binner = AutobinningTransform()
        self.study_id = self.storage.get_study_id_from_name(study_name)
        self.logger = logging.get_logger(__name__)
        self.trial_list = []
        # export model. should be joblib.Memory object
        self.pipeline = None
        self.export_model_path = export_model_path

    def __getstate__(self):
        # type: () -> Dict[Any, Any]

        state = self.__dict__.copy()
        del state['logger']
        return state

    def __setstate__(self, state):
        # type: (Dict[Any, Any]) -> None

        self.__dict__.update(state)
        self.logger = logging.get_logger(__name__)

    def __init_bin_params(self,):
        params = dict()
        params['binning_method'] = 'xgb'
        params['binning_value_type'] = 'woe'

    @property
    def best_value(self):
        # type: () -> float
        """Return the best objective value in the :class:`~diego.study.Study`.

        Returns:
            A float representing the best objective value.
        """

        best_value = self.best_trial.value
        if best_value is None:
            raise ValueError('No trials are completed yet.')

        return best_value

    @property
    def best_trial(self):
        # type: () -> basic.FrozenTrial
        """Return the best trial in the :class:`~diego.study.Study`.

        Returns:
        """
        bt = self.storage.get_best_trial(self.study_id)
        return bt

    @property
    def all_trials(self):
        return self.storage.get_all_trials(self.study_id)

    @property
    def direction(self):
        # type: () -> basic.StudyDirection
        """Return the direction of the :class:`~diego.study.Study`.

        Returns:
        """

        return self.storage.get_study_direction(self.study_id)

    @property
    def trials(self):
        # type: () -> List[basic.FrozenTrial]
        """Return all trials in the :class:`~diego.study.Study`.

        Returns:
        """

        return self.storage.get_all_trials(self.study_id)

    @property
    def user_attrs(self):
        # type: () -> Dict[str, Any]
        """Return user attributes.

        Returns:
            A dictionary containing all user attributes.
        """

        return self.storage.get_study_user_attrs(self.study_id)

    @property
    def system_attrs(self):
        # type: () -> Dict[str, Any]
        """Return system attributes.

        Returns:
            A dictionary containing all system attributes.
        """

        return self.storage.get_study_system_attrs(self.study_id)

    def optimize(
            self, X_test, y_test,
            timeout=None,  # type: Optional[float]
            n_jobs=1,  # type: int
            # type: Union[Tuple[()], Tuple[Type[Exception]]]
            catch=(Exception, ),
            metrics:str ='logloss'
    ):
        # type: (...) -> None
        """Optimize an objective function.

        Args:
            func:
                A callable that implements objective function.
            n_trials:
                The number of trials. If this argument is set to :obj:`None`, there is no
                limitation on the number of trials. If :obj:`timeout` is also set to :obj:`None`,
                the study continues to create trials until it receives a termination signal such
                as Ctrl+C or SIGTERM.
            timeout:
                Stop study after the given number of second(s). If this argument is set to
                :obj:`None`, the study is executed without time limitation. If :obj:`n_trials` is
                also set to :obj:`None`, the study continues to create trials until it receives a
                termination signal such as Ctrl+C or SIGTERM.
            n_jobs:
                The number of parallel jobs. If this argument is set to :obj:`-1`, the number is
                set to CPU counts.
            catch:
                A study continues to run even when a trial raises one of exceptions specified in
                this argument. Default is (`Exception <https://docs.python.org/3/library/
                exceptions.html#Exception>`_,), where all non-exit exceptions are handled
                by this logic.

        """
        X_test, y_test = check_X_y(X_test, y_test)
        self.storage.set_test_storage(X_test, y_test)
        # TODO Preprocess Trial
        if self.sample_method == 'lus':
            X_train, y_train = self.storage.X_train, self.storage.y_train
            X_train, y_train = self.sampler.fit_transform(X_train, y_train)
            self.storage.set_train_storage(X_train, y_train)
        if self.is_autobin:
            self.binner.fit(self.storage.X_train, self.storage.y_train)
            X_train = self.binner.transform(self.storage.X_train)
            X_test = self.binner.transform(X_test)
            self.storage.set_train_storage(X_train, self.storage.y_train)
            self.storage.set_test_storage(X_test, y_test)
            self._pipe_add(self.binner)
        n_jobs = basic.get_approp_n_jobs(n_jobs)
        if self.trial_list is None or self.trial_list == []:
            self.logger.warning('no trials, init by default params.')
            self.trial_list = self._init_trials(n_jobs)
        # 当前保证在Trial内进行多进程
        # if n_jobs == 1:
        #     self._optimize_sequential(self.trial_list, timeout, catch)
        # else:
        #     self._optimize_parallel(self.trial_list, timeout, n_jobs, catch)
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            self._optimize_sequential(self.trial_list, timeout, catch, metrics=metrics)
            self._pipe_add(self.best_trial.clf)
            self._export_model(self.export_model_path)

    def show_models(self):
        for step in self.pipeline.steps:
            name, estm = step
            if isinstance(estm, AutoSklearnClassifier):
                print(name, estm.show_models())
            else:
                print(name, estm)

    def set_user_attr(self, key, value):
        # type: (str, Any) -> None
        """Set a user attribute to the :class:`~diego.study.Study`.

        Args:
            key: A key string of the attribute.
            value: A value of the attribute. The value should be JSON serializable.

        """

        self.storage.set_study_user_attr(self.study_id, key, value)

    def set_system_attr(self, key, value):
        # type: (str, Any) -> None
        """Set a system attribute to the :class:`~diego.study.Study`.

        Note that diego internally uses this method to save system messages. Please use
        :func:`~diego.study.Study.set_user_attr` to set users' attributes.

        Args:
            key: A key string of the attribute.
            value: A value of the attribute. The value should be JSON serializable.

        """

        self.storage.set_study_system_attr(self.study_id, key, value)

    def trials_dataframe(self, include_internal_fields=False):
        # type: (bool) -> pd.DataFrame
        """Export trials as a pandas DataFrame_.

        The DataFrame_ provides various features to analyze studies. It is also useful to draw a
        histogram of objective values and to export trials as a CSV file. Note that DataFrames
        returned by :func:`~diego.study.Study.trials_dataframe()` employ MultiIndex_, and columns
        have a hierarchical structure. Please refer to the example below to access DataFrame
        elements.

        Example:

            Get an objective value and a value of parameter ``x`` in the first row.

            >>> df = study.trials_dataframe()
            >>> df
            >>> df.value[0]
            0.0
            >>> df.params.x[0]
            1.0

        Args:
            include_internal_fields:
                By default, internal fields of :class:`~diego.basic.FrozenTrial` are excluded
                from a DataFrame of trials. If this argument is :obj:`True`, they will be included
                in the DataFrame.

        Returns:
            A pandas DataFrame_ of trials in the :class:`~diego.study.Study`.

        .. _DataFrame: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html
        .. _MultiIndex: https://pandas.pydata.org/pandas-docs/stable/advanced.html
        """

        # column_agg is an aggregator of column names.
        # Keys of column agg are attributes of FrozenTrial such as 'trial_id' and 'params'.
        # Values are dataframe columns such as ('trial_id', '') and ('params', 'n_layers').
        column_agg = collections.defaultdict(set)  # type: Dict[str, Set]
        non_nested_field = ''

        records = []  # type: List[Dict[Tuple[str, str], Any]]
        for trial in self.trials_list:
            trial_dict = trial._asdict()

            record = {}
            for field, value in trial_dict.items():
                if not include_internal_fields and field in basic.FrozenTrial.internal_fields:
                    continue
                if isinstance(value, dict):
                    for in_field, in_value in value.items():
                        record[(field, in_field)] = in_value
                        column_agg[field].add((field, in_field))
                else:
                    record[(field, non_nested_field)] = value
                    column_agg[field].add((field, non_nested_field))
            records.append(record)

        columns = sum((sorted(column_agg[k])
                       for k in basic.FrozenTrial._fields), [])

        return pd.DataFrame(records, columns=pd.MultiIndex.from_tuples(columns))

    def _init_trials(self, metrics='roc_auc', n_jobs=1):
        # tpot耗时较久，舍弃。相同时间内不如auto-sklearn
        auto_sklearn_trial = self.generate_autosk_trial()
        # tpot_trial = self.generate_tpot_trial()
        return [auto_sklearn_trial]

    def _optimize_sequential(
            self,
            trials,  # type: Optional[int]
            timeout,  # type: Optional[float]
            catch ,
            metrics:str='logloss',
    ):
        # type: (...) -> None
        time_start = datetime.datetime.now()
        for trial in trials:
            if timeout is not None:
                elapsed_seconds = (datetime.datetime.now() -
                                   time_start).total_seconds()
                if elapsed_seconds >= timeout:
                    break

            self._run_trial(trial, catch, metrics=metrics)

    # TODO multi clf
    def _optimize_parallel(
            self,
            trials,
            timeout,  # type: Optional[float]
            n_jobs,  # type: int
            catch  # type: Union[Tuple[()], Tuple[Type[Exception]]]
    ):
        # type: (...) -> None

        self.start_datetime = datetime.datetime.now()

        if n_jobs == -1:
            n_jobs = multiprocessing.cpu_count()
        n_trials = len(trials)
        if trials is not None:
            # The number of threads needs not to be larger than trials.
            n_jobs = min(n_jobs, n_trials)

            if trials == 0:
                return  # When n_jobs is zero, ThreadPool fails.

        pool = multiprocessing.pool.ThreadPool(n_jobs)  # type: ignore

        # A queue is passed to each thread. When True is received, then the thread continues
        # the evaluation. When False is received, then it quits.
        def func_child_thread(que):
            # type: (Queue) -> None

            while que.get():
                self._run_trial(trial, catch)
            self.storage.remove_session()

        que = multiprocessing.Queue(maxsize=n_jobs)  # type: ignore
        for _ in range(n_jobs):
            que.put(True)
        n_enqueued_trials = n_jobs
        imap_ite = pool.imap(func_child_thread, [que] * n_jobs, chunksize=1)

        while True:
            if timeout is not None:
                elapsed_timedelta = datetime.datetime.now() - self.start_datetime
                elapsed_seconds = elapsed_timedelta.total_seconds()
                if elapsed_seconds > timeout:
                    break

            if n_trials is not None:
                if n_enqueued_trials >= n_trials:
                    break

            try:
                que.put_nowait(True)
                n_enqueued_trials += 1
            except queue.Full:
                time.sleep(1)

        for _ in range(n_jobs):
            que.put(False)

        # Consume the iterator to wait for all threads.
        collections.deque(imap_ite, maxlen=0)
        pool.terminate()
        que.close()
        que.join_thread()

    @staticmethod
    def _get_metric(metrics):
        if metrics == 'auc' or metrics == 'roc_auc':
            return diego_metrics.roc_auc
        elif metrics == 'logloss':
            return diego_metrics.log_loss
        elif metrics == 'acc' or metrics == 'accuracy':
            return diego_metrics.accuracy
        elif metrics == 'balanced_acc' or metrics == 'balanced_accuracy':
            return diego_metrics.balanced_accuracy
        elif metrics == 'f1' or metrics == 'f1_score':
            return diego_metrics.f1
        elif metrics == 'mae':
            return diego_metrics.mean_absolute_error
        elif metrics == 'pac':
            return diego_metrics.pac_score
    
    def _run_trial(self, trial, catch, metrics='auc'):
        # type: (ObjectiveFuncType, Union[Tuple[()], Tuple[Type[Exception]]]) -> trial_module.Trial
        trial_number = trial.number
        metrics_func = self._get_metric(metrics)
        print(type(metrics_func))
        try:
            trial.clf.fit(self.storage.X_train, self.storage.y_train, metric=metrics_func)
            result = trial.clf.score(self.storage.X_test, self.storage.y_test)
        # except basic.TrialPruned as e:
            # message = 'Setting status of trial#{} as {}. {}'.format(trial_number,
            #                                                         basic.TrialState.PRUNED,
            #                                                         str(e))
            # self.logger.info(message)
            # self.storage.set_trial_state(trial_id, basic.TrialState.PRUNED)
            # return trial
        except catch as e:
            message = 'Setting status of trial#{} as {} because of the following error: {}'\
                .format(trial_number, basic.TrialState.FAIL, repr(e))
            self.logger.warning(message, exc_info=True)
            self.storage.set_trial_state(trial_number, basic.TrialState.FAIL)
            self.storage.set_trial_system_attr(
                trial_number, 'fail_reason', message)
            return trial

        try:
            # result = float(result)
            self.logger.info('Trial{} was done'.format(trial.number))
        except (
                ValueError,
                TypeError,
        ):
            message = 'Setting status of trial#{} as {} because the returned value from the ' \
                      'objective function cannot be casted to float. Returned value is: ' \
                      '{}'.format(
                          trial_number, basic.TrialState.FAIL, repr(result))
            self.logger.warning(message)
            self.storage.set_trial_state(trial_number, basic.TrialState.FAIL)
            self.storage.set_trial_system_attr(
                trial_number, 'fail_reason', message)
            return trial

        if math.isnan(result):
            message = 'Setting status of trial#{} as {} because the objective function ' \
                      'returned {}.'.format(
                          trial_number, basic.TrialState.FAIL, result)
            self.logger.warning(message)
            self.storage.set_trial_state(trial_number, basic.TrialState.FAIL)
            self.storage.set_trial_system_attr(
                trial_number, 'fail_reason', message)
            return trial

        trial.report(result)
        self.storage.set_trial_state(trial_number, basic.TrialState.COMPLETE)
        self._log_completed_trial(trial_number, result)

        return trial

    def _run_proprecess_trial(self, trial, catch):
        # TODO Preprocess Trial
        X_train, y_train = self.storage.X_train, self.storage.y_train
        X_train, y_train = trial.clf.fit_transform(X_train, y_train)
        self.storage.set_train_storage(X_train, y_train)
        # whether to do in Test set  and add to Study.pipeline
        if self.sample_method == 'lus':
            X_train, y_train = self.storage.X_train, self.storage.y_train
            X_train, y_train = self.sampler.fit_transform(X_train, y_train)
            self.storage.set_train_storage(X_train, y_train)
        if self.is_autobin:
            self.binner.fit(self.storage.X_train, self.storage.y_train)
            X_train = self.binner.transform(self.storage.X_train)
            X_test = self.binner.transform(X_test)
            self.storage.set_train_storage(X_train, self.storage.y_train)
            self.storage.set_test_storage(X_test, y_test)
            self._pipe_add(self.binner)

        trial_number = trial.number

        try:
            trial.clf.fit(self.storage.X_train, self.storage.y_train)
            result = trial.clf.score(self.storage.X_test, self.storage.y_test)
        # except basic.TrialPruned as e:
            # message = 'Setting status of trial#{} as {}. {}'.format(trial_number,
            #                                                         basic.TrialState.PRUNED,
            #                                                         str(e))
            # self.logger.info(message)
            # self.storage.set_trial_state(trial_id, basic.TrialState.PRUNED)
            # return trial
        except catch as e:
            message = 'Setting status of trial#{} as {} because of the following error: {}'\
                .format(trial_number, basic.TrialState.FAIL, repr(e))
            self.logger.warning(message, exc_info=True)
            self.storage.set_trial_state(trial_number, basic.TrialState.FAIL)
            self.storage.set_trial_system_attr(
                trial_number, 'fail_reason', message)
            return trial

        try:
            # result = float(result)
            self.logger.info('Trial{} was done'.format(trial.number))
        except (
                ValueError,
                TypeError,
        ):
            message = 'Setting status of trial#{} as {} because the returned value from the ' \
                      'objective function cannot be casted to float. Returned value is: ' \
                      '{}'.format(
                          trial_number, basic.TrialState.FAIL, repr(result))
            self.logger.warning(message)
            self.storage.set_trial_state(trial_number, basic.TrialState.FAIL)
            self.storage.set_trial_system_attr(
                trial_number, 'fail_reason', message)
            return trial

        if math.isnan(result):
            message = 'Setting status of trial#{} as {} because the objective function ' \
                      'returned {}.'.format(
                          trial_number, basic.TrialState.FAIL, result)
            self.logger.warning(message)
            self.storage.set_trial_state(trial_number, basic.TrialState.FAIL)
            self.storage.set_trial_system_attr(
                trial_number, 'fail_reason', message)
            return trial

        trial.report(result)
        self.storage.set_trial_state(trial_number, basic.TrialState.COMPLETE)
        self._log_completed_trial(trial_number, result)

        return trial

    def _log_completed_trial(self, trial_number, value):
        # type: (int, float) -> None

        self.logger.info('Finished trial#{} resulted in value: {}. '
                         'Current best value is {}.'.format(
                             trial_number, value, self.best_value))

    def _pipe_add(self, step):
        """add steps to Study.pipeline

        Arguments:
            step {[list]} -- ['name', clf]
        """

        if isinstance(step, list):
            if step is not None and not hasattr(step, "fit"):
                raise TypeError("Last step of Pipeline should implement fit. "
                                "'%s' (type %s) doesn't"
                                % (step, type(step)))
            if isinstance(step, Pipeline) and self.pipeline is None:
                self.pipeline = step
                return
        else:
            pass
        if self.pipeline is None:
            self.pipeline = make_pipeline(step)
        else:
            steps = _name_estimators([step])
            self.pipeline.steps += steps

    def _export_model(self, export_model_path):
        if export_model_path is None or export_model_path == '':
            return
            # export_model_path = '/tmp/'+model_name
        model_name = 'diego_model_' + str(self.study_name) + '.joblib'
        export_model_path = export_model_path + model_name
        joblib.dump(self.pipeline, export_model_path)

    def generate_preprocessor_trials(self, mode='fast', ttype=None):
        """generate simple trials

        Keyword Arguments:
            mode {str} -- [description] (default: {'fast'})
            ttype {[type]} -- [description] (default: {None})
        """

        import random
        preprocessor_trial = create_trial(self)
        # self.trial_list.append(new_trial)
        return preprocessor_trial

    def generate_trials(self, mode='fast', ttype=None):
        """generate simple trials

        Keyword Arguments:
            mode {str} -- [description] (default: {'fast'})
            ttype {[type]} -- [description] (default: {None})
        """

        import random
        if not ttype:
            ttype = random.choice(['autosk', 'tpot'])
        # if ttype == 'autosk':
        new_trial = self.generate_autosk_trial(mode)
        # elif ttype == 'tpot':
            # new_trial = self.generate_tpot_trial(mode)
        # self.trial_list.append(new_trial)
        return new_trial

    # TODO decorator, add trials to pipeline.
    def generate_autosk_trial(self, mode='fast', n_jobs=-1, time_left_for_this_task=3600,
                              per_run_time_limit=360,
                              initial_configurations_via_metalearning=25,
                              ensemble_size: int = 50,
                              ensemble_nbest=50,
                              ensemble_memory_limit=4096,
                              seed=1,
                              ml_memory_limit=10240,
                              include_estimators=None,
                              exclude_estimators=None,
                              include_preprocessors=None,
                              exclude_preprocessors=None,
                              resampling_strategy='holdout',
                              resampling_strategy_arguments=None,
                              tmp_folder=None,
                              output_folder=None,
                              delete_tmp_folder_after_terminate=True,
                              delete_output_folder_after_terminate=True,
                              shared_mode=False,
                              disable_evaluator_output=False,
                              get_smac_object_callback=None,
                              smac_scenario_args=None,
                              logging_config=None,):
        """[summary]

        Keyword Arguments:
            mode {str} -- [description] (default: {'fast'})
            n_jobs {int} -- [description] (default: {-1})

        Returns:
            [type] -- [description]
        """
        n_jobs = basic.get_approp_n_jobs(n_jobs)
        auto_sklearn_trial = create_trial(self)
        if mode == 'fast':
            time_left_for_this_task=120
            per_run_time_limit=30
            ensemble_size = 10
            ensemble_nbest = 3
        elif mode == 'big':
            ensemble_size=50
            ensemble_nbest=30
            ml_memory_limit=10240
            ensemble_memory_limit=4096
            time_left_for_this_task=14400
            per_run_time_limit=1440
        else:
            pass
        autosk_clf = AutoSklearnClassifier(n_jobs=n_jobs, time_left_for_this_task=time_left_for_this_task,
                                               per_run_time_limit=per_run_time_limit,
                                               initial_configurations_via_metalearning=initial_configurations_via_metalearning,
                                               ensemble_size=ensemble_size,
                                               ensemble_nbest=ensemble_nbest,
                                               ensemble_memory_limit=ensemble_memory_limit,
                                               seed=seed,
                                               ml_memory_limit=ml_memory_limit,
                                               include_estimators=include_estimators,
                                               exclude_estimators=exclude_estimators,
                                               include_preprocessors=include_preprocessors,
                                               exclude_preprocessors=exclude_preprocessors,
                                               resampling_strategy=resampling_strategy,
                                               resampling_strategy_arguments=resampling_strategy_arguments,
                                               tmp_folder=tmp_folder,
                                               output_folder=output_folder,
                                               delete_tmp_folder_after_terminate=delete_tmp_folder_after_terminate,
                                               delete_output_folder_after_terminate=delete_output_folder_after_terminate,
                                               shared_mode=shared_mode,
                                               disable_evaluator_output=disable_evaluator_output,
                                               get_smac_object_callback=get_smac_object_callback,
                                               smac_scenario_args=smac_scenario_args,
                                               logging_config=logging_config,)
        auto_sklearn_trial.clf = autosk_clf
        self.trial_list.append(auto_sklearn_trial)
        return auto_sklearn_trial

    def generate_tpot_trial(self, mode='fast', **kwargs):
        tpot_trial = create_trial(self)
        # ref: http://epistasislab.github.io/tpot/api/
        # TPOT will evaluate population_size + generations × offspring_size pipelines in total.
        if mode == 'fast':
            tpot_clf = TPOTClassifier(generations=5, population_size=10,
                                      verbosity=2, n_jobs=-1, max_eval_time_mins=10, early_stop=5)
        elif mode == 'test':
            tpot_clf = TPOTClassifier(
                generations=2, population_size=10, n_jobs=-1, verbosity=1)
        elif mode == 'self-define':
            tpot_clf = TPOTClassifier(**kwargs)
        else:
            tpot_clf = TPOTClassifier(generations=50, population_size=100,
                                      verbosity=2, scoring='accuracy', n_jobs=-1, max_eval_time_mins=60, early_stop=30)
        tpot_trial.clf = tpot_clf
        self.trial_list.append(tpot_trial)
        return tpot_trial

    def add_preprocessor_trial(self, trial):
        pass


def create_trial(study: Study):
    trial_id = study.storage.create_new_trial_id(study.study_id)
    trial = Trial(study, trial_id)
    return trial


def get_storage(storage):
    # type: (Union[None, str, BaseStorage]) -> BaseStorage

    if storage is None:
        return Storage()
    else:
        return storage


def create_study(X, y,
                 storage=None,  # type: Union[None, str, storages.BaseStorage]
                 sample_method='lus',
                 study_name=None,  # type: Optional[str]
                 direction='maximize',  # type: str
                 load_cache=False,  # type: bool
                 is_autobin=False,
                 bin_params=dict(),
                 sample_params=dict(),
                 trials_list=list(),
                 export_model_path=None,
                 ):
    # type: (...) -> Study
    """Create a new :class:`~diego.study.Study`.

    Args:
        storage:
            Database URL. If this argument is set to None, in-memory storage is used, and the
            :class:`~diego.study.Study` will not be persistent.
        sampler:
            A sampler object that implements background algorithm for value suggestion. See also
            :class:`~diego.samplers`.
        study_name:
            Study's name. If this argument is set to None, a unique name is generated
            automatically.
        is_auto_bin: do autobinning
        bin_params: binning method
    Returns:
        A :class:`~diego.study.Study` object.

    """
    X, y = check_X_y(X, y, accept_sparse='csr')
    storage = get_storage(storage)
    try:
        study_id = storage.create_new_study_id(study_name)
    except basic.DuplicatedStudyError:
        # 内存中最好study不要重名，而且可以读取已有的Study。 数据存在storage中。
        # if load_if_exists:
        #     assert study_name is not None

        #     logger = logging.get_logger(__name__)
        #     logger.info("Using an existing study with name '{}' instead of "
        #                 "creating a new one.".format(study_name))
        #     study_id = storage.get_study_id_from_name(study_name)
        # else:
        raise

    study_name = storage.get_study_name_from_id(study_id)
    study = Study(
        study_name=study_name,
        storage=storage,
        sample_method=sample_method,
        is_autobin=is_autobin,
        bin_params=bin_params,
        export_model_path=export_model_path)

    if direction == 'minimize':
        _direction = basic.StudyDirection.MINIMIZE
    elif direction == 'maximize':
        _direction = basic.StudyDirection.MAXIMIZE
    else:
        raise ValueError(
            'Please set either \'minimize\' or \'maximize\' to direction.')

    study.storage.direction = _direction
    study.storage.set_train_storage(X, y)

    return study


def load_study(
        study_name,  # type: str
        storage,  # type: Union[str, storages.BaseStorage]

):
    # type: (...) -> Study
    """Load the existing :class:`~diego.study.Study` that has the specified name.

    Args:
        study_name:
            Study's name. Each study has a unique name as an identifier.
        storage:
            Database URL such as ``sqlite:///example.db``. diego internally uses `SQLAlchemy
            <https://www.sqlalchemy.org/>`_ to handle databases. Please refer to `SQLAlchemy's
            document <https://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls>`_ for
            further details.
    """

    return Study(study_name=study_name, storage=storage)


def get_all_study_summaries(storage):
    # type: (Union[str, storages.BaseStorage]) -> List[basic.StudySummary]
    """Get all history of studies stored in a specified storage.

    Args:
        storage:
            Database URL.

    Returns:
        List of study history summarized as :class:`~diego.basic.StudySummary` objects.

    """

    storage = get_storage(storage)
    return storage.get_all_study_summaries()

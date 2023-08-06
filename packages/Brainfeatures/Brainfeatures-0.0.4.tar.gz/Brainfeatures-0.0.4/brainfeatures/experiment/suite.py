import logging
import pickle
import os

from brainfeatures.experiment.experiment import Experiment
from brainfeatures.utils.data_util import assemble_overlapping_band_limits

logger = logging.getLogger()
logger.setLevel("DEBUG")


class ExperimentSuite(object):
    def __init__(self, result_dir=None):
        self.configs = []
        self.result_dir = result_dir

    def add(self, config):
        self.configs.append(config)

    def run(self):
        for i, config in enumerate(self.configs):
            logging.info("Running experiment {}".format(i))
            print(config)
            exp = Experiment(**config)
            exp.run()

            self.save(exp, str(i))

    def _remove_features(self, exp):

        keys = list(exp._features.keys())
        for key in keys:
            exp._features[key] = []

    def save(self, exp, exp_id, include_features=False):
        if not include_features:
            self._remove_features(exp)

        if self.result_dir is not None:
            exp_dir = os.path.join(self.result_dir, exp_id)
            os.makedirs(exp_dir)
            exp_file = os.path.join(exp_dir, "exp_" + exp_id + ".pkl")
            with open(exp_file, "wb") as pickle_file:
                pickle.dump(exp, pickle_file)
            logging.info("Saved experiment to {}".format(exp_dir))


class FilterBankExperiment(Experiment):
    # can the suite be used here?
    def __init__(self, feature_generation_params, args, kwargs):
        assert "band_limits" in feature_generation_params, "no freq bands given"
        self.band_limits = feature_generation_params["band_limits"]
        if feature_generation_params["band_overlap"]:
            self.band_limits = assemble_overlapping_band_limits(
                self.band_limits)
        self.args = args
        self.kwargs = kwargs

    def run(self):
        for band_limit in self.band_limits:

            exp = Experiment(*self.args, **self.kwargs)
            exp.run()


from conf.data import Data
from conf.run import Run
from conf.run_batch import BatchRun


class Config:
    def __init__(self, default=False):
        if default:
            self.set_data()
        else:
            self.data = None
        self.run_instance = None

    def set_data(self, data_set: int = 18, mode: bool = False, number: int = 2) -> Data:
        self.data = Data(data_set, mode, number)
        return self.data

    def run(self, *args, **kwargs) -> Run:
        self.run_instance = Run(self.data, *args, **kwargs)
        return self.run_instance

    def run_batch(self, *data_sets) -> BatchRun:
        self.run_instance = BatchRun(data_sets)
        return self.run_instance

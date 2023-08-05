import copy
import csv
import glob
import os
import pickle
import random
from typing import List

import numpy as np

from .annotations import ECGAnnotation
from .sequence_data import Time, Signal
from .subject_info import SubjectInfo


class ECGRecord:
    time: Time = None
    record_name: str = None
    _signals: List[Signal] = []
    annotations: ECGAnnotation = None
    info: SubjectInfo = None

    def __eq__(self, other):
        if self.n_sig != other.n_sig:
            return False
        if self.record_name != other.record_name:
            return False
        if self._signals != other._signals:
            return False
        if self.annotations != other.annotations:
            return False
        if self.info != other.info:
            return False
        return True

    def __init__(self, name, time):
        self.record_name = name
        if not isinstance(time, Time):
            raise TypeError("time should be ECGTime")
        self.time = time
        self._signals = []

    @property
    def duration(self):
        return max(self.time)

    @property
    def n_sig(self):
        return len(self._signals)

    @property
    def p_signal(self):
        return np.array([s for s in self._signals])

    @property
    def lead_names(self):
        return [s.lead_name for s in self._signals]

    def get_lead(self, lead_name):
        try:
            return list(filter(lambda s: s.lead_name == lead_name, self._signals))[0]
        except IndexError:
            return None

    def add_signal(self, signal):
        if not isinstance(signal, Signal):
            raise TypeError("signal should be ECGSignal")
        if len(signal) != len(self):
            raise ValueError(f"len(signal) has {len(signal)} samples != len(timestamps) = {len(self.time)}")
        self._signals.append(signal)

    def __len__(self):
        return len(self.time)

    def __repr__(self):
        return f"Record {self.record_name}: {self.lead_names}"

    def __getitem__(self, item):
        new_instance = copy.copy(self)
        new_instance.time = new_instance.time.slice(item)
        new_instance._signals = [s.slice(item) for s in new_instance._signals]
        return new_instance

    @classmethod
    def from_wfdb(cls, hea_file, selected_leads=None):
        from pyecg.importers import WFDBLoader
        loader = WFDBLoader(selected_leads=selected_leads)
        return loader.load(hea_file)

    @classmethod
    def from_ishine(cls, ecg_file, selected_leads=None):
        from pyecg.importers import ISHINELoader
        loader = ISHINELoader(selected_leads=selected_leads)
        return loader.load(ecg_file)

    @classmethod
    def from_np_array(cls, name, time, signal_array, signal_names):
        new_instance = cls(name, Time.from_timestamps(time))
        if len(signal_array.shape) != 2:
            raise ValueError(f"Signal should be 2D array e.g. (3, 1000) got {signal_array.shape}")
        if signal_array.shape[0] != len(signal_names):
            raise ValueError(f"signal_array.shape[0] should match len(signal_names)")

        for signal, name in zip(signal_array, signal_names):
            new_instance.add_signal(Signal(signal=signal, lead_name=name))
        return new_instance


class RelocatableDataset:
    _dataset_dir = None

    @property
    def dataset_dir(self):
        return self._dataset_dir

    @dataset_dir.setter
    def dataset_dir(self, value):
        if os.path.isdir(value):
            self._dataset_dir = value
        else:
            raise FileNotFoundError(f"{value} is not a valid directory")


class RecordTicket(RelocatableDataset):

    def __init__(self, record_file, selected_leads=None):
        """

        :param record_file: .hea / .ecg
        :param selected_leads: if this kwarg is specified, lead names outside this list will not be loaded
        """
        self._record_file = record_file
        self._dataset_dir = os.path.dirname(record_file)
        self.selected_leads = selected_leads

    @property
    def record_base(self):
        return os.path.split(self.record_file)[1]

    @property
    def record_file(self):
        return os.path.join(self.dataset_dir, os.path.split(self._record_file)[1])

    def __call__(self, *args, **kwargs):
        """
        Call means load from disk
        :param args:
        :param kwargs:
        :return:
        """
        extension = os.path.splitext(self.record_file)[1].lower()
        if extension == "":
            file_candidates = glob.glob(self.record_file + "*.hea")
            file_candidates += glob.glob(self.record_file + "*.ecg")
            if len(file_candidates) == 0:
                raise FileNotFoundError(f"No hea/ecg file found with basename {self.record_file}")
            if len(file_candidates) > 1:
                raise ValueError(f"Too many files ({len(file_candidates)}) starts with {self.record_file}")
            extension = os.path.splitext(file_candidates[0])[1].lower()

        if extension == ".hea":
            return ECGRecord.from_wfdb(self.record_file, self.selected_leads)
        elif extension == ".ecg":
            return ECGRecord.from_ishine(self.record_file, self.selected_leads)
        else:
            raise ValueError(f"Unknown extension {extension}")

    def __repr__(self):
        return os.path.split(self._record_file)[1]

    def __eq__(self, other):
        if self.record_file == other.record_file and self.selected_leads == other.selected_leads:
            return True
        return False


class ECGDataset(RelocatableDataset):
    record_tickets: List[RecordTicket] = []
    dataset_name = None

    def __init__(self, dataset_name=None, dataset_dir=None, record_tickets: List[RecordTicket] = []):
        if not os.path.isdir(dataset_dir):
            raise FileNotFoundError(f"{dataset_dir} is not a directory")

        if dataset_name is not None:
            self.dataset_name = dataset_name
        else:
            self.dataset_name = os.path.split(dataset_dir)[1]

        self._dataset_dir = dataset_dir
        self.record_tickets = record_tickets

    @property
    def records(self):
        return [rt() for rt in self.record_tickets]

    def __iter__(self):
        return iter(self.records)

    def __getitem__(self, item):
        if isinstance(item, slice):
            return [rt() for rt in self.record_tickets[item]]
        else:
            return self.record_tickets[item]()

    def shuffle(self):
        random.shuffle(self.record_tickets)

    def slice(self, item):
        new_instance = copy.copy(self)
        new_instance.record_tickets = new_instance.record_tickets[item]
        return new_instance

    @classmethod
    def from_dir(cls, dataset_dir, selected_leads=None):
        if not os.path.isdir(dataset_dir):
            raise FileNotFoundError(f"{dataset_dir} does not exist")

        hea_files = glob.glob(os.path.join(dataset_dir, "*.hea"))
        ecg_files = glob.glob(os.path.join(dataset_dir, "*.ecg"))
        record_tickets = [RecordTicket(f, selected_leads) for f in hea_files + ecg_files]
        if len(record_tickets) == 0:
            raise FileNotFoundError(f"{dataset_dir} does not contain any valid ECG record")
        return cls(dataset_dir=dataset_dir, record_tickets=record_tickets)

    def split_dataset(self, dataset_names=None, *ratios):
        """

        :param dataset_names: ["train", "dev", "test"]
        :param ratios: 0.8, 0.1
        :return:
        """
        if sum(ratios) > 1:
            raise ValueError("Sum of ratios should be less than or equal to 1")
        if len(dataset_names) != len(ratios) + 1:
            raise ValueError("len(dataset_names) must == len(ratios) + 1")
        record_numbers = (len(self) * np.array(ratios)).astype(int).tolist()  # type:list
        record_numbers.append(len(self) - sum(record_numbers))
        output_dataset = []
        starting_index = 0
        for name, number in zip(dataset_names, record_numbers):
            ending_index = starting_index + number
            output_dataset.append(self.slice(slice(starting_index, ending_index)))
            starting_index = ending_index
        return tuple(output_dataset)

    def save_csv(self, output_file_name):
        """

        :param output_file_name: if extension is .csv, create directory and write into the file, if not assume this is directory and write into dataset_name_records.csv
        :return:
        """
        extension = os.path.splitext(output_file_name)[1].lower()
        if extension != ".csv":
            output_file_name = os.path.join(output_file_name, self.dataset_name + "_records.csv")
        try:
            os.makedirs(os.path.dirname(output_file_name))
        except OSError:
            pass

        with open(output_file_name, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, dialect="excel")
            csvwriter.writerow(["Dataset_Directory", "Base_Name"])
            for r in self.record_tickets:
                csvwriter.writerow([r.dataset_dir, r.record_base])

    def to_pickle(self, output_file_name):
        output_csv_name = os.path.splitext(output_file_name)[0] + ".csv"
        self.save_csv(output_csv_name)
        if os.path.splitext(output_file_name)[1] != ".pickle":
            raise ValueError(f"Extension of {output_file_name} must be .pickle")

        with open(output_file_name, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def from_pickle(cls, pickle_file):
        if not os.path.isfile(pickle_file):
            raise FileNotFoundError(f"{pickle_file} is not found")
        with open(pickle_file, 'rb') as f:
            return pickle.load(f)

    def __len__(self):
        return len(self.record_tickets)

    def __add__(self, other):
        new_instance = copy.copy(self)
        new_instance.record_tickets += other.record_tickets
        return new_instance

    def __repr__(self):
        record_str = '\n'.join([str(r) for r in self.record_tickets])
        return f"Dataset with records\n{record_str}"

    def __eq__(self, other):
        for s, o in zip(self.record_tickets, other.record_tickets):
            if s != o:
                return False
        return True

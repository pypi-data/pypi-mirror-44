import io
import os
import shutil
from abc import ABCMeta, abstractmethod as abstract_method

from future.utils import with_metaclass


class Batch(object):
    """Represents one batch of examples to write in the output files."""
    def __init__(self, index, examples, synonyms):
        super(Batch, self).__init__()
        self.index = index
        self.examples = examples
        self.synonyms = synonyms


class Adapter(with_metaclass(ABCMeta, object)):
    """
    Superclass for all the adapters.
    Using the list of generated examples, creates and writes
    the output file(s).
    """

    def __init__(self, batch_size=10000):# -> None:
        super(Adapter, self).__init__()
        self._batch_size = batch_size
        self._single_file_output = None  # Set up just before writing

    def write(self, output_directory, examples, synonyms):
        self._single_file_output = (len(examples) <= self._batch_size)

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        for batch in self.__generate_batch(examples, synonyms, self._batch_size):
            output_file_path = self.__get_file_name(batch, output_directory)
            with io.open(output_file_path, 'w') as output_file:
                self._write_batch(output_file, batch)

    @abstract_method
    def _get_file_extension(self):
        raise NotImplementedError()

    def __get_file_name(self, batch, output_directory):
        # pylint: disable=bad-continuation
        if self._single_file_output:
            return os.path.join(output_directory, "output." +
                                                  self._get_file_extension())
        return os.path.join(output_directory, "output." + str(batch.index) +
                                              "." + self._get_file_extension())


    @abstract_method
    def _write_batch(self, output_file_handle, batch):
        raise NotImplementedError()

    @classmethod
    def __generate_batch(cls, examples, synonyms, n=1):
        length = len(examples)
        for index, ndx in enumerate(range(0, length, n)):
            yield Batch(index, examples[ndx:min(ndx + n, length)], synonyms)

    
    @abstract_method
    def prepare_example(self, example):
        """Transforms an example into a str writable to an output file."""
        raise NotImplementedError()

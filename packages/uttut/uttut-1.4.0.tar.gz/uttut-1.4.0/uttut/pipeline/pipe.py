from typing import Dict, List
import warnings

import json

from uttut.elements import Datum

from .intermediate import Intermediate
from .ops.base import LabelAligner, Operator
from .utils import unpack_datum


class Pipe:

    """Pipe is a container for a series of operators

    Attributes:
        _steps (Operators) : a list of operator instances
        _checkpoints (strs): a list of checkpoints
    """

    def __init__(self):
        self._steps = []
        self._checkpoints = {}

    def add(self, op_name: str, op_kwargs: Dict = None, checkpoint: str = None):
        """Add op into steps based on the operation name & kwargs.

        This method creates an operator given name & kwargs, and then append it
        to steps.

        Warning: This method will be deprecated, please use `add_op`.

        Args:
            op_name (str): the class name of operator.
            op_kwargs (dict): the keyword arguments to create operator.
            checkpoint (str): the name of checkpoint.

        Raises:
            TypeError: If input_type of op isn't consistent with pipe's output_type.
            KeyError: If the checkpoint name has already been added.
        """

        warnings.warn("This method will be deprecated, please use `add_op`.", DeprecationWarning)
        if op_kwargs is None:
            op_kwargs = {}

        op = Operator.from_dict({'op_name': op_name, 'op_kwargs': op_kwargs})
        self.add_op(op, checkpoint=checkpoint)

    def add_op(self, op: Operator, checkpoint: str = None):
        """Add op into steps

        Append the input op to steps.

        Args:
            op (Operator): An operator instance to be added to steps.
            checkpoint (str): the name of checkpoint

        Raises:
            TypeError: If input_type of operator isn't consistent with pipe's output_type.
            KeyError: If the checkpoint name has already been added.
        """

        if self.steps:
            if op.input_type != self.output_type:
                raise TypeError(
                    "InputType of the step op is not valid."
                    f"Got {op.input_type}, but requires {self.output_type}",
                )
        self._steps.append(op)

        if checkpoint is not None:
            if checkpoint in self.checkpoints:
                raise KeyError(f"duplicated checkpoints: {checkpoint}")
            self._checkpoints[checkpoint] = len(self.steps)

    def __eq__(self, other):
        return (self.steps, self._checkpoints) == (other.steps, other._checkpoints)

    @property
    def steps(self):
        return self._steps

    @property
    def checkpoints(self):
        return self._checkpoints

    @property
    def output_type(self):
        if not self.steps:
            raise IndexError("Pipe is empty!")
        return self.steps[-1].output_type

    def transform(self, datum: Datum):
        """Process data based on steps

        This method processes datum according to the Pipe's steps.

        Arg:
            datum (Datum)

        Returns:
            output_sequence: transfromed sequence
            intent_labels (ints)
            entity_labels (ints)
            label_alingers: an instance of LabelAlignerSequence
            intermediate: an instance of Intermediate

        """
        input_sequence, intent_labels, entity_labels = unpack_datum(datum)
        output_sequence, label_aligners, intermediate = self.transform_sequence(input_sequence)
        updated_entity_labels = label_aligners.transform(entity_labels)

        return output_sequence, intent_labels, updated_entity_labels, label_aligners, intermediate

    def transform_sequence(self, input_sequence):
        """Process input_sequence based on steps

        This method processes input_sequence according to the Pipe's steps.

        Arg:
            input_sequence

        Returns:
            output_sequence: transfromed sequence
            label_alingers: an instance of LabelAlignerSequence
            intermediate: an instance of Intermediate

        """
        intermediate = Intermediate(self.checkpoints)

        intermediate.add(input_sequence)
        label_aligners = LabelAlignerSequence()

        for op in self.steps:
            input_sequence, label_aligner = op.transform(input_sequence)
            intermediate.add(input_sequence)
            label_aligners.add(label_aligner)

        return input_sequence, label_aligners, intermediate

    def serialize(self) -> str:
        return json.dumps({
            'steps': [op.serialize() for op in self.steps],
            'checkpoints': self.checkpoints,
        })

    @classmethod
    def deserialize(cls, serialized_str: str) -> 'Pipe':
        pipe = cls()
        pipe_bundle = json.loads(serialized_str)
        # restore steps
        for step_info in pipe_bundle['steps']:
            op = Operator.deserialize(step_info)
            pipe.add_op(op)
        # restore checkpoints
        pipe._checkpoints = pipe_bundle['checkpoints']
        return pipe


class LabelAlignerSequence:

    def __init__(self):
        self.collections = []

    def add(self, label_aligner: LabelAligner):
        """Append label_aligner into collections

        Arg:
            label_aligner: an instance of LabelAligner

        """
        self.collections.append(label_aligner)

    def transform(self, labels: List[int]) -> List[int]:
        """Update labels based on given label_aligners

        Arg:
            labels (ints): raw labels (entity)

        Return:
            ints: updated labels which has the same length as
                  transformed sequence

        """
        for label_aligner in self.collections:
            labels = label_aligner.transform(labels)
        return labels

    def inverse_transform(self, labels: List[int]) -> List[int]:
        """Realign model prediction to its original input

        Arg:
            labels (ints): model prediction (entity)

        Return:
            ints: updated labels which has the same length as
                  original input (utterance)

        """
        for label_aligner in self.collections[::-1]:
            labels = label_aligner.inverse_transform(labels)
        return labels

from typing import Protocol

from chemprop.v2.featurizers.molgraph import MolGraph


class MolGraphFeaturizerProto(Protocol):
    def __call__(self, *args, **kwargs) -> MolGraph:
        pass

    @property
    def shape(self) -> tuple[int, int]:
        """the feature dimensions of the atoms and bonds, respectively, of `MolGraph`s generated by
        this featurizer"""
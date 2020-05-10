from collections import OrderedDict

from torch.utils.data import Subset

from catalyst.contrib.data.dataset import Compose, MNIST, Normalize, ToTensor
from catalyst.dl import ConfigExperiment


class Experiment(ConfigExperiment):
    """
    @TODO: Docs. Contribution is welcome
    """

    @staticmethod
    def get_transforms(stage: str = None, mode: str = None):
        """
        @TODO: Docs. Contribution is welcome
        """
        return Compose([ToTensor(), Normalize((0.1307,), (0.3081,))])

    def get_datasets(self, stage: str, n_samples: int = 320, **kwargs):
        """
        @TODO: Docs. Contribution is welcome
        """
        datasets = OrderedDict()

        if stage != "infer":
            trainset = MNIST(
                "./data",
                train=False,
                download=True,
                transform=Experiment.get_transforms(stage=stage, mode="train"),
            )
            testset = MNIST(
                "./data",
                train=False,
                download=True,
                transform=Experiment.get_transforms(stage=stage, mode="valid"),
            )
            if n_samples > 0:
                trainset = Subset(trainset, list(range(n_samples)))
                testset = Subset(testset, list(range(n_samples)))
            datasets["train"] = trainset
            datasets["valid"] = testset
        else:
            testset = MNIST(
                "./data",
                train=False,
                download=True,
                transform=Experiment.get_transforms(stage=stage, mode="valid"),
            )
            if n_samples > 0:
                testset = Subset(testset, list(range(n_samples)))
            datasets["infer"] = testset

        return datasets

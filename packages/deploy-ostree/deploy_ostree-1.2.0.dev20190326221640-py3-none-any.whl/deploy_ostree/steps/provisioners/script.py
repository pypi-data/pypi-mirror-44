# Copyright 2018, 2019 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from ...config import Config, ScriptProvisionerConfig
from . import DeployStep
from ...run import run


class ScriptProvisioner(DeployStep):
    def __init__(self, config: Config, provisioner: ScriptProvisionerConfig) -> None:
        self.config = config
        self.provisioner = provisioner

    @property
    def title(self) -> str:
        return 'Provisioning: script[%s]' % self.provisioner.interpreter

    def run(self):
        run(
            [self.provisioner.interpreter],
            input=self.provisioner.script,
            cwd=self.config.deployment_dir
        )

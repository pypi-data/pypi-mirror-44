from ..core.basejob import MultiJob
from ..core.results import Results
from ..core.settings import Settings
from ..mol.molecule import Molecule
from ..interfaces.adfsuite.adf import ADFJob


__all__ = ['ADFFragmentJob', 'ADFFragmentResults']


class ADFFragmentResults(Results):

    def get_properties(self):
        return self.job.full.results.get_properties()

    def get_main_molecule(self):
        return self.job.full.results.get_main_molecule()

    def get_input_molecule(self):
        return self.job.full.results.get_input_molecule()

    def get_energy(self, unit='au'):
        return self.job.full.results.get_energy(unit)

    def get_dipole_vector(self, unit='au'):
        return self.job.full.results.get_dipole_vector(unit)

    def get_energy_decomposition(self, unit='au'):
        return self.job.full.results.get_energy_decomposition(unit)


class ADFFragmentJob(MultiJob):
    _result_type = ADFFragmentResults

    def __init__(self, fragment1=None, fragment2=None, full_settings=None, **kwargs):
        MultiJob.__init__(self, **kwargs)
        self.fragment1 = fragment1.copy() if isinstance(fragment1, Molecule) else fragment1
        self.fragment2 = fragment2.copy() if isinstance(fragment2, Molecule) else fragment2
        self.full_settings = full_settings or Settings()

    def prerun(self):
        self.f1 = ADFJob(name=self.name+'_f1', molecule=self.fragment1, settings=self.settings)
        self.f2 = ADFJob(name=self.name+'_f2', molecule=self.fragment2, settings=self.settings)

        for at in self.fragment1:
            at.properties.adf.fragment = 'subsystem1'
        for at in self.fragment2:
            at.properties.adf.fragment = 'subsystem2'

        self.full = ADFJob(name = self.name + '_full',
            molecule = self.fragment1 + self.fragment2,
            settings = self.settings + self.full_settings)
        self.full.settings.input.fragments.subsystem1 = self.f1
        self.full.settings.input.fragments.subsystem2 = self.f2

        self.children = [self.f1, self.f2, self.full]



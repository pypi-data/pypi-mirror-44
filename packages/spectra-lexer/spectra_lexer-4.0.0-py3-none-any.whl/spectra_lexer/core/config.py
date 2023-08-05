from typing import Dict, Optional

from spectra_lexer import Component
from spectra_lexer.file import CFG


class ConfigManager(Component):
    """ Configuration parser for the Spectra program. """

    file = Resource("cmdline", "config-file", "~/config.cfg", "CFG file with config settings to load at startup.")

    @on("load_dicts", pipe_to="set_dict_config")
    @on("config_load", pipe_to="set_dict_config")
    def load(self, filename:str="") -> Optional[Dict[str, dict]]:
        """ Load all config options from disk. Ignore failures and convert strings using AST. """
        try:
            d = CFG.load(filename or self.file)
        except OSError:
            return None
        self._update_components(d)
        return d

    @on("config_save")
    def save(self, d:Dict[str, dict], filename:str="") -> None:
        """ Send a new set of config values to the components and save them to disk.
            Saving should not fail silently, unlike loading. If no save filename is given, use the default. """
        self._update_components(d)
        CFG.save(filename or self.file, d)

    def _update_components(self, d:Dict[str, dict]) -> None:
        """ Update all active components with values from the given dict. """
        for sect, page in d.items():
            for name, val in page.items():
                self.engine_call(f"set_config_{sect}:{name}", val)

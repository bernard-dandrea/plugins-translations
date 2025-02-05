import json
import os
from pathlib import Path
import pytest

from plugintranslations.translator import PluginTranslator
from plugintranslations.consts import (
    EN_US,
    FR_FR,
    ES_ES,
    DE_DE,
    PLUGIN_ROOT,
    INPUT_SOURCE_LANGUAGE,
    INPUT_TARGET_LANGUAGES,
    INPUT_INCLUDE_EMPTY_TRANSLATION,
    INPUT_USE_CORE_TRANSLATIONS,
    INPUT_GENERATE_SOURCE_LANGUAGE_TRANSLATIONS,
    INPUT_DEBUG,
)


class TestTranslatePlugin():
    # Arrange
    @pytest.fixture(scope="session", autouse=True)
    def current_working_dir(self, tmp_path_factory) -> Path:
        _cwd = tmp_path_factory.mktemp("plugin_root")
        return _cwd

    @pytest.fixture(autouse=True)
    def os_config(self):
        os.environ[INPUT_SOURCE_LANGUAGE] = FR_FR
        os.environ[INPUT_TARGET_LANGUAGES] = f'{EN_US},{ES_ES},{DE_DE}'
        os.environ[INPUT_INCLUDE_EMPTY_TRANSLATION] = 'False'
        os.environ[INPUT_USE_CORE_TRANSLATIONS] = 'False'
        os.environ[INPUT_GENERATE_SOURCE_LANGUAGE_TRANSLATIONS] = 'False'
        os.environ[INPUT_DEBUG] = 'True'

    @pytest.fixture(autouse=True)
    def info_json(self, current_working_dir: Path):
        plugin_info_root = current_working_dir/PLUGIN_ROOT/"plugin_info"
        plugin_info_root.mkdir(parents=True, exist_ok=True)
        assert plugin_info_root.exists()

        info_json_content = {}
        info_json_content['language'] = [FR_FR, EN_US, ES_ES, DE_DE]
        info_json_content['id'] = 'fake_plugin'

        info_json_file = plugin_info_root/'info.json'
        info_json_file.write_text(json.dumps(info_json_content, ensure_ascii=False, indent='\t'), encoding="UTF-8")

    def test_translate_plugin(self, current_working_dir):
        self._test_translate = PluginTranslator(current_working_dir)
        assert self._test_translate is not None
        assert isinstance(self._test_translate, PluginTranslator)

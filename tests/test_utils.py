#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import unittest

import ftransc.utils as futils


class UtilsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture_filename = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fixtures', 'presets.json'))
        with open(fixture_filename) as fd:
            cls.presets = json.load(fd)

    def test_presets(self):
        for audio_format, preset in self.presets.items():
            is_external = audio_format.endswith('_ext')
            audio_format = audio_format.split('_')[0]
            for audio_quality, quality_preset in preset.items():
                self.assertEqual(futils.get_audio_presets(audio_format, audio_quality, is_external), quality_preset)


if __name__ == '__main__':
    unittest.main()

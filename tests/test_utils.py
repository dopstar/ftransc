#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import json
import logging
import unittest
import datetime
from collections import deque

import ftransc.utils as futils


class UtilsTestCase(unittest.TestCase):
    def test_get_audio_presets__mp3_normal_internal(self):
        self.assertEqual(futils.get_audio_presets('mp3'), u'-vn -ac 2 -acodec libmp3lame -aq 4')
        self.assertEqual(futils.get_audio_presets('mp3', 'normal'), u'-vn -ac 2 -acodec libmp3lame -aq 4')

    def test_get_audio_preset__mp3_insane_internal(self):
        self.assertEqual(futils.get_audio_presets('mp3', 'insane'), u'-vn -ac 2 -acodec libmp3lame -ab 320k')
    
    def test_get_audio_preset__mp3_extreme_internal(self):
        self.assertEqual(futils.get_audio_presets('mp3', 'extreme'), u'-vn -ac 2 -acodec libmp3lame -aq 0')

    def test_get_audio_preset__mp3_high_internal(self):
        self.assertEqual(futils.get_audio_presets('mp3', 'high'), u'-vn -ac 2 -acodec libmp3lame -aq 2')

    def test_get_audio_preset__mp3_low_internal(self):
        self.assertEqual(futils.get_audio_presets('mp3', 'low'), u'-vn -ac 2 -acodec libmp3lame -aq 9')

    def test_get_audio_preset__mp3_tiny_internal(self): 
        self.assertEqual(futils.get_audio_presets('mp3', 'tiny'), u'-vn -ac 1 -acodec libmp3lame -ab 32k -ar 32000')


if __name__ == '__main__':
    unittest.main()

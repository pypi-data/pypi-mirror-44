# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
import unittest
import xml

import pytest

from pymediainfo import MediaInfo

os_is_nt = os.name in ("nt", "dos", "os2", "ce")

if sys.version_info < (3, 3):
    FileNotFoundError = IOError

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

class MediaInfoTest(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(data_dir, 'sample.xml'), 'r') as f:
            self.xml_data = f.read()
        self.mi = MediaInfo(self.xml_data)
    def test_populate_tracks(self):
        self.assertEqual(4, len(self.mi.tracks))
    def test_valid_video_track(self):
        for track in self.mi.tracks:
            if track.track_type == 'Video':
                self.assertEqual('DV', track.codec)
                self.assertEqual('Interlaced', track.scan_type)
                break
    def test_track_integer_attributes(self):
        for track in self.mi.tracks:
            if track.track_type == 'Audio':
                self.assertTrue(isinstance(track.duration, int))
                self.assertTrue(isinstance(track.bit_rate, int))
                self.assertTrue(isinstance(track.sampling_rate, int))
                break
    def test_track_other_attributes(self):
        for track in self.mi.tracks:
            if track.track_type == 'General':
                self.assertEqual(5, len(track.other_file_size))
                self.assertEqual(4, len(track.other_duration))
                break
    def test_load_mediainfo_from_string(self):
        self.assertEqual(4, len(self.mi.tracks))
    def test_getting_attribute_that_doesnot_exist(self):
        self.assertTrue(self.mi.tracks[0].does_not_exist is None)

class MediaInfoInvalidXMLTest(unittest.TestCase):
    def setUp(self):
        if sys.version_info < (2, 7):
            self._exc_class = xml.parsers.expat.ExpatError
        else:
            self._exc_class = xml.etree.ElementTree.ParseError
        with open(os.path.join(data_dir, 'invalid.xml'), 'r') as f:
            self.xml_data = f.read()
    def test_parse_invalid_xml(self):
        self.assertRaises(self._exc_class, MediaInfo, self.xml_data)

class MediaInfoLibraryTest(unittest.TestCase):
    def setUp(self):
        self.mi = MediaInfo.parse(os.path.join(data_dir, "sample.mp4"))
    def test_can_parse_true(self):
        self.assertTrue(MediaInfo.can_parse())
    def test_track_count(self):
        self.assertEqual(len(self.mi.tracks), 3)
    def test_track_types(self):
        self.assertEqual(self.mi.tracks[1].track_type, "Video")
        self.assertEqual(self.mi.tracks[2].track_type, "Audio")
    def test_track_details(self):
        self.assertEqual(self.mi.tracks[1].format, "AVC")
        self.assertEqual(self.mi.tracks[2].format, "AAC")
        self.assertEqual(self.mi.tracks[1].duration, 958)
        self.assertEqual(self.mi.tracks[2].duration, 980)

class MediaInfoUnicodeXMLTest(unittest.TestCase):
    def setUp(self):
        self.mi = MediaInfo.parse(os.path.join(data_dir, "sample.mkv"))
    def test_parse_file_with_unicode_tags(self):
        self.assertEqual(
            self.mi.tracks[0].title,
            "Dès Noël où un zéphyr haï me vêt de glaçons "
            "würmiens je dîne d’exquis rôtis de bœuf au kir à "
            "l’aÿ d’âge mûr & cætera !"
        )

class MediaInfoUnicodeFileNameTest(unittest.TestCase):
    def setUp(self):
        self.mi = MediaInfo.parse(os.path.join(data_dir, "accentué.txt"))
    def test_parse_unicode_file(self):
        self.assertEqual(len(self.mi.tracks), 1)

class MediaInfoURLTest(unittest.TestCase):
    def setUp(self):
        self.mi = MediaInfo.parse("https://github.com/sbraz/pymediainfo/blob/master/tests/data/sample.mkv?raw=true")
    def test_parse_url(self):
        self.assertEqual(len(self.mi.tracks), 2)

class MediaInfoPathlibTest(unittest.TestCase):
    def setUp(self):
        self.pathlib = pytest.importorskip("pathlib")
    def test_parse_pathlib_path(self):
        path = self.pathlib.Path(data_dir) / "sample.mp4"
        mi = MediaInfo.parse(path)
        self.assertEqual(len(mi.tracks), 3)
    @pytest.mark.skipif(os_is_nt, reason="Windows paths are URLs")
    def test_parse_non_existent_path_pathlib(self):
        path = self.pathlib.Path(data_dir) / "this file does not exist"
        self.assertRaises(FileNotFoundError, MediaInfo.parse, path)

class MediaInfoTestParseNonExistentFile(unittest.TestCase):
    @pytest.mark.skipif(os_is_nt, reason="Windows paths are URLs")
    def test_parse_non_existent_path(self):
        path = os.path.join(data_dir, "this file does not exist")
        self.assertRaises(FileNotFoundError, MediaInfo.parse, path)

class MediaInfoCoverDataTest(unittest.TestCase):
    def setUp(self):
        self.mi = MediaInfo.parse(
                os.path.join(data_dir, "sample_with_cover.mp3"),
                cover_data=True
        )
    def test_parse_cover_data(self):
        self.assertEqual(
                self.mi.tracks[0].cover_data,
                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACXBIWXMAAAAAAA"
                "AAAQCEeRdzAAAADUlEQVR4nGP4x8DwHwAE/AH+QSRCQgAAAABJRU5ErkJggg=="
        )

class MediaInfoTrackParsingTest(unittest.TestCase):
    def test_track_parsing(self):
        mi = MediaInfo.parse(os.path.join(data_dir, "issue55.flv"))
        self.assertEqual(len(mi.tracks), 2)

class MediaInfoRuntimeErrorTest(unittest.TestCase):
    def test_parse_invalid_url(self):
        # This is the easiest way to cause a parsing error
        # since non-existent files return a different exception
        self.assertRaises(RuntimeError, MediaInfo.parse,
                "unsupportedscheme://")

class MediaInfoSlowParseTest(unittest.TestCase):
    def setUp(self):
        self.mi = MediaInfo.parse(
                os.path.join(data_dir, "vbr_requires_parsespeed_1.mp4"),
                parse_speed=1
        )
    def test_slow_parse_speed(self):
        self.assertEqual(self.mi.tracks[2].stream_size, "3353 / 45")

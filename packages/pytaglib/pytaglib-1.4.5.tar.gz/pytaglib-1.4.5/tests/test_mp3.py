# -*- coding: utf-8 -*-
# Copyright 2011-2016 Michael Helmling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation
#
from __future__ import unicode_literals
import taglib
from . import copy_test_file


def test_remove_genre_frame_from_mp3(tmpdir):
    """See https://bugs.kde.org/show_bug.cgi?id=298183
    """
    f = copy_test_file('rare_frames.mp3', tmpdir)
    tfile = taglib.File(f)
    assert 'GENRE' in tfile.tags
    assert len(tfile.tags['GENRE']) == 1

    del tfile.tags['GENRE']
    tfile.save()
    tfile.close()

    tfile = taglib.File(f)
    assert 'GENRE' not in tfile.tags
    tfile.close()


def test_remove_title_frame_from_mp3(tmpdir):
    """See https://bugs.kde.org/show_bug.cgi?id=298183."""
    f = copy_test_file('r2.mp3', tmpdir)
    tfile = taglib.File(f)
    assert 'TITLE' in tfile.tags
    assert len(tfile.tags['TITLE']) == 1

    del tfile.tags['TITLE']
    tfile.save()
    tfile.close()

    tfile = taglib.File(f)
    assert 'TITLE' not in tfile.tags
    tfile.close()


def test_id3v1_is_converted_to_v2_on_save(tmpdir):
    f = copy_test_file('onlyv1.mp3', tmpdir)
    tfile = taglib.File(f)
    assert 'ARTIST' in tfile.tags
    assert tfile.tags['ARTIST'][0] == 'Bla'
    tfile.tags['NONID3V1'] = ['omg', 'wtf']
    ret = tfile.save()
    assert len(ret) == 0
    tfile.close()

    tfile = taglib.File(f)
    assert 'NONID3V1' in tfile.tags
    tfile.close()

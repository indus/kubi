import pytest

from kubi.kubi import main, run, parse_args
import os
import sys
import glob

os.environ['PATH'] =  'C:/Program Files/vips-dev-8.10/bin' + ';' + os.environ['PATH']

import pyvips

__author__ = "Keim, Stefan"
__copyright__ = "Keim, Stefan"
__license__ = "MIT"

path_in =  './tests/in/'
path_out =  './tests/out/'



def test_parse_args(capsys):
    
    args0 = parse_args(['srcfile'])
    assert args0.co != None

    args1 = parse_args(['-co', 'compression=lzw', 'srcfile'])
    assert args1.co['compression'] == 'lzw'
    
    args2 = parse_args(['-co', 'lzw', '-co', 'predictor=horizontal', 'srcfile'])
    assert args2.co['compression'] == 'lzw' and args2.co['predictor'] == 'horizontal'

    parse_args([])
    captured = capsys.readouterr()
    assert "error: 'srcfile' or 'dstindex' has to be set" in captured.out

    parse_args(['--io', 'nosize'])
    captured = capsys.readouterr()
    assert "error: to write 'dstindex' without 'src' you have to set 'size' (-s)" in captured.out

    parse_args(['--ii', 'nosize', '-s', '999', 'somesrc'])
    captured = capsys.readouterr()
    assert "error: 'size', 'transform', 'flip' and 'layout' is already baked into the 'srcindex'; please remove the arguments" in captured.out


def test_run(capsys):

    args = ['', '-v','--vips','some/path/to/vips/bin', 'does_not_exist.tif']
    print('\nargs:  '+' '.join(args))
    sys.argv = args
    run()
    captured = capsys.readouterr()
    assert 'does_not_exist.tif: No such file or directory' in captured.out
    assert 'some/path/to/vips/bin;' in os.environ['PATH']

def test_main_none_io(capsys):
    args = ['--io', path_out + 'idx_none', path_in+'basemap.tif', path_out+'basemap_none.jpg']
    print('\nargs:  '+' '.join(args))
    main(args)
    
    dst_names = glob.glob(path_out+"*_none*.jpg")
    assert len(dst_names) == 6
    dst0 = pyvips.Image.new_from_file(dst_names[0])
    assert dst0.width == dst0.height == 1024
    assert dst0.bands == 3

def test_main_none_ii(capsys):
    args = ['--ii', path_out + 'idx_none', path_in+'base*.tif', path_out+'multi.png']
    print('\nargs:  '+' '.join(args))
    main(args)
    
    dst_names = glob.glob(path_out+"*multi*.png")
    assert len(dst_names) == 12
    dst0 = pyvips.Image.new_from_file(dst_names[0])
    assert dst0.width == dst0.height == 1024
    assert dst0.bands == 3


def test_main_none_inplace(capsys):
    os.chdir(path_out)
    args = ['-s', '256', '-t', 'eac', 'bm.tif']
    print('\nargs:  '+' '.join(args))
    main(args)
    os.chdir("./../..")
    dst_names = glob.glob(path_out+"*eac*.tif")
    assert len(dst_names) == 6
    dst0 = pyvips.Image.new_from_file(dst_names[0])
    assert dst0.width == dst0.height == 256

def test_main_none_sub(capsys):
    args = ['-s', '256', '-t', 'otc', path_out+'bm.tif', path_out+'sub/warped.png']
    print('\nargs:  '+' '.join(args))
    main(args)
    
    dst_names = glob.glob(path_out+"sub/*warped*.png")
    assert len(dst_names) == 6
    dst0 = pyvips.Image.new_from_file(dst_names[0])
    assert dst0.width == dst0.height == 256

def test_main_column_ii(capsys):
    args = ['-l','column', '--io', path_out + 'idx_column', path_in+'basemap.tif', path_out+'basemap_column.png']
    print('\nargs:  '+' '.join(args))
    main(args)

    dst_names = glob.glob(path_out+"*_column*.png")
    assert len(dst_names) == 1
    dst0 = pyvips.Image.new_from_file(dst_names[0])
    assert dst0.width == 1024 and dst0.height == 1024 * 6

def test_main_column_io(capsys):
    args = ['--ii', path_out + 'idx_column', path_in+'baseoverlay.tif', path_out+'baseoverlay_column']
    print('\nargs:  '+' '.join(args))
    main(args)

    dst_names = glob.glob(path_out+"baseoverlay_column.tif")
    assert len(dst_names) == 1
    dst0 = pyvips.Image.new_from_file(dst_names[0])
    assert dst0.width == 1024 and dst0.height == 1024 * 6

def test_main_row_multi(capsys):
    args = ['-l','row', '-s','512','-i','both','-t','eac', path_in+'base*.tif', path_out+'basemap_row.png']
    print('\nargs:  '+' '.join(args))
    main(args)

    dst_names = glob.glob(path_out+"*_row*.png")
    assert len(dst_names) == 2
    dst0 = pyvips.Image.new_from_file(dst_names[0])
    assert dst0.width == 512 * 6 and dst0.height == 512

def test_main_crossL(capsys):
    args = ['-l','crossL','-i','horizontal', path_in+'basemap.tif', path_out+'basemap_crossL.png']
    print('\nargs:  '+' '.join(args))
    main(args)

    dst_names = glob.glob(path_out+"*_crossL*.png")
    assert len(dst_names) == 1
    dst0 = pyvips.Image.new_from_file(dst_names[0])
    assert dst0.width == 1024 * 4 and dst0.height == 1024 * 3

def test_main_crossR(capsys):
    args = ['-l','crossR','-t','otc', path_in+'basemap.tif', path_out+'basemap_crossR.png']
    print('\nargs:  '+' '.join(args))
    main(args)

    dst_names = glob.glob(path_out+"*_crossR*.png")
    assert len(dst_names) == 1
    dst0 = pyvips.Image.new_from_file(dst_names[0])
    assert dst0.width == 1024 * 4 and dst0.height == 1024 * 3

def test_main_crossH(capsys):
    args = ['-l','crossH', path_in+'basemap.tif', path_out+'basemap_crossH.png']
    print('\nargs:  '+' '.join(args))
    main(args)

    dst_names = glob.glob(path_out+"*_crossH*.png")
    assert len(dst_names) == 1
    dst0 = pyvips.Image.new_from_file(dst_names[0])
    assert dst0.width == 1024 * 3 and dst0.height == 1024 * 4

def test_main_crossH(capsys):
    args = ['-l','crossH', path_in+'basemap.tif', path_out+'basemap_crossH.png']
    print('\nargs:  '+' '.join(args))
    main(args)

    dst_names = glob.glob(path_out+"*_crossH*.png")
    assert len(dst_names) == 1
    dst0 = pyvips.Image.new_from_file(dst_names[0])
    assert dst0.width == 1024 * 3 and dst0.height == 1024 * 4

def test_main_tiled(capsys):
    args = ['-co','tile_size=512','-co','depth=onetile','-co','overlap=0','-co','suffix=.jpg[Q=75]',path_in+'basemap.tif',path_out+'tiled\dstfile.dz']
    print('\nargs:  '+' '.join(args))
    main(args)

    dst_names = glob.glob(path_out+"tiled/**/*", recursive=True)
    assert len(dst_names) == 54





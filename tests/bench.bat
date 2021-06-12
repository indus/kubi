hyperfine.exe -r 5 -L s 1024,2048,4096 ^
"kubi -s {s} -co lzw -l crossL tests\in\basemap.tif tests\out\cross_kubi_{s}.tif" "python tests\in\convert360.py --convert e2c --w {s} --i tests\in\basemap.tif --o tests\out\cross_convert360_{s}.tif" 

::hyperfine.exe -r 5 -L s 1024,2048,4096 ^
::"kubi -s {s} .\tests\in\basemap.jpg .\tests\out\kubi_{s}\basemap" ".\tests\in\panorama_windows.exe -l {s} -i .\tests\in\basemap.jpg -o .\tests\out\panorama_{s}"

::hyperfine.exe -r 3 -L x 1,2,3,5,10,20 ^
::"kubi -s 2048 -co lzw -x {x} -l crossL tests\in\basemap*.tif tests\out\cross_kubi_{x}.tif"
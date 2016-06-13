# bash ftpcompile.sh lp0364d adc
# bash ftpcompile.sh i5bch1b8p1 adc
MYPWD=$(<$HOME/.ftprc)
ftp -i -n -v $1 << ftp_end
user $2 $MYPWD

quote namefmt 1

bin
mkdir /home/ADC/python
mkdir /home/ADC/python/itoolkit_egg
mkdir /home/ADC/python/itoolkit_egg/itoolkit
mkdir /home/ADC/python/itoolkit_egg/itoolkit/rest
mkdir /home/ADC/python/itoolkit_egg/itoolkit/db2
mkdir /home/ADC/python/itoolkit_egg/itoolkit/lib
mkdir /home/ADC/python/itoolkit_egg/itoolkit/test
mkdir /home/ADC/python/itoolkit_egg/itoolkit/doc
mkdir /home/ADC/python/itoolkit_egg/itoolkit/sample

cd /home/ADC/python/itoolkit_egg
put README
mput *.sh
mput *.py
cd /home/ADC/python/itoolkit_egg/itoolkit
lcd itoolkit
put README
put LICENSE
mput *.py
cd /home/ADC/python/itoolkit_egg/itoolkit/rest
lcd rest
mput *.py
cd /home/ADC/python/itoolkit_egg/itoolkit/db2
lcd ../db2
mput *.py
cd /home/ADC/python/itoolkit_egg/itoolkit/lib
lcd ../lib
mput *.c
mput *.py
cd /home/ADC/python/itoolkit_egg/itoolkit/test
lcd ../test
put README
mput *.py
cd /home/ADC/python/itoolkit_egg/itoolkit/doc
lcd ../doc
put README
cd /home/ADC/python/itoolkit_egg/itoolkit/sample
lcd ../sample
put README
mput *.py

quit

ftp_end


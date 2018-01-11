#!/bin/sh
#
# main
#
opr="error"
for arg in "$@"
{
  case "$arg" in
    34-lite)
      opr="ok"
      python3 setup.py build_ext --disable-libcall bdist_egg
    ;;
    27-lite)
      opr="ok"
      python2 setup.py build_ext --disable-libcall bdist_egg
    ;;
    26-lite)
      opr="ok"
      python setup.py build_ext --disable-libcall bdist_egg
    ;;
    34)
      opr="ok"
      python3 setup.py bdist_egg
    ;;
    27)
      opr="ok"
      python2 setup.py bdist_egg
    ;;
    26)
      opr="ok"
      python setup.py bdist_egg
    ;;
    *)
      break
    ;;
  esac
}
case "$opr" in
  error)
    echo "./$(basename $0) [34|27|26|34-lite|27-lite|26-lite]"
  ;;
esac


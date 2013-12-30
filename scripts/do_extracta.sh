#!/usr/bin/sh

# /cygdrive/c/OrCAD/OrCAD_16.6_Lite/tools/pcb/bin/extracta.exe *.brd mfg/bin/CircuitCAM/Xtrctnet.cmd foo.txt
#  see:  /Volumes/C/OrCAD/OrCAD_16.6_Lite/share/pcb/text/views  for more stuff

#/cygdrive/c/OrCAD/OrCAD_16.6_Lite/tools/pcb/bin/extracta.exe *.brd fabmaster.txt FooA.txt FooB.txt FooC.txt FooD.txt FooE.txt FooF.txt FooG.txt FooH.txt FooI.txt

EXTRACTA="/cygdrive/c/OrCAD/OrCAD_16.6_Lite/tools/pcb/bin/extracta.exe"
BRD="../eval_boards/bbb_a6a/BeagleBone_Black_RevB6_nologo.brd"
DIR=`dirname $BRD`
NAME=`basename $BRD .brd`
OUT="${DIR}/${NAME}.fab"

## this file tells extracta what sections and data to include
FABMASTER="fabmaster.txt.2"

$EXTRACTA $BRD $FABMASTER FooA.txt FooB.txt FooC.txt FooD.txt FooE.txt FooF.txt FooG.txt FooH.txt

echo "Converting ${NAME}.brd ---> ${OUT}"
cat Foo?.txt > ${OUT}

rm Foo?.txt
rm extract.log


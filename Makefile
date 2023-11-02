VERSION=00
VERSION_PREC=$$(($(VERSION)-1))
VERSION_PREC_PRT=$(shell printf "%02d" ${VERSION_PREC} )
NAME=draft-claise-yang-full-include

all:
	cd builder; python3 build_draft.py ${VERSION}
	LOCALE="EN_us.utf8" xml2rfc ${NAME}-${VERSION}.xml 
	rfcdiff ${NAME}-${VERSION_PREC_PRT}.txt  ${NAME}-${VERSION}.txt

clean:
	${RM} *.txt *.xml

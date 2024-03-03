VERSION=02
VERSION_PREC=$$(($(VERSION)-1))
VERSION_PREC_PRT=$(shell printf "%02d" ${VERSION_PREC} )
NAME=draft-quijou-netmod-yang-full-include

all:
	cd builder; python3 build_draft.py ${VERSION}
	LOCALE="EN_us.utf8" xml2rfc ${NAME}-${VERSION}.xml
	cp ${NAME}-${VERSION}.txt docs/latest.txt
	iddiff ${NAME}-${VERSION_PREC_PRT}.txt  ${NAME}-${VERSION}.txt > docs/latest-diff.html

clean:
	${RM} *.txt *.xml

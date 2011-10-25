#!/bin/sh

API_DOCS_DIR="../api_docs/python"

if [ ! -d $API_DOCS_DIR ]
    then 
        echo "creating $API_DOCS_DIR"
    mkdir -p $API_DOCS_DIR
fi

epydoc --no-private \
    --no-frames \
    --no-sourcecode \
    --name mapnik2 \
    --url http://mapnik.org \
    --css mapnik_epydoc.css \
    ../../bindings/python/mapnik \
    -o $API_DOCS_DIR

exit $?

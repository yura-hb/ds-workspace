
SRC_IMP_PATH=src/shared/pipelines/$1
DST_IMP_PATH=src/shared/pipelines/$2

SRC_TEST_PATH=src/tests/pipelines/$1
DST_TEST_PATH=src/tests/pipelines/$2

SRC_PARAMETER_PATH=conf/base/parameters/$1.yml
DST_PARAMETER_PATH=conf/base/paramters/$2.yml

mkdir -p $(dirname $DST_IMP_PATH)
mkdir -p $(dirname $DST_TEST_PATH)
mkdir -p $(dirname $DST_TEST_PATH)

mv $SRC_IMP_PATH "${DST_IMP_PATH}" 2>/dev/null
mv "$SRC_TEST_PATH" "${DST_TEST_PATH}" 2>/dev/null
mv "SRC_PARAMETER_PATH" "${DST_PARAMETER_PATH}" 2>/dev/null

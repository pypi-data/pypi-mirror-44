Thes are the mitogenome related sources including MITOS and other (more or less) helpful tools. Note that some of the tools are unfinished and not in a production state.

Clearly this README is a stub. We are happy to extend the documentation on request. So just send a message if you need further information.

Installation
============

There are three ways to install. Prefered is the installation via conda since this also takes care of non-python requirements of the main mitos script.

1. via conda: `conda install mitos -c bioconda -m -n mitos`
2. via pip: `pip install mitos`
3. manual: pip -r requirements.txt

For the non-python requirements see README.MITOS.

MITOS
=====

* runmitos.py: standalone CLI MITOS

see also `mitos.py --help` README.MITOS


genbank file handling
=====================

* refseqsplit:
    - splits a file consisting of concatenated gb files into single genbank files
    - its possible to apply filters (taxonomy, prefix)

skewness related programs
=========================

* skew:
	compute skewness values for a gene of given genbank files
* skewcum:
	compute cumulative skewness for given genbank files
* skewsvm:
	do svm classification of skewness values .. and try to relate misclassifications to rearrangements

MISC
====

* gcpp
	- pretty print and compare genetic code

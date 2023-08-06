.. _coverage:

========
coverage
========

*coverage* module contain several functions which allow to get the coverages from data input, a
:class:`craw.wig.Genome` object or a :class:`pysam.AlignmentFile`.

There is 2 kind of functions:

- the functions to get coverage from input.
- the functions to process the coverage.

Functions to get coverage
=========================

These low level functions are not aimed to be called directly.
They are called inside function which process the coverages.

get_raw_bam_coverage
--------------------

Get coverage from `pysam` for reference (*chromosome*) for an interval of positions, a quality on both strand.
and convert the coverage return by `pysam`. A score on each position for each base (ACGT)) in a global coverage for this
position.

This function is called for each entry of the annotation file.


get_raw_wig_coverage
--------------------

Get coverage from :class:`craw.wig.Genome` instance for reference (*chromosome*) for an interval of positions, on both strand.
The quality parameter is here just to have the same signature as get_bam_coverage but will be ignores .

This function is called for each entry of the annotation file.

get_raw_coverage_function
-------------------------

Allow to choose the right *get_raw_(\*)_coverage* in function of the data input type
(:class:`craw.wig.Genome`, :class:`pysam.AlignmentFile`)


.. automodule:: craw.coverage
    :members: get_raw_wig_coverage, get_raw_bam_coverage, get_raw_coverage_function
    :private-members:
    :special-members:



Functions to process coverages
==============================

These functions guess the right *get_raw_(\*)_coverage* in function of the data input and pass
it to a post processing function.

all functions returned have the same API

3 parameters as input

- **annot_entry**: an entry of the annotation file.
- **start**: The position to start to compute the coverage(coordinates are 0-based, start position is included).
- **stop**: The position to stop to compute the coverage (coordinates are 0-based, stop position is excluded).

and

- **return**: a tuple of two list or tuple containing in this order the coverages on the forward strand then the
  coverages on the reverse strand.

These architecture allow to combine easily the different get_raw_coverage function with the different post-processing.
For instance::

    bam = pysam.AlignmentFile(bam_file, "rb")
    get_coverage = get_padded_coverage(bam, max_left, max_right, qual_thr=15)
    forward, reverse = get_coverage(annot_entry, 10 200)

or ::

    wig = wig_parser.parse()
    get_coverage = get_resized_coverage(wig, 200)
    forward, reverse = get_coverage(annot_entry, 10 200)



.. automodule:: craw.coverage
    :members: padded_coverage_maker, resized_coverage_maker, sum_coverage_maker
    :private-members:
    :special-members:


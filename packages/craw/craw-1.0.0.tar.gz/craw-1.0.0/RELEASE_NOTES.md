Version 1.0
===========

Features
--------

* add option craw_coverage **\-\-justify** the coverage of all genes are scaled to have the same number 
  of values whatever their length, this option suppress the alignment on the reference and the "padding".
* add option craw_coverage **\-\-sum** instead of compute the coverage for each nucleotides inside the window
  do the sum of these coverages.

code refactoring to follow the python standards.
Containers are now available (Singularity & Docker)
  
Version 0.9
===========

Bug fix
-------

**craw_coverage** when gene is on reverse strand the coverage scores must be reversed
to always display coverages scores in the same sense than the gene.
([bug 27](https://gitlab.pasteur.fr/bneron/craw/issues/27))

Features
--------

**craw_coverage** allow to specify to wig files as input one for the forward strand one for the reverse
([feature 26](https://gitlab.pasteur.fr/bneron/craw/issues/26))

**craw_htmp** allow the user to specify marks a mark is a vertical line in a given color at a given positon
([feature 25](https://gitlab.pasteur.fr/bneron/craw/issues/25))
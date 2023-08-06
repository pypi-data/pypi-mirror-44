Python Classes for manipulating Bible references
------------------------------------------------
Python classes for Bible Verse and Passage - useful for storing, comparing,
and formatting Bible references. Also includes Django form classes to make it
easy to add Bible references to your Django models.

Note that this module does not let you actually pull and display the text
of a Bible verse or passage - it is just for working with and displaying
the reference to the verses. Other tools and APIs can be used to grab and
display the actual verse text for a reference.

Installation
------------

pip install bible-passage-reference-parser


## Using Classes

While this section is being expanded, please see the test program, test_bible.py 
for numerous examples of use. Here are some basics:

- create Verse objects:  `bible.Verse('James 2:10')`
- create Passage objects:  `bible.Passage('John 4:3', 'John 4:10')`
                           `bible.Passage('John 4:3-10')`
                           or supply 2 Verse objects
- test for a Verse to be included in a passage:
       `Passage.includes(Verse)`
- test for a Passage to have overlap with another Passage:
       `Passage1.overlap(Passage2)`
- and more

Fork and Thanks
---------------

I forked this to add a `parse_string` methods

\__str__ and \__repr__ added to both Verse and Passage classes, \__len__ added to
 Passage, other changes were minimal.

Thanks to Jason Ford and Tom Faulkner for writing this and making it available
to the world.

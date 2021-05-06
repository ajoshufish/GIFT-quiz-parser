# GIFT-quiz-parser
Parse an appropriately formatted .txt file into a GIFT format single-unit Moodle quiz import.

GIFT reference guide: https://docs.moodle.org/310/en/GIFT_format#Special_Characters_.7E_.3D_.23_.7B_.7D

Format notes:
* Set Unit number at start of file
* Input filename: quiz.txt
* Blank lines used to indicate question transitions -- no extra blank lines, including at start/end of file.
* Questions should start either #. or ##. (e.g., 4. or 12.)
* If question will contain HTML formatting, it should start [html]#. or [html]##. (spacing here is fine, it picks things up after the '.' mark anyway).
* Categories will be created as subcategories for the Unit in question, set at start of file.
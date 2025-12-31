** GROUP 10
* MEMBER NAME: OWUSU PRINCE ASANTE INDEX NUMBER: 1725628151
* MEMBER NAME: JEREMIAH ABBAN INDEX NUMBER: 1730228832
* MEMBER NAME: BENJAMIN YAMOAH INDEX NUMBER: 1724836980
* MEMBER NAME: MICHAEL KWEKU GABRIEL FREMPONG INDEX NUMBER: 1730138773
* MEMBER NAME: NANA AKWASI NYAMEKYE DONKOR INDEX NUMBER: 1725907707
* MEMBER NAME: PRINCESS XORSEH DONKOR INDEX NUMBER: 1723900176
//MEMBER NAME: BERNARD OBENG ABOAGYE INDEX NUMBER: 1725028853
//MEMBER NAME: RONY AYORKOR OKAI INDEX NUMBER: 1724242663
//MEMBER NAME: AMANING SALOMEY INDEX NUMBER: 1724850241
//MEMBER NAME: GWENDOLYN ESSEL INDEX NUMBER: 1725743271

ILOC Compiler Front-End – ICT411 Mid-Semester Project
Implementation Language: Python 3

Building and Running Instructions:

No compilation is required.

1. Make the launcher script executable (do this only once):
   chmod a+x 411fe

2. Run the program using one of the following commands:

   ./411fe -h                    # Display help message
   ./411fe -s <filename>         # Scanner mode only
   ./411fe -p <filename>         # Scan + parse + error reporting (default mode)
   ./411fe -r <filename>         # Scan + parse + print intermediate representation
   ./411fe <filename>            # Same as -p (default when no flag is given)

Supported Command-Line Options:

-h                  Show this help message
-s <file>           Scan the input file and print all tokens
-p <file>           Scan, parse, validate syntax, and report "VALID ILOC PROGRAM" or all errors with line numbers
-r <file>           Scan, parse, build IR, and print the intermediate representation in the required format
(no flag) <file>    Default behaviour is equivalent to -p

Flag priority (handled automatically): -h > -r > -p > -s
Invalid flag combinations will display an error message followed by the help text.

Additional Notes:
- The scanner is fully character-by-character (no regular expressions used).
- The parser continues after errors and reports all syntax issues found.
- Tested on Linux.


This program takes an input terminated by a specific character and repeats it back

>                                           Leave cell 0 empty for later
>>>++++++++++++++++++++++++++++++++         This writes the comparison character to cell 4; Modify this line with the appropriate number of pluses
[-<<+>+>>+<]                                Copy the comparison character to cells 2 3 and 5 removing it from cell 4
<<<,                                        Read the first character to cell 1
>                                           Move to the comparison character at cell 2
[-<->]                                      Subtract the comparison character from the read character
<                                           Move back to the modified read character at cell 1

[                                           While the modified read character is nonzero: read more characters
    >>                                          Move to the comparison character two cells after the last modified read character
    [-<<+>>]                                    Restore the modified read character to its original value
    >>                                          Move to the last remaining copy of the comparison character
    [-<<+>+>>+<]                                Copy the comparison character to the adjacent two spaces to the left and one space to the right and destroy the original
    <<<                                         Prepare to read a character
    ,                                           Read a character from the input
    >                                           Move to the first comparison character
    [-<->]                                      Subtract the comparison character from the read character
    <                                           Move back to the modified read character
]

>>                                          Move to the comparison character two cells after the last modified read character
[-<<+>>]                                    Restore the modified read character to its original value
<<                                          Move to the last read character
[<]>                                        Move to the start of the read characters
[.>]                                        Write the characters

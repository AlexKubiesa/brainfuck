This program takes an input terminated by any control character or space and repeats it back without that final character

>                                                   Leave cell 0 empty for later and move to cell 1
++++++++++++++++++++++++++++++++                    Write a space comparison character to cell 1
[->+>>>>+>>+<<<<<<<]                                Clone the comparison character from cell 1 to cells 2 (comparison cell) 6 (restore cell) and 8 (backup cell)

,                                                   Read a character into cell 1 (entry cell)
>>>>+<<<<[>]>[>]>[<<<-<-[>]>[>]>]>[<]>-<<<<         subtract_difference

[                                                   While the modified read value is nonzero:
    [->>>>>-<<<<<]>>>>>[-<<<<<+>>>>>]<<<<<              Restore the original value from the restore cell
    >>>>>>>[-<<<<<+>>>>+>>+<]<<<<<<<                    Clone the backup cell to relative cells 5L; 1L and 1R
    >                                                   Move to the next entry cell
    ,                                                   Read a character into the entry cell
    >>>>+<<<<[>]>[>]>[<<<-<-[>]>[>]>]>[<]>-<<<<         subtract_difference
]

<[<]>                                               Move back to the start of the string
[.>]                                                Write the string to the output


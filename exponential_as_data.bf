This script calculates an exponential A^B; B is written into cell 0 initially while A is encoded into the instructions


+++                         Set cell 0 to be 3 (B)
>+++++                      Set cell 1 to be 5 (A)
<                           Move back to cell 0

                            # Multiply cell 1 a number of times according to cell 0
>>+                         Set cell 2 to be 1 (the multiplicative identity)
<<                          Move back to cell 0
[                           While cell 0 is nonzero:
    -                           Subtract 1 from cell 0
    >                           Move to cell 1
    
                                # Multiply cells 1 and 2 and store the result in cell 2
    >                           Move to cell 2
    [                           While cell 2 is nonzero:
        -                           Subtract 1 from cell 2
        <                           Move to cell 1
        [->>+>+<<]                  Clone cell 1 into cells 3 and 4
        >>>[-<<<+>>>]               Transfer cell 4 into cell 1
        <<                          Move back to cell 2
    ]
    >[-<+>]<                    Transfer cell 3 to cell 2
    
    <<                          Move back to cell 0
]

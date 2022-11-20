This script calculates an exponential A^B; B is written into cell 0 initially while A is encoded into the instructions


+++                         Set cell 0 to be 3 (B)

                            # Multiply A a number of times according to cell 0
>+                          Set cell 1 to be 1 (the multiplicative identity)
<                           Move back to cell 0
[                           While cell 0 is nonzero:
    -                           Subtract 1 from cell 0
    >                           Move to cell 1
    
                                # Multiply cell 1 by 5 (A)
    [                           While cell 1 is nonzero:
        -                           Subtract 1 from cell 1
        >+++++                      Add 5 to cell 2
        <                           Move back to cell 1
    ]
    >[-<+>]<                    Transfer cell 2 to cell 1
]

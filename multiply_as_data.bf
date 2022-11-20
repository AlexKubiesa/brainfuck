This script multiplies two numbers initially written into cells 0 and 1; The result ends up in cell 2

Required memory layout:
    A B 0 0
    ^


+++++                       Set cell 0 to be 5 (first input)
>+++                        Set cell 1 to be 3 (second input)
<                           Move back to cell 0

[                           While cell 0 is nonzero:
    -                           Subtract 1 from cell 0
    >                           Move to cell 1
    [->+>+<<]                   Clone cell 1 into cells 2 and 3
    >>[-<<+>>]<<                Transfer cell 3 to cell 1
    <                           Move back to cell 0
]

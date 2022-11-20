>+++++                      Set cell 1 to be 5
>+++                        Set cell 2 to be 3
<                           Move back to cell 1

>>>>+<<<<                   Write an indicator 1 to cell 5 and go back to cell 1
[>]>[>]>                    This moves us to cell 3 or 4 if one of A or B is zero; otherwise it moves us to cell 5

[                           Perform the subtraction:
    <<<-<-                      Move back to cell 1 while subtracting 1 from cells 2 and 1
    [>]>[>]>                    Check whether both numbers are zero
]                               At the end of this loop we are at cell 3 if A and B were equal; or cell 4 if they were not

>[<]>                       Move to cell 5
-                           Set cell 5 to 0
<<<<                        Move back to cell 1

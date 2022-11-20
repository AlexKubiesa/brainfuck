This program takes as input a LF terminated string and returns the same as output

>               Leave a space at the start for later
,----------     Read the first character and compare to LF
[>,----------]  Read the input while checking if the characters are line feeds
<[<]>           Move to the start of the stored text
[++++++++++.>]  Write the original characters
++++++++++.     Write the final LF

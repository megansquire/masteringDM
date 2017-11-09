There was an error on page 11 of Chapter 8:
```
F1 = 2*((MUC_Precision * MUC_Recall) / (MUC_Precision + MUC_Recall))
   = 2*(.5 * .5) / (.5 + .5))
   = 50%
```
is missing a parenthesis on line 2, and should read:
```
F1 = 2*((MUC_Precision * MUC_Recall) / (MUC_Precision + MUC_Recall))
   = 2*((.5 * .5) / (.5 + .5))
   = 50%
```

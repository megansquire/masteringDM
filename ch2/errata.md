# Some errors I noticed in the book
## Page 7 - showing a rule 
bananas -> vanilla wafers, whipped cream
[support = .001%, confidence=10%]

For clarity's sake, this support value should have had the same value as the one above it (1%) rather than this new value of .001%.

## Page 9 - calculating Added Value
In the calculation of confidence, I accidentally took the right-hand side instead of the left-hand side. I wrote "The confidence of vanilla wafers -> bananas in this scenario is .3/.8 = 37.5%" but it should have been "The confidence of vanilla wafers -> bananas in this scenario is .3/.5 = 60%". 

This changes the AV calculations at the bottom of the page:

confidence of rule = .6
support of right-hand side (bananas) = .8
added value = .6 - .8 = -0.2

The rule is still true, that bananas do better on their own. 

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

## Page 40-41 - calculating confidence
The Python code needs a change in the order the parameters are passed into the SQL query:
```python
    queryConf = "SELECT num_projs \
              FROM msquire.fc_project_tag_pairs \
              WHERE (tag1 = %s AND tag2 = %s) \
              OR    (tag2 = %s AND tag1 = %s)"
    cursor.execute(queryConf, (tagA, tagB, tagA, tagB))
    pairSupport = cursor.fetchone()[0]
    confidence = round((ruleSupport / pairSupport),2)
```

Squad DF
=====

Nice and clean QA dataset from squad.


```bash
pip install squad_df
```

```python
from squad_df import v1, v2

import pandas as pd
df = pd.DataFrame(list(v2))
df.info()
# context         142192 non-null object                                                                       
# is_train        142192 non-null bool                                                                         
# mark_0_start    92749 non-null float64                                                                       
# mark_0_text     92749 non-null object                                                                        
# mark_1_start    5927 non-null float64                                                                        
# mark_1_text     5927 non-null object                                                                         
# mark_2_start    5839 non-null float64                                                                        
# mark_2_text     5839 non-null object                                                                         
# mark_3_start    1601 non-null float64                                                                        
# mark_3_text     1601 non-null object                                                                         
# mark_4_start    976 non-null float64                                                                         
# mark_4_text     976 non-null object                                                                          
# mark_5_start    31 non-null float64                                                                          
# mark_5_text     31 non-null object                                                                           
# para_id         142192 non-null int64                                                                        
# possible        142192 non-null bool                                                                         
# question        142192 non-null object                                                                       
# question_id     142192 non-null object                                                                       
# wiki_id         142192 non-null int64 
```

Column          |   Meaning
----------------|-------------------
`context`       | the paragraph from which the question needs to be answered
`is_train`      | is this example part of the training set?
`mark_i_start`  | starting character index of the marking
`mark_i_text`   | text of the marking
`para_id`       | id of a para in a 'paragraphs'
`question_id`   | id of the question to be used for submissions
`wiki_id`       | id of an item in 'data' in the original json
`question`      | the question text.
`possible`      | whether answering the question is possible.


The markings are sorted in order of length. Duplicates are not removed.

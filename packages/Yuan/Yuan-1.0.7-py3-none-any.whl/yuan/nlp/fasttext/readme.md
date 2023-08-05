# [FastText][1]

---
- Train
```bash
./fastText-0.2.0/fasttext cbow
-input ./all_data_cut.tsv \
-output ./fast_text.model \
- ws 5 \
-dim 200 \
-minCount 64 \
-minn 1 \
-maxn 6 \
-epoch 16 \
-thread 64

./fastText-0.2.0/fasttext skipgram
-input ./all_data_cut.tsv \
-output ./fast_text.model \
- ws 5 \
-dim 200 \
-minCount 64 \
-minn 1 \
-maxn 6 \
-epoch 16 \
-thread 64
```
- Load: 加载C++版的FastText模型
```python
from gensim.models import FastText
model = FastText.load_fasttext_format('./fasttext.model')
```

---
[1]: https://github.com/facebookresearch/fastText#building-fasttext-using-make-preferred
https://radimrehurek.com/gensim/models/fasttext.html#module-gensim.models.fasttext

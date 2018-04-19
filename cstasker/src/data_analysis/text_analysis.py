import sqlite3
import lda
import lda.datasets
import numpy as np
import jieba
import re


def is_float(val):
    return not not re.match('^(\d+\.\d*)|(\d+)|([a-zA-Z0-9]+)$', val)


def is_chinese(val):
    return re.match('^[^\x00-\xff]+$', val)


if __name__ == '__main__':
    conn = sqlite3.connect('/Users/wangfeng/Downloads/blued/data0302.db')
    print('database connected')

    with open('../data/word_dict.txt') as f_in:
        for i in f_in.readlines():
            # print(i.strip())
            jieba.suggest_freq(i.strip(), True)

    stop_words = set()
    stop_words.add('\n')
    stop_words.add(' ')
    with open('../data/chinese_stop_words.txt') as f_in:
        for i in f_in.readlines():
            stop_words.add(i.strip())

    sql = """
        SELECT "description" FROM "user20180202" WHERE description != ''
    """
    c = conn.cursor()
    data = [_ for _ in c.execute(sql)]
    print(len(data))
    sql = """
        select "description" from "user20180202" join where
    """
    conn.close()

    sentences = []
    train_mat = []
    words_set = set()
    count = 0
    for s in data[:30000]:
        words = [_ for _ in jieba.cut(s[0])]
        # print(words)
        # words = filter(lambda _: _ not in stop_words and not is_float(_), words)
        words = [x for x in filter(lambda _: _ not in stop_words and is_chinese(_), words)]
        if len(words) > 0:
            sentences.append(words)
            for w in words:
                count += 1
                # print(w, is_float(w))
                words_set.add(w)
    print(len(words_set))
    print(count)
    all_words = list(words_set)
    word2index = {i[1]: i[0] for i in enumerate(words_set)}
    # print(word2index)
    doc_count_each_word = [0 for _ in range(len(words_set))]

    with open('../data/tmp_out.txt', 'w+') as f_out:
        for i in words_set:
            f_out.write(i + '\n')

    count = 0
    for s in sentences:
        a = [0 for _ in range(len(words_set))]
        has_word = [0 for _ in range(len(words_set))]
        for w in s:
            # print(w)
            # a[word2index[w]] += 1.0 / len(s)
            a[word2index[w]] += 1
            has_word[word2index[w]] = 1
        train_mat.append(a)
        for i, j in enumerate(has_word):
            doc_count_each_word[i] += j
        print(count)
        count += 1

    train_mat = np.array(train_mat)
    print(train_mat.shape)

    # calculate tf-idf for each description
    # for i in range(train_mat.shape[0]):
    #     for j in range(train_mat.shape[1]):
    #         train_mat[i][j] = train_mat[i][j] * np.log(len(sentences) * 1.0 / (1 + doc_count_each_word[j]))

    model = lda.LDA(n_topics=2, n_iter=1500, random_state=1)
    model.fit(train_mat)
    topic_word = model.topic_word_
    n_top_words = 80
    for i, topic_dist in enumerate(topic_word):
        # index = np.argsort(topic_dist)[:-(n_top_words + 1): -1]
        # for j in index:
        #     print(all_words[j], )
        topic_words = np.array(all_words)[np.argsort(topic_dist)][:-(n_top_words + 1): -1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))

    res = model.transform(train_mat)
    print(res[10])

    # X = lda.datasets.load_reuters()
    # print(X.shape)
    # vocab = lda.datasets.load_reuters_vocab()
    # titles = lda.datasets.load_reuters_titles()
    # model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
    # model.fit(X)
    # topic_word = model.topic_word_  # model.components_ also works
    # n_top_words = 8
    # for i, topic_dist in enumerate(topic_word):
    #     topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n_top_words + 1):-1]
    #     print('Topic {}: {}'.format(i, ' '.join(topic_words)))

    # conn.close()

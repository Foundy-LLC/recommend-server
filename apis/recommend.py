import numpy as np
import re
from gensim.models import fasttext
from sklearn.metrics.pairwise import cosine_similarity
from konlpy.tag import Okt

from crud.count_users import is_user_valid
from crud.response_body import get_recommend_response_body
from crud.room_recommend import *
from crud.user_recommend import *


def cosine_sim(vector1, vector2):
    vector1 = np.array(vector1).reshape(1, -1)
    vector2 = np.array(vector2).reshape(1, -1)

    similarity = cosine_similarity(vector1, vector2)[0, 0]

    return similarity


def get_recommended_friends(db, user_id: str):
    if not is_user_valid(db, user_id):
        return get_recommend_response_body([])

    TOP_N = 10

    recommend = list()

    user_vector = get_my_tag_vector(db, user_id)
    rows = get_users_tag_vector(db, user_id)

    for row in rows:
        if len(recommend) == TOP_N:
            break

        u_id, name, profileImage, introduce, status, tag_vec = row

        if not is_friend(db, user_id, u_id):
            similarity = cosine_sim(user_vector, tag_vec)
            recommend.append((u_id, name, profileImage, introduce, status, similarity))

    recommend = sorted(recommend, key=lambda x: x[-1], reverse=True)

    return get_recommend_response_body(recommend)


def update_users_vector(db, model: fasttext, user_id=None):
    users_tag = get_users_all_tag(db, user_id)

    for user, tags in users_tag.items():
        tags_len = len(tags)
        vector_avg = np.zeros(300, dtype=np.float32)

        for tag in tags:
            tag_vector = model.wv[tag]
            vector_avg = np.sum([vector_avg, tag_vector], axis=0)

        vector_avg /= tags_len

        insert_user_vector(db, user, vector_avg.tolist())

    print("Users Vector Update Complete")


def update_rooms_vector(db, model: fasttext):
    rooms_info = get_rooms_info(db)

    for room, info in rooms_info.items():
        tags_len = len(info) - 1  # except title

        vector_avg = np.zeros(300, dtype=np.float32)

        for tag in info[1:]:
            tag_vector = model.wv[tag]
            vector_avg = np.sum([vector_avg, tag_vector], axis=0)

        vector_avg /= max(1, tags_len)

        title = preprocess_title(info[0])
        print(title)

        title_len = len(title)

        for word in title:
            word_vector = model.wv[word]
            vector_avg = np.sum([vector_avg, word_vector], axis=0)

        vector_avg /= max(1, title_len)

        insert_room_vector(db, room, vector_avg.tolist())

    print("Rooms Vector update Complete")

def preprocess_title(title:str):
    okt = Okt()
    title = okt.normalize(title)

    original = title

    pattern = r'\([^)]*\)'  # ()
    title = re.sub(pattern=pattern, repl='', string=title)

    pattern = r'\[[^)]*\]'  # []
    title = re.sub(pattern=pattern, repl='', string=title)

    pattern = r'\<[^)]*\>'  # <>
    title = re.sub(pattern=pattern, repl='', string=title)

    pattern = r'\{[^)]*\}'  # {}
    title = re.sub(pattern=pattern, repl='', string=title)

    title = title.replace("...", " ")

    pattern = r'[^a-zA-Z가-힣]'
    title = re.sub(pattern=pattern, repl=' ', string=title)

    title = list(filter(lambda x:len(x)>1, title.split()))


    if not title:
        return original.split()

    return title

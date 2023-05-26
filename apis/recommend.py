from gensim.models import fasttext
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from crud.user_recommend import *

def cosine_sim(vector1, vector2):
    vector1 = np.array(vector1).reshape(1,-1)
    vector2 = np.array(vector2).reshape(1,-1)

    similarity = cosine_similarity(vector1, vector2)[0, 0]

    return similarity


def get_recommended_friends(db, user_id: str, model:fasttext):
    recommend = list()

    user_vector = get_my_tag_vector(db, user_id)
    rows = get_users_tag_vector(db, user_id)

    for row in rows:
        u_id, tag_vec = row

        if not is_friend(db, user_id, u_id):
            similarity = cosine_sim(user_vector, tag_vec)
            recommend.append({"user" : u_id, "similarity":similarity})

    recommend = sorted(recommend, key=lambda x:x["similarity"], reverse=True)
    print(recommend)

    

def update_users_vector(db, model:fasttext):
    users_tag = get_users_all_tag(db)

    for user, tags in users_tag.items():
        tags_len = len(tags)
        vector_avg = np.zeros(300, dtype=np.float32)

        for tag in tags:
            tag_vector = model.wv[tag]
            vector_avg = np.sum([vector_avg, tag_vector], axis=0)

        vector_avg /= tags_len

        insert_user_vector(db, user, vector_avg.tolist())

    print("Users Vector Update Complete")


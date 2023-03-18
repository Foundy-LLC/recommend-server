from crud import crud_ranking


def ranking_index(db):
    something = crud_ranking.get_items(db)
    return something

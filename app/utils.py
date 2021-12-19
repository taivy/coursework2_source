import json
import logging
from pathlib import Path
from collections import Counter


DATA__PATH = "app/data"
DATA_PATH_OBJ = Path(DATA__PATH)


def read_json(file_path):
    try:
        with open(file_path.resolve(), "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        logging.error("Error reading file %s: %s", file_path, e)
        return None


def load_comments():
    data_file_path = DATA_PATH_OBJ / "comments.json"
    return read_json(data_file_path)


def get_comments_counter():
    comments = load_comments()
    counter = Counter()
    for comment in comments:
        counter[comment["post_id"]] += 1
    return counter


def get_post_comments(post_id):
    comments = load_comments()
    return list(filter(lambda comment: comment["post_id"] == post_id, comments))


def get_post_comments_count_text(comments_cnt):
    if comments_cnt == 0:
        return "Нет комментариев"
    elif comments_cnt == 1:
        return "1 комментарий"
    else:
        return f"{comments_cnt} комментариев"


def get_post_desc_short(post_content):
    desc_short = post_content[:50]
    if len(post_content) > 50:
        desc_short += "..."
    return desc_short


def enrich_post_data(post, add_desc_short=False):
    post["comments"] = get_post_comments(post["pk"])
    post["comments_count_text"] = get_post_comments_count_text(len(post["comments"]))
    if add_desc_short:
        post["desc_short"] = get_post_desc_short(post["content"])


def get_post_by_id(post_id):
    posts = load_posts()
    posts_filtered = list(filter(lambda post_: post_["pk"] == post_id, posts))
    if len(posts_filtered) == 0:
        return None
    post = posts_filtered[0]
    enrich_post_data(post)
    return post


def get_post_by_user(user_name):
    posts = load_posts()
    posts_filtered = list(filter(lambda post_: post_["poster_name"] == user_name, posts))
    for post in posts_filtered:
        enrich_post_data(post, add_desc_short=True)
    return posts_filtered


def search_posts(search_str):
    posts = load_posts()
    posts_filtered = list(filter(lambda post_: search_str.lower() in post_["content"].lower(), posts))[:10]
    for post in posts_filtered:
        enrich_post_data(post, add_desc_short=True)
    return posts_filtered


def load_posts():
    data_file_path = DATA_PATH_OBJ / "data.json"
    return read_json(data_file_path)


def get_posts():
    posts = load_posts()
    comments_counter = get_comments_counter()

    for post in posts:
        post["desc_short"] = get_post_desc_short(post["content"])
        comments_cnt = comments_counter[post["pk"]]
        post["comments_count_text"] = get_post_comments_count_text(comments_cnt)

    return posts

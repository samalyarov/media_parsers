# Importing libraries:
import pandas as pd
import re
from stop_words import get_stop_words
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords

# Designed to be used in JupLab
from tqdm import tqdm_notebook
tqdm_notebook().pandas()


def fix_vk_data(data,
                likes=True,
                comments=True,
                views=True,
                reposts=True,
                classification=True,
                fix_channel_names=True,
                groups_excel='vk_groups.xlsx',
                new_df=True):
    """
    Function for preparing data downloaded from VK via the parser for future analysis

    :param data: Dataframe with data to edit
    :param likes: Should the "likes" column be fixed
    :param comments: Should the "comments" column be fixed
    :param views: Should the "views" column be fixed
    :param reposts: Should the "reposts" column be fixed
    :param fix_channel_names: Whether the "channel_id" should be changed to their names
    :param groups_excel: Excel with groups and their IDs
    :param new_df: Should a new DataFrame be made with only the required columns?
    :return:
    """

    if likes:
        data_likes = data['likes'].str.split(',', expand=True).reset_index(drop=True)
        data_likes = data_likes[1]
        data_likes = data_likes.str.replace("'count': ", "")
        data['likes'] = data_likes.values.astype(float)

    if comments:
        data_comments = data['comments'].str.split(',', expand=True).reset_index(drop=True)
        data_comments = data_comments[1]
        data_comments = data_comments.str.replace("'count': ", "")
        data_comments = data_comments.str.replace(" ", "")
        data_comments = data_comments.str.replace("}", "")
        data['comments'] = data_comments.values.astype(float)

    if views:
        data_views = data['views'].str.split(',', expand=True).reset_index(drop=True)
        data_views = data_views[0]
        data_views = data_views.str.replace("'count': ", "")
        data_views = data_views.str.replace("{", "")
        data_views = data_views.str.replace("}", "")
        data['views'] = data_views.values.astype(float)

    if reposts:
        data_reposts = data['reposts'].str.split(',', expand=True).reset_index(drop=True)
        data_reposts = data_reposts[0]
        data_reposts = data_reposts.str.replace("'count': ", "")
        data_reposts = data_reposts.str.replace("{", "")
        data['reposts'] = data_reposts.values.astype(float)

    if classification:
        groups_excel = 'vk_groups.xlsx'
        groups_info = pd.read_excel(groups_excel)

        groups_info.drop(columns=['#', 'Group name', 'Full link', 'Channel Members'], inplace=True)
        groups_info.rename(columns={'Channel ID': 'owner_id'}, inplace=True)
        data = pd.merge(data, groups_info, on='owner_id', how='left')

    if fix_channel_names:
        groups_excel = pd.read_excel(groups_excel)
        groups_ids = groups_excel['Channel ID'].tolist()
        groups_names = groups_excel['Group name'].tolist()

        channel_ids = {}

        for i in range(len(groups_ids)):
            channel_ids[-groups_ids[i]] = groups_names[i]

        for channel_id, channel_name in channel_ids.items():
            data['owner_id'].mask(data['owner_id'] == channel_id, channel_name, inplace=True)

    if new_df:
        data = data[['owner_id', 'date', 'text', 'comments', 'likes', 'views', 'reposts']]
        data.reset_index(drop=True)

    return data


def lemmatize(doc):
    """
    Function for lemmatizing strings

    :param doc: A string setting to lemmatize
    :return:
    """
    patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
    morph = MorphAnalyzer()
    stopwords_ru = stopwords.words("russian")

    doc = re.sub(patterns, ' ', doc)
    tokens = []
    for token in doc.split():
        if token and token not in stopwords_ru:
            token = token.strip()
            token = morph.normal_forms(token)[0]
            tokens.append(token)
            ' '.join(tokens)
    if len(tokens) > 2:
        return tokens
    return None


def prepare_text(data,
                 cleaned_text_column='cleaned_text'
                 ):
    """
    Function for preparing the text for analysis

    :param data: DataFrame with which to work
    :param cleaned_text_column: Which column should the new text be added to
    :return:
    """
    # Переводим текст в нижний регистр и заменяем "ё" на "е"
    data['text'] = data['text'].str.lower().replace("ё", "е")

    # Берём текст постов и лемматизируем его
    only_text_data = data['text'].astype(str)
    text_preps = only_text_data.progress_apply(lemmatize)

    # Добавляем полученный результат к новому ДФ:
    text_preps = text_preps.to_frame().reset_index(drop=True).fillna(value="-")

    # Соединяем список из слов в предложения
    for i in tqdm_notebook(range(len(text_preps))):
        stringy = ' '.join(text_preps.loc[i, 'text'])
        text_preps.loc[i, 'text'] = stringy

    # Добавляем столбец с дополнительными данными
    data[cleaned_text_column] = text_preps['text'].values

    return data

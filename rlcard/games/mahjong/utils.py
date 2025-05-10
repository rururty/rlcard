import numpy as np
from rlcard.games.mahjong.card import MahjongCard as Card


card_encoding_dict = {}
num = 0
for _type in ['bamboo', 'characters', 'dots']:
    for _trait in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
        card = _type+"-"+_trait
        card_encoding_dict[card] = num
        num += 1
for _trait in ['green', 'red', 'white']:
    card = 'dragons-'+_trait
    card_encoding_dict[card] = num
    num += 1

for _trait in ['east', 'west', 'north', 'south']:
    card = 'winds-'+_trait
    card_encoding_dict[card] = num
    num += 1
card_encoding_dict['pong'] = num # 碰
card_encoding_dict['chow'] = num + 1 # 吃
card_encoding_dict['gong'] = num + 2 # 杠
card_encoding_dict['stand'] = num + 3 # 上听

card_decoding_dict = {card_encoding_dict[key]: key for key in card_encoding_dict.keys()}

# 获得一个牌堆，牌堆中有34种牌（card对象），每种牌有4张
def init_deck():
    deck = []
    info = Card.info
    for _type in info['type']:
        index_num = 0
        if _type != 'dragons' and _type != 'winds':
            for _trait in info['trait'][:9]:
                card = Card(_type, _trait)
                card.set_index_num(index_num)
                index_num = index_num + 1
                deck.append(card)
        elif _type == 'dragons':
            for _trait in info['trait'][9:12]:
                card = Card(_type, _trait)
                card.set_index_num(index_num)
                index_num = index_num + 1
                deck.append(card)
        else:
            for _trait in info['trait'][12:]:
                card = Card(_type, _trait)
                card.set_index_num(index_num)
                index_num = index_num + 1
                deck.append(card)
    deck = deck * 4
    return deck

# 将牌堆平铺为列表
# 如[[bamboo-1, bamboo-2], [bamboo-3, bamboo-4]] -> [bamboo-1, bamboo-2, bamboo-3, bamboo-4]
def pile2list(pile):
    cards_list = []
    for each in pile:
        cards_list.extend(each)
    return cards_list

# 将[牌]转化为[牌的字符串]，如['bamboo-1', 'bamboo-2', ...]
def cards2list(cards):
    cards_list = []
    for each in cards:
        cards_list.append(each.get_str())
    return cards_list


# [牌] -> 牌矩阵(34,4)有这个牌对应的位置为1 
# 如[[bamboo-1, bamboo-2], [bamboo-3, bamboo-4]] -> [[1, 0, 0, 0], [1, 0, 0, 0], ...]
def encode_cards(cards):
    plane = np.zeros((34,4), dtype=int)
    cards = cards2list(cards)
    for card in list(set(cards)):
        index = card_encoding_dict[card]
        num = cards.count(card)
        plane[index][:num] = 1
    return plane

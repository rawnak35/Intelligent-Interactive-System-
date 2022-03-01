import numpy as np
from random import shuffle

def gamma(q_k, q_l, rank_list):
    try:
        index_k = rank_list.index(q_k)
        index_l = rank_list.index(q_l)
        if index_k > index_l:
            return 1
        elif index_l > index_k:
            return -1
        else:
            return 0
    except:
        return 0


def Z_k(L, rank_list, k):
    q_k = L[k]
    Z_k_list = []
    for q_l in L:
        if q_l not in rank_list:
            continue
        index_l = rank_list.index(q_l)
        if index_l < k:
            Z_k_list.append(tuple([q_l, q_k]))

    return Z_k_list


def A_k(L, true_rank_list, pred_rank_list, k):
    Z_k_ = Z_k(L, pred_rank_list, k)
    if k == 0:
        return 0
    sum_I = 0
    for q_j, q_k in Z_k_:
        if q_k not in pred_rank_list:
            continue
        index_k_t = true_rank_list.index(q_k)
        index_k_p = pred_rank_list.index(q_k)
        index_j_t = true_rank_list.index(q_j)
        index_j_p = pred_rank_list.index(q_j)
        if ((index_k_t > index_j_t) and (index_k_p > index_j_p)) or ((index_k_t < index_j_t) and (index_k_p < index_j_p)):
            sum_I += 1

    return sum_I / k


def calc_AP(L, true_rank_list, pred_rank_list):
    s_AP = 0
    for k in range(len(L)):
        A_k_ = A_k(L, true_rank_list, pred_rank_list, k)
        s_AP += A_k_

    return s_AP / (len(L)-1)


def rv(q_k, q_l, Students_Questions_dict, i):
    students = list(Students_Questions_dict.keys())
    students.remove(i)
    rank_i = Students_Questions_dict[i]
    rv_sum = 0
    for j in students:
        rank_j = Students_Questions_dict[j]
        gamma_ = gamma(q_k, q_l, rank_j)
        if gamma_ == 0:
            continue
        AP = calc_AP(rank_i, rank_i, rank_j)
        rv_sum += gamma_ * AP
    
    return np.sign(rv_sum)

def copeland_score(q, Students_Questions_dict, i):
    L_i = Students_Questions_dict[i]
    #L_i.remove(q)
    sum_c = 0
    for q_l in L_i:
        if q_l != q:
            rv_ = rv(q, q_l, Students_Questions_dict, i)
            sum_c += rv_
    return sum_c


def EduRank(Students_Questions_dict_train, Students_Questions_dict_test, i):
    L_i = Students_Questions_dict_test[i]
    shuffle(L_i) #TODO
    q_c_dict = {}
    for q in L_i:
        c_q = copeland_score(q, Students_Questions_dict_train, i)
        q_c_dict[q] = c_q


    q_c_dict_sorted = {k: v for k, v in sorted(q_c_dict.items(), key=lambda item: item[1])}
    return list(q_c_dict_sorted.keys())


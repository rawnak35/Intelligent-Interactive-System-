import EduRank2
import pickle
import evalution
import random_model


def run_EduRank(file_out):

    dict_out_put = {}
    sample = list(Students_Questions_dict_test.keys())
    j = 0
    s = len(sample)
    for i in Students_Questions_dict_test.keys():
        if i in sample:
            if j % 100 == 0:
                print(f" {j} out of {s}")
            dict_out_put[i] = EduRank2.EduRank(dict_neighbors[i], Students_Questions_dict_test, i)
            j += 1
    with open(file_out, 'wb') as f:
        pickle.dump(dict_out_put, f)
    return dict_out_put


def run_Random(file_out):
    dict_out_put = {}
    sample = list(Students_Questions_dict_train.keys())
    j = 0
    s = len(sample)
    for i in Students_Questions_dict_test.keys():
        if i in sample:
            dict_out_put[i] =random_model.predict_rank(Students_Questions_dict_test[i])
            j += 1
    with open(file_out, 'wb') as f:
        pickle.dump(dict_out_put, f)
    return dict_out_put


def calc_NDCG(diff_true_list, diff_pred_list):
    NDCG_sum = 0
    N = len(diff_pred_list)
    for i in range(N):
        n = len(diff_true_list[i])
        NDCG_sum += evalution.calc_NDCG(diff_true_list[i], diff_pred_list[i], p=n)
    return NDCG_sum/N


def AP_score(dict_out_put, true_dict):
    AP_sum = 0
    N = len(dict_out_put)
    for s in dict_out_put.keys():
        AP_sum += evalution.AP(true_dict[s], dict_out_put[s])
    return AP_sum/N

def NDPM_score(dict_out_put, true_dict):
    NDPM_sum = 0
    N = len(dict_out_put)
    for s in dict_out_put.keys():
        NDPM_sum += evalution.calc_NDPM(true_dict[s], dict_out_put[s])
    return NDPM_sum / N


def evaluate(dict_out_put, true_dict):
    diff_true_list = []
    diff_pred_list = []
    for s, q in dict_out_put.items():
        n = len(q)
        diff_true = list(range(n, 0, -1))
        diff_true_list.append(diff_true)
        diff_pred = []
        pred_list = q
        true_i = true_dict[s]
        for i in pred_list:
            diff_pred.append(n-true_i.index(i))
        diff_pred_list.append(diff_pred)

    #NDCG = round(calc_NDCG(diff_true_list, diff_pred_list), 3)
    NDCG = calc_NDCG(diff_true_list, diff_pred_list)
    print(f"NDCG score: {NDCG}")
    AP = AP_score(dict_out_put, true_dict)
    print(f"AP score: {AP}")
    NDPM = NDPM_score(dict_out_put, true_dict)
    print(f"NDPM score: {NDPM}")



with open('dict_ranked_s_q_master_sample_base.pkl', 'rb') as f:
    Students_Questions_dict_test = pickle.load(f)
with open('dict_ranked_s_q_train_sample_base.pkl', 'rb') as f:
    Students_Questions_dict_train = pickle.load(f)
with open('dict_neighbors_base.pkl', 'rb') as f:
    dict_neighbors = pickle.load(f)

"""
file_out = 'out_put_base.pkl'
out_put = run_EduRank(file_out)
print("------------------ base ------------------")
evaluate(out_put, Students_Questions_dict_test)
file_out = 'out_put_base_random.pkl'
print("random: ")
out_put = run_Random(file_out)
evaluate(out_put, Students_Questions_dict_test)



with open('dict_ranked_s_q_master_sample_op1.pkl', 'rb') as f:
    Students_Questions_dict_test = pickle.load(f)
with open('dict_ranked_s_q_train_sample_op1.pkl', 'rb') as f:
    Students_Questions_dict_train = pickle.load(f)
with open('dict_neighbors_op1.pkl', 'rb') as f:
    dict_neighbors = pickle.load(f)

file_out = 'out_put_op1.pkl'
out_put = run_EduRank(file_out)
print("------------------ op1 ------------------")

evaluate(out_put, Students_Questions_dict_test)
file_out = 'out_put_random_op1.pkl'
print("random: ")
out_put = run_Random(file_out)
evaluate(out_put, Students_Questions_dict_test)


with open('dict_ranked_s_q_master_sample_op2.pkl', 'rb') as f:
    Students_Questions_dict_test = pickle.load(f)
with open('dict_ranked_s_q_train_sample_op2.pkl', 'rb') as f:
    Students_Questions_dict_train = pickle.load(f)
with open('dict_neighbors_op2.pkl', 'rb') as f:
    dict_neighbors = pickle.load(f)
file_out = 'out_put_op2.pkl'
out_put = run_EduRank(file_out)
print("------------------ op2 ------------------")
evaluate(out_put, Students_Questions_dict_test)
file_out = 'out_put_random_op2.pkl'
print("random: ")
out_put = run_Random(file_out)

evaluate(out_put, Students_Questions_dict_test)

"""

with open('dict_ranked_s_q_master_sample_op3.pkl', 'rb') as f:
    Students_Questions_dict_test = pickle.load(f)
with open('dict_ranked_s_q_train_sample_op3.pkl', 'rb') as f:
    Students_Questions_dict_train = pickle.load(f)
with open('dict_neighbors_op3.pkl', 'rb') as f:
    dict_neighbors = pickle.load(f)
file_out = 'out_put_op3.pkl'
out_put = run_EduRank(file_out)
print("------------------ op3 ------------------")
evaluate(out_put, Students_Questions_dict_test)
file_out = 'out_put_random_op3.pkl'
print("random: ")
out_put = run_Random(file_out)
evaluate(out_put, Students_Questions_dict_test)

"""
with open('dict_ranked_s_q_master_sample_op4.pkl', 'rb') as f:
    Students_Questions_dict_test = pickle.load(f)
with open('dict_ranked_s_q_train_sample_op4.pkl', 'rb') as f:
    Students_Questions_dict_train = pickle.load(f)
with open('dict_neighbors_op4.pkl', 'rb') as f:
    dict_neighbors = pickle.load(f)
file_out = 'out_put_op4.pkl'
out_put = run_EduRank(file_out)
print("------------------ op4 ------------------")
evaluate(out_put, Students_Questions_dict_test)
file_out = 'out_put_random_op4.pkl'
out_put = run_Random(file_out)
print("random: ")
evaluate(out_put, Students_Questions_dict_test)
"""

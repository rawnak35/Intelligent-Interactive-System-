import pandas as pd
import pickle
global dict_student_ques_base
dict_student_ques_base = {}
global dict_student_ques_op1
dict_student_ques_op1 = {}
global dict_student_ques_op2
dict_student_ques_op2 = {}
global dict_student_ques_op3
dict_student_ques_op3 = {}
global dict_student_ques_op4
dict_student_ques_op4 = {}


def question_id(row):
    return row['Problem Name'] + ' ' + row['Step Name']


def creat_dict_student_ques_base(row):
    s = row['Anon Student Id']
    q_id = row['q_id']
    values = (row['Correct First Attempt'], -1 * row['Step Duration (sec)'])
    if s in dict_student_ques_base.keys():
        dict_student_ques_base[s][q_id] = values
    else:
        dict_student_ques_base[s] = {q_id: values}
    return


def creat_dict_student_ques_op1(row):
    s = row['Anon Student Id']
    q_id = row['q_id']
    values = (-1 * row['Incorrects'], -1 * row['Step Duration (sec)'])
    if s in dict_student_ques_op1.keys():
        dict_student_ques_op1[s][q_id] = values
    else:
        dict_student_ques_op1[s] = {q_id: values}
    return

def creat_dict_student_ques_op2(row):
    s = row['Anon Student Id']
    q_id = row['q_id']
    values = (-1 * row['Hints'], -1 * row['Step Duration (sec)'])
    if s in dict_student_ques_op2.keys():
        dict_student_ques_op2[s][q_id] = values
    else:
        dict_student_ques_op2[s] = {q_id: values}
    return

def creat_dict_student_ques_op3(row):

    s = row['Anon Student Id']
    q_id = row['q_id']
    values = (row['Opportunity'], -1 * row['Step Duration (sec)'])
    if s in dict_student_ques_op3.keys():
        dict_student_ques_op3[s][q_id] = values
    else:
        dict_student_ques_op3[s] = {q_id: values}
    return


def creat_dict_student_ques_op4(row):
    s = row['Anon Student Id']
    q_id = row['q_id']
    values = (-1 * row['Hints'], -1 * row['Incorrects'], row['Opportunity'])
    if s in dict_student_ques_op4.keys():
        dict_student_ques_op4[s][q_id] = values
    else:
        dict_student_ques_op4[s] = {q_id: values}
    return


def data_features_base(data, file_out):
    dict_student_ques_base = {}
    data = data[[ 'Anon Student Id', 'q_id', 'Step Duration (sec)', 'Correct First Attempt']]
    df1 = data.groupby(['Anon Student Id','q_id']).agg({'Correct First Attempt':'max', 'Step Duration (sec)':'mean'})
    df1 = df1.reset_index(level=['Anon Student Id','q_id'])
    df1.apply(creat_dict_student_ques_base, axis=1)
    dict_ranked_s_q = {}
    for s_id, s_dict in dict_student_ques_base.items():
        sorted_s_dict = sorted(s_dict.items(), key=lambda x: x[1])[:80]
        if len(sorted_s_dict) < 3:
            continue
        ranked_questions = dict(sorted_s_dict).keys()
        dict_ranked_s_q[s_id] = list(set(ranked_questions))
        if len(list(set(ranked_questions))) < 3:
            print('0-0-0')
    print(len(dict_ranked_s_q))
    # save ranked_dict
    with open(file_out, 'wb') as f:
        pickle.dump(dict_ranked_s_q, f)
    return dict_ranked_s_q


def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    if a_set & b_set:
        return True
    else:
        return False

def create_neighbors(dict_ranked_s_q, file_out):
    #  key: student id, value: dictionary contains the students that have in common at least one question
    dict_neighbors = {}
    for s, q_list in dict_ranked_s_q.items():
        dict_neighbors[s] = {}
        for s2, q_list2 in dict_ranked_s_q.items():
            if common_member(q_list, q_list2):
                dict_neighbors[s][s2] = q_list2
    with open(file_out, 'wb') as f:
        pickle.dump(dict_neighbors, f)
    print("====")


def process_opportunity(row):
    op = row['Opportunity(Default)']
    if '~~' in str(op):
        l = op.split('~~')
        l = [float(i) for i in l]
        return sum(l)/len(l)
    return op


def data_features_op1(data, file_out):

    data = data[[ 'Anon Student Id', 'q_id', 'Step Duration (sec)', 'Correct First Attempt','Incorrects']]
    df1 = data.groupby(['Anon Student Id', 'q_id']).agg({'Correct First Attempt':'max', 'Incorrects':'max',
                                                         'Step Duration (sec)':'mean'})
    df1 = df1.reset_index(level=['Anon Student Id', 'q_id'])
    print(df1.shape)

    df1.apply(creat_dict_student_ques_op1, axis=1) #TODO
    dict_ranked_s_q = {}
    for s_id, s_dict in dict_student_ques_op1.items():
        sorted_s_dict = sorted(s_dict.items(), key=lambda x: x[1])[:80]
        if len(sorted_s_dict) < 3:
            continue
        ranked_questions = dict(sorted_s_dict).keys()
        dict_ranked_s_q[s_id] = list(set(ranked_questions))
    print(len(dict_ranked_s_q))
    # save ranked_dict
    with open(file_out, 'wb') as f:
        pickle.dump(dict_ranked_s_q, f)
    return dict_ranked_s_q


def data_features_op2(data, file_out):
    data = data[[ 'Anon Student Id', 'q_id', 'Step Duration (sec)', 'Correct First Attempt', 'Hints']]
    df1 = data.groupby(['Anon Student Id', 'q_id']).agg({'Correct First Attempt':'max', 'Hints':'max',
                                                         'Step Duration (sec)':'mean'})
    df1 = df1.reset_index(level=['Anon Student Id', 'q_id'])
    df1.apply(creat_dict_student_ques_op2, axis=1) #TODO
    dict_ranked_s_q = {}
    for s_id, s_dict in dict_student_ques_op2.items():
        sorted_s_dict = sorted(s_dict.items(), key=lambda x: x[1])[:80]
        if len(sorted_s_dict) < 3:
            continue
        ranked_questions = dict(sorted_s_dict).keys()
        dict_ranked_s_q[s_id] = list(set(ranked_questions))
    print(len(dict_ranked_s_q))
    # save ranked_dict
    with open(file_out, 'wb') as f:
        pickle.dump(dict_ranked_s_q, f)
    return dict_ranked_s_q


def data_features_op3(data, file_out):

    data = data[[ 'Anon Student Id', 'q_id', 'Step Duration (sec)', 'Opportunity']]
    df1 = data.groupby(['Anon Student Id', 'q_id']).agg({'Opportunity':'min', 'Step Duration (sec)': 'mean'})

    df1 = df1.reset_index(level=['Anon Student Id', 'q_id'])
    df1.apply(creat_dict_student_ques_op3, axis=1) #TODO
    dict_ranked_s_q = {}
    for s_id, s_dict in dict_student_ques_op3.items():
        sorted_s_dict = sorted(s_dict.items(), key=lambda x: x[1])[:80]
        if len(sorted_s_dict) < 3:
            continue
        ranked_questions = dict(sorted_s_dict).keys()
        dict_ranked_s_q[s_id] = list(set(ranked_questions))
    print(len(dict_ranked_s_q))
    # save ranked_dict
    with open(file_out, 'wb') as f:
        pickle.dump(dict_ranked_s_q, f)
    return dict_ranked_s_q

def data_features_op4(data, file_out):
    df1 = data.groupby(['Anon Student Id','q_id']).agg({'Incorrects':'max','Hints':'max','Opportunity':'min'})
    df1 = df1.reset_index(level=['Anon Student Id', 'q_id'])
    df1.apply(creat_dict_student_ques_op4, axis=1) #TODO
    dict_ranked_s_q = {}
    for s_id, s_dict in dict_student_ques_op4.items():
        sorted_s_dict = sorted(s_dict.items(), key=lambda x: x[1])[:80]
        if len(sorted_s_dict) < 3:
            continue
        ranked_questions = dict(sorted_s_dict).keys()
        dict_ranked_s_q[s_id] = list(set(ranked_questions))
    print(len(dict_ranked_s_q))
    # save ranked_dict
    with open(file_out, 'wb') as f:
        pickle.dump(dict_ranked_s_q, f)
    return dict_ranked_s_q


data_path_list = ['algebra_2005_2006/algebra_2005_2006_train.txt', 'algebra_2005_2006/algebra_2005_2006_master.txt']

for x in range(2):
    if x == 0:
        continue
        data = pd.read_csv('sample_data.csv')
        print(data.shape)
        file_out = 'dict_ranked_s_q_train_sample_'
    else:
        data = pd.read_csv(data_path_list[x], delimiter='\t')
        data = data[['Anon Student Id', 'Problem Name', 'Step Name', 'Correct First Attempt', 'Incorrects', 'Hints',
                     'Opportunity(Default)', 'Step Duration (sec)']].dropna()
        file_out = 'dict_ranked_s_q_master_sample_'

    data['Opportunity'] = data.apply(process_opportunity, axis=1)
    data['Opportunity'] = data['Opportunity'] .astype(float)
    data['q_id'] = data.apply(question_id, axis=1)
    data = data[['Anon Student Id', 'q_id', 'Correct First Attempt', 'Incorrects', 'Hints', 'Opportunity',
                 'Step Duration (sec)']]
    print(data.shape)

    """file_out_ = file_out + 'base.pkl'
    dict_ranked_base = data_features_base(data, file_out_)
    if x == 0:
        create_neighbors(dict_ranked_base, "dict_neighbors_base.pkl")


    file_out_ = file_out + 'op1.pkl'
    dict_ranked_op1 = data_features_op1(data, file_out_)
    if x == 0:
        create_neighbors(dict_ranked_op1, "dict_neighbors_op1.pkl")

    file_out_ = file_out + 'op2.pkl'
    dict_ranked_op2 = data_features_op2(data, file_out_)
    if x == 0:
        create_neighbors(dict_ranked_op2, "dict_neighbors_op2.pkl")"""

    file_out_ = file_out + 'op3.pkl'
    dict_ranked_op3 = data_features_op3(data, file_out_)
    if x == 0:
        create_neighbors(dict_ranked_op3, "dict_neighbors_op3.pkl")

    """file_out_ = file_out + 'op4.pkl'
    dict_ranked_op4 = data_features_op4(data, file_out_)
    if x == 0:
        create_neighbors(dict_ranked_op4, "dict_neighbors_op4.pkl")"""

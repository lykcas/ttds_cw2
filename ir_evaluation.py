import string
import copy
from collections import defaultdict
import re


# read from qrels file
f_q = open("qrels.txt")
lines_q = f_q.readlines()
qrels = defaultdict(list)
for line in lines_q:
    pos1 = line.find(':')
    query_number = line[0:int(pos1)]
    query_number = int(query_number)
    qrels.setdefault(query_number, [])
    line = line.split()
    del line[0]
    trantab = str.maketrans(dict.fromkeys(string.punctuation, ' '))
    for item in line:
        item = item.translate(trantab)
        item = item.split()
        qrels[query_number].append(item)

for i in range(1, 2):
    filename = "S" + str(i) + ".results"
    # read
    f_S = open(filename)
    evalname = "S" + str(i) + ".eval"
    # write
    # f__ = open(evalname)

    # read from results file
    lines = f_S.readlines()
    Sresults = defaultdict(list)
    for line in lines:
        line = line.split()
        results_number = int(line[0])
        content_line = line[2: -1]
        if Sresults.get(results_number):
            Sresults[results_number].append(content_line)
        else:
            Sresults.setdefault(results_number, []).append(content_line)

    # P@10 function
    p_at_10 = defaultdict(list)
    p_10_results = []
    for j in range(1, 11):
        p_at_10.setdefault(j, [])
        top10_Sresults = Sresults[j][0: 10]
        top10_docno = [x[0] for x in top10_Sresults]
        for item in top10_docno:
            p_at_10[j].append(item)
        count = 0
        for doc_content in qrels[j]:
            doc_no = doc_content[0]
            if str(doc_no) in p_at_10[j]:
                count += 1
            # try:
            #     p_at_10[j].index(str(doc_no))
            #     flag = 1
            #     count += 1
            # except ValueError:
            #     flag = 0
        precision = count / 10
        p_10_results.append(precision)

    # R@50 function
    r_at_50 = defaultdict(list)
    r_50_results = []
    for j in range(1, 11):
        r_at_50.setdefault(j, [])
        top50_Sresults = Sresults[j][0:50]
        top50_docno = [x[0] for x in top50_Sresults]
        for item in top50_docno:
            r_at_50[j].append(item)
        count = 0
        for doc_content in qrels[j]:
            doc_no = doc_content[0]
            if doc_no in r_at_50[j]:
                count += 1
        recall = count / len(qrels[j])
        r_50_results.append(round(recall, 3))

    # R-precision function
    r_p = defaultdict(list)
    r_p_results = []
    for j in range(1, 11):
        r_p.setdefault(j, [])
        rel = len(qrels[j])
        top_x_Sresults = Sresults[j][0:rel]
        top_x_docno = [x[0] for x in top_x_Sresults]
        for item in top_x_docno:
            r_p[j].append(item)
        count = 0
        for doc_content in qrels[j]:
            doc_no = doc_content[0]
            if doc_no in r_p[j]:
                count += 1
        r_precision = count / rel
        r_p_results.append(round(r_precision, 3))

    # MAP
    map_results = []
    for j in range(1, 11):
        ap_individuals = []
        map_Sresults = Sresults[j][:]
        map_docno = [x[0] for x in map_Sresults]
        map_qrels = qrels[j][:]
        map_qrels_docno = [x[0] for x in map_qrels]
        retrieved_file_position = 1
        relevent_file_position = 1
        for item in map_docno:
            if item in map_qrels_docno:
                ap_individual = relevent_file_position / retrieved_file_position
                ap_individuals.append(ap_individual)
                retrieved_file_position += 1
                relevent_file_position += 1
            else:
                retrieved_file_position += 1
        ap = 0
        for ind in ap_individuals:
            ap += ind
        ap = ap / len(qrels[j])
        map_results.append(round(ap, 3))

    # nDCG@10 有变量名和前两个function重合，为了区分理解，在重合的变量名前加上了n10
    import math
    nDCG_k_results = defaultdict(list)
    nDCG_k_retrieved = defaultdict(list)  # {查询：[docno，rank]}
    ideal_retrieved = defaultdict(list)
    nDCG_sets_retrieved = defaultdict(list)
    ideal_sets_retrieved = defaultdict(list)
    sets = 10

    for j in range(1, 11):
        nDCG_k_retrieved.setdefault(j, [])
        docno_retrieved_all = Sresults[j][:]  # 随着j update
        docno_retrieved = [x[0] for x in docno_retrieved_all]
        docno_qrels = qrels[j][:]
        for docno in docno_retrieved:
            rank = '0'
            for q in docno_qrels:
                if docno in q[0]:
                    rank = q[1]
            temp = [docno, rank]
            nDCG_k_retrieved[j].append(temp)

        ideal_retrieved.setdefault(j, [])
        ideal_retrieved[j] = sorted(nDCG_k_retrieved[j], key=lambda x: x[1], reverse=True)

        nDCG_sets_retrieved.setdefault(j, [])
        nDCG_sets_retrieved[j] = copy.deepcopy(nDCG_k_retrieved[j][0: sets])
        # nDCG_sets_retrieved[j] = nDCG_k_retrieved[j][0: sets]
        k = 1
        dcgk = 0
        for item_n in nDCG_sets_retrieved[j]:
            if k == 1:
                dg = float(item_n[1])
            else:
                dg = float(item_n[1])
                dg = dg / math.log2(k)
                dg = round(dg, 3)
            dcgk += dg
            dcgk = round(dcgk, 3)
            nDCG_sets_retrieved[j][k-1].append(str(dg))
            nDCG_sets_retrieved[j][k-1].append(str(dcgk))
            k += 1

        ideal_sets_retrieved.setdefault(j, [])
        ideal_sets_retrieved[j] = copy.deepcopy(ideal_retrieved[j][0: sets])
        # ideal_sets_retrieved[j] = ideal_retrieved[j][0: sets]
        k = 1
        dcgk = 0
        for item_i in ideal_sets_retrieved[j]:
            if k == 1:
                dg = float(item_i[1])
            else:
                dg = float(item_i[1]) / math.log2(k)
                dg = round(dg, 3)
            dcgk += dg
            dcgk = round(dcgk, 3)
            ideal_sets_retrieved[j][k-1].append(str(dg))
            ideal_sets_retrieved[j][k-1].append(str(dcgk))
            k += 1

        nDCG_k_results.setdefault(j, [])
        flag = ideal_sets_retrieved[j][-1][3]
        dcgk = float(nDCG_sets_retrieved[j][-1][3])
        if flag == '0':
            ndcgk = 0
            nDCG_k_results[j].append(str(ndcgk))
        else:
            ndcgk = dcgk / float(flag)
            ndcgk = round(ndcgk, 3)
        nDCG_k_results[j].append(str(ndcgk))




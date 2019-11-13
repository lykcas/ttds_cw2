import sys
import re


def load_file(input_file):
	with open(input_file,encoding = 'windows-1252') as f:

		text = f.read().splitlines()
	return text

if __name__=='__main__':
	train_file = 'Tweets.14cat.train'
	links_pattern = r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?'
	regex = re.compile(r"[\w']+")
	train_text = load_file(train_file)

	class_id_file = 'classID.txt'
	class_text = load_file(class_id_file)

	class_dict={}
	for line in class_text:
		line = line.split()
		class_dict[' '.join(line[:-1])] = line[-1]

	feats={}

	n = 1
	with open("feats.dict",'w') as d:
		for line in train_text:
			for class_pattern in class_dict:
				if line.endswith(class_pattern)==True:
					line = re.sub(class_pattern,"",line)
			no_links_line = re.sub(links_pattern,"",line)
			term_line = regex.findall(no_links_line)
			for term in term_line[1:]:
				if term not in feats:
					feats[term]=n
					d.write(str(n)+" "+term+"\n")
					n = n + 1
						
		d.close()

	with open("feats.train",'w') as t:
		for line in train_text:
			for class_pattern in class_dict:
				if line.endswith(class_pattern)==True:
					class_id = class_dict[class_pattern]
					line = re.sub(class_pattern,"",line)
			no_links_line = re.sub(links_pattern,"",line)
			term_line = regex.findall(no_links_line)
			if len(term_line)!= 0:
				doc_id = term_line[0]
				class_doc_list=[]
				for term in term_line[1:]:
					if feats[term] not in class_doc_list:
						class_doc_list.append(feats[term])
				class_doc_list.sort()
				string = class_id+" "
				for i in class_doc_list:
					string += " " + str(i)+":1"
				string += "\n"
				t.write(string)
	t.close()









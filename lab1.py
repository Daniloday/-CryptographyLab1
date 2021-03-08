import codecs
from operator import itemgetter
import math
import openpyxl
import xlwt
import pandas as pd

def getTextFromFile():
	text = ''
	with codecs.open('HarryPotter.txt', 'r', encoding = 'utf8') as file:
		text = file.read()
	file.close()
	return text

def filter(abc,text):
	textLower = text.lower()
	textClean = ''
	last = ''
	for sym in textLower:
		if sym == ' ' and last == ' ':
			continue
		if sym == "-" and last != " ":
			textClean += " "
			last = " "
		if sym in abc:
			textClean += sym
			last = sym
	return textClean

def filter2(abc,text):
	textLower = text.lower()
	textClean = ''
	for sym in textLower:
		if sym in abc:
			textClean += sym
	return textClean

def letterFrequency(text):
	data = []
	for sym in text:
		find = False
		for i in range(len(data)):
			if data[i][0] == sym:
				data[i][1] += 1
				find = True
				break
		if not find:
			data.append([sym,1])
	data = sort(data)
	data.reverse()
	return data

def bigramFrequency(text):
	data = []
	for i in range(len(text)-1):
		sym = text[i] + text[i+1]
		find = False
		for i in range(len(data)):
			if data[i][0] == sym:
				data[i][1] += 1
				find = True
				break
		if not find:
			data.append([sym,1])
	data = sort(data)
	data.reverse()
	return data

def bigramFrequency2(text):
	data = []
	j = 0
	while j < len(text) - 1:
		sym = text[j] + text[j+1]
		find = False
		for i in range(len(data)):
			if data[i][0] == sym:
				data[i][1] += 1
				find = True
				break
		if not find:
			data.append([sym,1])
		j += 2
	data = sort(data)
	data.reverse()
	return data

def sort(sub_li): 
    l = len(sub_li) 
    for i in range(0, l): 
        for j in range(0, l-i-1): 
            if (sub_li[j][1] > sub_li[j + 1][1]): 
                tempo = sub_li[j] 
                sub_li[j]= sub_li[j + 1] 
                sub_li[j + 1]= tempo 
    return sub_li

def entropia(freq, num):
	counter = 0
	H = 0
	for sym in freq:
		counter += sym[1]
	for sym in freq:
		p = sym[1]/counter
		sym.append(p)
		H += -p * math.log(p,2)
	return H/num

def helper1(lf):
	letters1 = []
	freq1 = []
	for i in range(len(lf)):
		letters1.append(lf[i][0])
		freq1.append(lf[i][2])
	dict1 = {'Letters': letters1,
                   'Frequency': freq1}
	return dict1

def helper2(abc,bf):
	dict1 = {'' : abc}
	for let in abc:
		freq = []
		for let2 in abc:
			fr = 0
			for i in range(len(bf)):
				if bf[i][0][0] == let2 and bf[i][0][1] == let:
					fr = bf[i][2]
					break
			freq.append(fr)
		dict1[let] = freq
	return dict1

def cout(abc1,abc2,lf1,lf2,bf11,bf12,bf21,bf22):
	
	df1 = pd.DataFrame(helper1(lf1))
	df2 = pd.DataFrame(helper1(lf2))
	df3 = pd.DataFrame(helper2(abc1,bf11))
	df4 = pd.DataFrame(helper2(abc2,bf12))
	df5 = pd.DataFrame(helper2(abc1,bf21))
	df6 = pd.DataFrame(helper2(abc2,bf22))

	with pd.ExcelWriter('output.xlsx') as writer:
		df1.to_excel(writer, sheet_name='LettersWithSpace', index = False)
		df2.to_excel(writer, sheet_name='LettersWithoutSpace', index = False)
		df3.to_excel(writer, sheet_name='BigramsWithSpaceCrossing', index = False)
		df4.to_excel(writer, sheet_name='BigramsWithoutSpaceCrossing', index = False)
		df5.to_excel(writer, sheet_name='BigramsWithSpaceUncrossing', index = False)
		df6.to_excel(writer, sheet_name='BigramsWithoutSpaceUncrossing', index = False)

def main():
	abc1 = (" ","а","б","в","г","д","е","ё","ж","з","и","й","к","л","м","н","о",
            "п","р","с","т","у","ф","х","ц","ч","ш","щ","ъ","ы","ь","э","ю","я")
	abc2 = ("а","б","в","г","д","е","ё","ж","з","и","й","к","л","м","н","о",
            "п","р","с","т","у","ф","х","ц","ч","ш","щ","ъ","ы","ь","э","ю","я")

	text = getTextFromFile()

	# with space
	print("With space:")
	textClean = filter(abc1,text)

	lf1 = letterFrequency(textClean)
	bf11 = bigramFrequency(textClean)
	bf21 = bigramFrequency2(textClean)

	h11 = entropia(lf1,1)
	print("H(1) = ",h11)
	rh11 = 1 - h11/math.log(len(abc1), 2)
	print("R(H1) = ",rh11)
	h21 = entropia(bf11,2)
	print("H(2) = ",h21, " - with crossing")
	rh21 = 1 - h21/math.log(len(abc1), 2)
	print("R(H2) = ",rh21)
	h31 = entropia(bf21,2)
	print("H(2) = ",h31, " - without crossing")
	rh31 = 1 - h31/math.log(len(abc1), 2)
	print("R(H2) = ",rh31)
	print("_____________________")

	# without space
	print("Without space:")
	textClean2 = filter2(abc2,text)

	lf2 = letterFrequency(textClean2)
	bf12 = bigramFrequency(textClean2)
	bf22 = bigramFrequency2(textClean2)

	h12 = entropia(lf2,1)
	print("H(1) = ",h11)
	rh12 = 1 - h12/math.log(len(abc2), 2)
	print("R(H1) = ",rh12)
	h22 = entropia(bf12,2)
	print("H(2) = ",h22, " - with crossing")
	rh22 = 1 - h22/math.log(len(abc2), 2)
	print("R(H2) = ",rh22)
	h32 = entropia(bf22,2)
	print("H(2) = ",h31, " - without crossing")
	rh32 = 1 - h32/math.log(len(abc2), 2)
	print("R(H2) = ",rh32)
	print("_____________________")

	letters = 32
	a10 = 1 - 2.562/math.log(letters,2)
	print("R(H10) = ", a10)
	a20 = 1 - 2.42/math.log(letters,2)
	print("R(H20) = ", a20)
	a30 = 1 - 3.05/math.log(letters,2)
	print("R(H30) = ", a30)

	cout(abc1,abc2,lf1,lf2,bf11,bf12,bf21,bf22)


if __name__ == '__main__':
	main()
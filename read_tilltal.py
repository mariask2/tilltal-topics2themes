import json
import os
import statistics

def get_most_infrequenct(cat_list, freq_dict):
    most_infrueqent = ""
    most_infrequenct_freq = float('inf')
    
    for el in cat_list:
        if freq_dict[el] < most_infrequenct_freq:
            most_infrequenct_freq = freq_dict[el]
            most_infrueqent = el
    return most_infrueqent

dub = open("dubletter.txt")
dupletter = []
for line in dub:
    dupletter.append((line.strip().replace(".txt","")))


f = open('maria-perioder_160-126.json')
data = json.load(f)
current_inspelning = ""
inspelning_counter = 1
categories = {}
huvudrubrik_rubrik_dict = {}
huvudrubrik_dict = {}
for el in data:
    classifications = set(c["Rubrik"].strip() for c in el["klassifikation"])
    huvudrubrik_rubrik = set((c["Huvudrubrik"], c["Rubrik"].strip()) for c in el["klassifikation"])
    for category in classifications:
        if category == "":
            continue
        if category not in categories:
            categories[category] = 1
        else:
            categories[category] = categories[category] + 1
            
    for (h, r) in huvudrubrik_rubrik:
        huvudrubrik_rubrik_dict[r] = h
        if h not in huvudrubrik_dict:
            huvudrubrik_dict[h] = 1
        else:
            huvudrubrik_dict[h] = huvudrubrik_dict[h] + 1

categories[""] = float('inf')

data_label_list = []
for c in categories:
    data_label_list.append({"DATA_LABEL" : c, "DIRECTORY_NAME" : c, "LABEL_COLOR" : "#ccad00" })
print(data_label_list)
print()

classification_dict = {}
classification_statistics = {}
classification_statistics_main = {}
rubrik_label_statistics = {}
rubrik_sub_labels_statistics = {}
underrubrik_benamning_tuples_statistics = {}

nr_of_classifications_list = []
nr_of_sentence_list = []

for el in data:
    if (el["inspelning"]) != current_inspelning:
        current_inspelning = el["inspelning"]
        inspelning_counter = 1

    classifications = []
    main_classifications = []
    rubrik_underrubrik_tuples = []
    underrubrik_benamning_tuples = []
    
    for classification in el["klassifikation"]:
        additional_info = []
        for name in ["Rubrik2", "Rubrik3", "Rubrik4", "Underrubrik", "Benämning"]:
            if classification[name] not in additional_info and classification[name] != "" and classification[name] != classification["Rubrik"]:
                additional_info.append(classification[name])
        
        additional_info_str = ""
        if len(additional_info) > 0:
            additional_info_str = " (" + "/".join(additional_info) + ")"
            
        classification_to_append = classification["Rubrik"].strip() + additional_info_str + " [" + classification["Huvudrubrik"] + "]"
        if len(classification_to_append.replace("[", "").replace("]","").replace(" ", "")) > 0:
            classifications.append(classification_to_append)
        
        if classification["Huvudrubrik"] and classification["Huvudrubrik"] != "":
            main_classifications.append(classification["Huvudrubrik"])
    
        if classification["Rubrik"] and classification["Rubrik"] != "":
            rubrik_underrubrik_tuple = (classification["Rubrik"], classification["Underrubrik"])
            if rubrik_underrubrik_tuple not in rubrik_underrubrik_tuples:
                rubrik_underrubrik_tuples.append(rubrik_underrubrik_tuple)
            if classification["Underrubrik"] != "":
                underrubrik_benamning_tuple = (classification["Rubrik"] + "/" + classification["Underrubrik"], classification["Benämning"])
                if underrubrik_benamning_tuple not in underrubrik_benamning_tuples:
                    underrubrik_benamning_tuples.append(underrubrik_benamning_tuple)
        
    main_classifications = set(main_classifications)
    
    main_folder = "tilltal"
    rubrik_labels = [c["Rubrik"].strip() for c in el["klassifikation"]]
    
    
    infreq = get_most_infrequenct(rubrik_labels, categories) # Use the most infrequent category as the main one
    if infreq == "":
        infreq = "Saknar Rubrik"
    infreq_name = infreq  #.strip().replace(" ", "-").replace(",", "")
    path = os.path.join(main_folder, infreq_name)
    if not os.path.exists(path):
        os.makedirs(path)
    n = current_inspelning + "_" + str(inspelning_counter)
    classifications = list(set(classifications))
    #classification_dict[n] = classifications
    
    if n not in dupletter:
        nr_of_classifications_list.append(len(classifications))
        for stat_cl in classifications:
            if stat_cl not in classification_statistics:
                classification_statistics[stat_cl] = 1
            else:
                classification_statistics[stat_cl] = classification_statistics[stat_cl] + 1
                
        for stat_cl_main in main_classifications:
            if stat_cl_main not in classification_statistics_main:
                classification_statistics_main[stat_cl_main] = 1
            else:
                classification_statistics_main[stat_cl_main] = classification_statistics_main[stat_cl_main] + 1
        
        rubrik_already_added_for_text_list = []
        for (r, u) in rubrik_underrubrik_tuples:
            if r not in rubrik_already_added_for_text_list:
                if r not in rubrik_label_statistics:
                    rubrik_label_statistics[r] = 1
                else:
                    rubrik_label_statistics[r] = rubrik_label_statistics[r] + 1
            rubrik_already_added_for_text_list.append(r)
            if r not in rubrik_sub_labels_statistics:
                rubrik_sub_labels_statistics[r] = {}
            if u not in rubrik_sub_labels_statistics[r]:
                rubrik_sub_labels_statistics[r][u] = 1
            else:
                rubrik_sub_labels_statistics[r][u] = rubrik_sub_labels_statistics[r][u] + 1
        
        for (ur, b) in underrubrik_benamning_tuples:
            if ur not in underrubrik_benamning_tuples_statistics:
                underrubrik_benamning_tuples_statistics[ur] = {}
            if b not in underrubrik_benamning_tuples_statistics[ur]:
                underrubrik_benamning_tuples_statistics[ur][b] = 1
            else:
                underrubrik_benamning_tuples_statistics[ur][b] = underrubrik_benamning_tuples_statistics[ur][b] + 1

    file_name = os.path.join(path, n + ".txt")

    to_file = open(file_name, "w")
    text = el["text"].strip().replace("\n", " <br> ").replace("kl.", "klockan")
    nr_of_sentence_list.append(text.count("."))
    to_file.write(text)
    to_file.close()
  
    inspelning_counter = inspelning_counter + 1

f.close()

#print(classification_dict)
cs_list = sorted([(item, key) for (key, item) in classification_statistics.items()])
cs_list_main = sorted([(item, key) for (key, item) in classification_statistics_main.items()])

rubrik_label_statistics_list = sorted([(item, key) for (key, item) in rubrik_label_statistics.items()], reverse=True)


at_least_five = 0
for (key, item) in cs_list:
    if key >= 5:
        at_least_five = at_least_five  + 1
    print(key, item)

print("********")
at_least_five_main = 0
for (key, item) in cs_list_main:
    if key >= 5:
        at_least_five_main = at_least_five_main  + 1
    print(key, item)

print("len", len(cs_list))
print("at_least_five", at_least_five)

print("len main", len(cs_list_main))
print("at_least_five main ", at_least_five_main)
print("nr_of_classifications_list mean", sum(nr_of_classifications_list)/len(nr_of_classifications_list))
print("nr_of_classifications_list median", statistics.median(nr_of_classifications_list))

print("nr_of_sentence_list mean", sum(nr_of_sentence_list)/len(nr_of_sentence_list))
print("nr_of_sentence_list median", statistics.median(nr_of_sentence_list))

for (nr, item) in rubrik_label_statistics_list:
    if nr >= 20:
        print("*****")
        print(item, nr)
        sub_cateogories = sorted([(item, key) for (key, item) in rubrik_sub_labels_statistics[item].items()], reverse=True)
        for (sub_nr, sub_item) in sub_cateogories:
            if sub_nr >= 10 and sub_item != "":
                print("\t", sub_item, sub_nr)
                benamning_cateogories = sorted([(ii, kk) for (kk, ii) in underrubrik_benamning_tuples_statistics[item + "/" + sub_item].items()], reverse=True)
                for (benamning_nr, benamnming_item) in benamning_cateogories:
                    if benamning_nr >= 10:
                        print("\t\t", benamnming_item, benamning_nr)

        

#print(rubrik_sub_labels)

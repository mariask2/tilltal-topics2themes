import json
import os

def get_most_infrequenct(cat_list, freq_dict):
    most_infrueqent = ""
    most_infrequenct_freq = float('inf')
    
    for el in cat_list:
        if freq_dict[el] < most_infrequenct_freq:
            most_infrequenct_freq = freq_dict[el]
            most_infrueqent = el
    return most_infrueqent


f = open('maria-perioder_160-126.json')
data = json.load(f)
current_inspelning = ""
inspelning_counter = 1
categories = {}
for el in data:
    classifications = set(c["Rubrik"].strip() for c in el["klassifikation"])
    for category in classifications:
        if category == "":
            continue
        if category not in categories:
            categories[category] = 1
        else:
            categories[category] = categories[category] + 1

categories[""] = float('inf')

data_label_list = []
for c in categories:
    data_label_list.append({"DATA_LABEL" : c, "DIRECTORY_NAME" : c, "LABEL_COLOR" : "#ccad00" })
print(data_label_list)
print()

classification_dict = {}
for el in data:
    if (el["inspelning"]) != current_inspelning:
        current_inspelning = el["inspelning"]
        inspelning_counter = 1

    classifications = []
    for classification in el["klassifikation"]:
        additional_info = []
        for name in ["Rubrik2", "Rubrik3", "Rubrik4", "Underrubrik", "Benämning"]:
            if classification[name] not in additional_info and classification[name] != "" and classification[name] != classification["Rubrik"]:
                additional_info.append(classification[name])
        
        additional_info_str = ""
        if len(additional_info) > 0:
            additional_info_str = " (" + "/".join(additional_info) + ")"
        classifications.append(classification["Rubrik"].strip() + additional_info_str + " [" + classification["Huvudrubrik"] + "]")
    
    
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
    
    classification_dict[n] = classifications
    file_name = os.path.join(path, n + ".txt")

    to_file = open(file_name, "w")
    text = el["text"].strip().replace("\n", " <br> ").replace("kl", "klockan")
    to_file.write(text)
    to_file.close()
  
    inspelning_counter = inspelning_counter + 1

f.close()

print(classification_dict)

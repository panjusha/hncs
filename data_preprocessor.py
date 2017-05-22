# Date Created: 19-Apr-2017

import time
import os
from datetime import datetime
import re
import string

start_time = time.time()
print(datetime.now())
print()

# Data preprocessor: clean data

INPUT_FOLDER = '../data/body/nbt/raw/'
OUTPUT_FOLDER = '../data/body/nbt/processed/'

hi_stop_word_lst = ["अंदर", "अत", "अदि", "अप", "अपना", "अपनि", "अपनी", "अपने", "अभि", "अभी", "आदि", "आप", "इंहिं",
                    "इंहें", "इंहों", "इतयादि", "इत्यादि", "इन", "इनका", "इन्हीं", "इन्हें", "इन्हों", "इस", "इसका",
                    "इसकि", "इसकी", "इसके", "इसमें", "इसि", "इसी", "इसे", "उंहिं", "उंहें", "उंहों", "उन", "उनका",
                    "उनकि", "उनकी", "उनके", "उनको", "उन्हीं", "उन्हें", "उन्हों", "उस", "उसके", "उसि", "उसी", "उसे",
                    "एक", "एवं", "एस", "एसे", "ऐसे", "ओर", "और", "कइ", "कई", "कर", "करता", "करते", "करना", "करने",
                    "करें", "कहते", "कहा", "का", "काफि", "काफ़ी", "कि", "किंहें", "किंहों", "कितना", "किन्हें",
                    "किन्हों", "किया", "किर", "किस", "किसि", "किसी", "किसे", "की", "कुछ", "कुल", "के", "को", "कोइ",
                    "कोई", "कोन", "कोनसा", "कौन", "कौनसा", "गया", "घर", "जब", "जहाँ", "जहां", "जा", "जिंहें", "जिंहों",
                    "जितना", "जिधर", "जिन", "जिन्हें", "जिन्हों", "जिस", "जिसे", "जीधर", "जेसा", "जेसे", "जैसा", "जैसे",
                    "जो", "तक", "तब", "तरह", "तिंहें", "तिंहों", "तिन", "तिन्हें", "तिन्हों", "तिस", "तिसे", "तो", "था",
                    "थि", "थी", "थे", "दबारा", "दवारा", "दिया", "दुसरा", "दुसरे", "दूसरे", "दो", "द्वारा", "न", "नहिं",
                    "नहीं", "ना", "निचे", "निहायत", "नीचे", "ने", "पर", "पहले", "पुरा", "पूरा", "पे", "फिर", "बनि",
                    "बनी", "बहि", "बही", "बहुत", "बाद", "बाला", "बिलकुल", "भि", "भितर", "भी", "भीतर", "मगर", "मानो",
                    "मे", "में", "यदि", "यह", "यहाँ", "यहां", "यहि", "यही", "या", "यिह", "ये", "रखें", "रवासा", "रहा",
                    "रहे", "ऱ्वासा", "लिए", "लिये", "लेकिन", "व", "वगेरह", "वरग", "वर्ग", "वह", "वहाँ", "वहां", "वहिं",
                    "वहीं", "वाले", "वुह", "वे", "वग़ैरह", "संग", "सकता", "सकते", "सबसे", "सभि", "सभी", "साथ", "साबुत",
                    "साभ", "सारा", "से", "सो", "हि", "ही", "हुअ", "हुआ", "हुइ", "हुई", "हुए", "हे", "हें", "है", "हैं",
                    "हो", "होता", "होति", "होती", "होते", "होना", "होने"]

hindi_stop_words = set(hi_stop_word_lst)

suffixes = {
    1: ["ो", "े", "ू", "ु", "ी", "ि", "ा"],
    2: ["कर", "ाओ", "िए", "ाई", "ाए", "ने", "नी", "ना", "ते", "ीं", "ती", "ता", "ाँ", "ां", "ों", "ें"],
    3: ["ाकर", "ाइए", "ाईं", "ाया", "ेगी", "ेगा", "ोगी", "ोगे", "ाने", "ाना", "ाते", "ाती", "ाता", "तीं", "ाओं", "ाएं",
        "ुओं", "ुएं", "ुआं"],
    4: ["ाएगी", "ाएगा", "ाओगी", "ाओगे", "एंगी", "ेंगी", "एंगे", "ेंगे", "ूंगी", "ूंगा", "ातीं", "नाओं", "नाएं", "ताओं",
        "ताएं", "ियाँ", "ियों", "ियां"],
    5: ["ाएंगी", "ाएंगे", "ाऊंगी", "ाऊंगा", "ाइयाँ", "ाइयों", "ाइयां"],
}


def hi_stem(word):
    for L in 5, 4, 3, 2, 1:
        if len(word) > L + 1:
            for suf in suffixes[L]:
                if word.endswith(suf):
                    return word[:-L]
    return word


files = [f for f in os.listdir(INPUT_FOLDER) if os.path.isfile(os.path.join(INPUT_FOLDER, f))]

for file in files:

    input_path = os.path.join(INPUT_FOLDER, file)
    output_path = os.path.join(OUTPUT_FOLDER, file)

    # read
    print("Reading", input_path)
    with open(input_path, encoding='utf-8') as input_file:
        lines = input_file.readlines()

    # process
    for i in range(len(lines)):

        # remove non-hindi characters [Hindi char range is \u0900-\u097F and \u20B9 is INR symbol: ₹]
        content = re.sub(u'[^\u20B9\u0900-\u097F]', ' ', lines[i].strip())

        # remove hindi punctuation
        content = re.sub(r'।', ' ', content)  # purna viram
        content = re.sub(r'॥', ' ', content)  # deergh viram

        # stemming + stop word removal
        words = content.split()
        words = [hi_stem(x) for x in words if x not in hindi_stop_words]
        lines[i] = ' '.join(words)

    lines = [x for x in lines if x]

    # write
    print("Writing", output_path)
    with open(output_path, mode='w', encoding='utf-8') as output_file:
        output_file.write('\n'.join(lines))

    print()

print(datetime.now())
print("Total time: %s seconds" % (time.time() - start_time))

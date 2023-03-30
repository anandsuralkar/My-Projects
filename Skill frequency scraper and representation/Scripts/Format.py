# Converts the multi-word designation string into k value for 'naukri.com'
# designation key value with required number of postings.

def format_designation(des, value):
    # for dash '-' separated designation use value False
    # for value '%20' separated return use value True

    words = des.split()
    text = ""
    text += words[0]
    if len(words) > 1:
        for i in range(len(words)-1):
            if value:
                text += "%20"
            else:
                text += "-"
            text += words[i+1]
    print(text)
    return text

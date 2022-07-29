file_perms = list(itertools.permutations(files, 2))
results = {}
for p in file_perms:
    doc_a = p[0]
    doc_b = p[1]

    while True:
        seq_match = SequenceMatcher(a=doc_a, b=doc_b)
        match = seq_match.find_longest_match(0, len(doc_a), 0, len(doc_b)) 

        if (match.size >= 5): 
            doc_a_start, doc_a_stop = match.a, match.a + match.size
            doc_b_start, doc_b_stop = match.b, match.b + match.size 
            match_word = doc_a[doc_a_start:doc_a_stop]

            if match_word in results:
                results[match_word] += 1
            else:
                results[match_word] = 1

            doc_a = doc_a[:doc_a_start] + doc_a[doc_a_stop:]
            doc_b = doc_b[:doc_b_start] + doc_b[doc_b_stop:]
        else: 
            break 

df = pd.DataFrame(
    {
        'Value': [x for x in results.keys()],
        'Count': [x for x in results.values()]
    }
)
print(df)


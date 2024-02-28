file = open('mbox-short.txt')
domainlist = list()
domaindict = dict()
for line in file:
    if line.startswith('From '):
        words = line.split()
        email = words[1]
        domainpos = email.find('@')
        domainname = email[domainpos+1:]
        domainlist.append(domainname)
for domain in domainlist:
    domaindict[domain] = domaindict.get(domain, 0) + 1
print(domaindict)

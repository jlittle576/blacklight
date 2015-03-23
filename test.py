from re import search


sea = search('bush\w+/.*/s\w+', 'bushing/comp/stiffness')

print sea
print bool(sea.groups())
for group in sea.groups():
    print '  ', group
#print sea.group(1)
str1 = "323031303A30383A31332030323A33323A313400"
str2 = "393939393A39393A39392039393A39393A39392E3030"
new_date = "9999:99:99 99:99:99"
temp = ''.join(str(hex(ord(c))[2:]).upper() for c in new_date) + '00'
print(temp)
#new_date_in_hex = ''.join(str(ord(c)) for c in new_date)
#print(new_date_in_hex)
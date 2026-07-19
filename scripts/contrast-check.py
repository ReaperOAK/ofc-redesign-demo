def lin(c):
    c = c/255
    return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4

def lum(h):
    h = h.lstrip('#')
    r,g,b = (int(h[i:i+2],16) for i in (0,2,4))
    return 0.2126*lin(r) + 0.7152*lin(g) + 0.0722*lin(b)

def ratio(a,b):
    la,lb = lum(a), lum(b)
    hi,lo = max(la,lb), min(la,lb)
    return (hi+0.05)/(lo+0.05)

pairs = [
    ("#A16207","#FAFAF9","amber-700 on light surface"),
    ("#A16207","#1C1917","amber-700 on dark surface"),
    ("#F59E0B","#1C1917","amber-500 on dark surface"),
    ("#0C0A09","#F59E0B","near-black text on amber button"),
    ("#0C0A09","#FAFAF9","body text on light surface"),
    ("#FAFAF9","#1C1917","body text on dark surface"),
]
for fg,bg,label in pairs:
    r = ratio(fg,bg)
    body = "PASS" if r>=4.5 else "FAIL"
    large= "PASS" if r>=3.0 else "FAIL"
    print(f"{r:6.2f}:1  body(4.5) {body}  large/UI(3.0) {large}   {label}")

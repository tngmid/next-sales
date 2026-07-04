import pdfplumber

def scraper_2025(pdf_path):
    true_names = {"Retail": "Retail Stores",
                  "Online (UK)": "Online (UK)", 
                  "UK total": "UK Product total",
                  "Online (International)": "Online (International)",
                  "Total NEXT Trading sales (including markdown)": "Product total",
                  "Finance": "NEXT Finance",
                  "Total Platform": "Total Platform",
                  "Franchise, Sourcing, Property & Other": "Other business activities",
                  "Total NEXT sales": "Total NEXT sales",
                  "NEXT's share of sales from investments": "NEXT's share of sales from investments",
                  "Total Group sales": "Total Group sales"}
    
    
    data = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        count = 1
        for p in pdf.pages:
            for t in p.extract_tables():
                try:
                    if "TOTAL GROUP SALES (VAT EX.)" in t[0][0]:
                        rows = t[1:-1]
                        
                        table = {}
                        for r in rows:
                            if "NEXT's share of" in r[0]:
                                r = r[0].split(" ")
                                r = [" ".join(r[0:6])] + [r[6]] + [r[7]]
                            r[0] = true_names[r[0]]
                            r[2] = int(r[2].replace(",",""))
                            table[r[0]] = r[2]
                        data += [table]
                except:
                    continue
            if count == 30:
                break
            count += 1
    return data

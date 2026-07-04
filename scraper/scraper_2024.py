import pdfplumber

def scraper_2024(pdf_path):
    true_names = {"Retail": "Retail Stores",
                  "Online": "Online", 
                  "UK total": "UK Product total",
                  "Total NEXT Trading sales": "Product total",
                  "Finance": "NEXT Finance",
                  "Total Platform": "Total Platform",
                  "Franchise, Sourcing, Property & Other": "Other business activities",
                  "Total NEXT sales": "Total NEXT sales",
                  "Revenue from investments": "NEXT's share of sales from investments",
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
                            if "Total Pl" in r[0]:
                                r[0] = "Total Platform"
                            if "Revenue from investments" in r[0]:
                                r = r[0].split(" ")
                                r = [" ".join(r[0:3])] + [r[3]] + [r[4]]
                            r[0] = true_names[r[0]]
                            r[2] = r[2].replace(",","")
                            table[r[0]] = r[2]
                        data += [table]
                except:
                    continue
            if count == 35:
                break
            count += 1
    return data

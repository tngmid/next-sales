import pdfplumber

def scraper_2023(pdf_path):
    true_names = {"Retail": "Retail Stores",
                  "Online": "Online", 
                  "UK total": "UK Product total",
                  "Total Trading Sales": "Product total",
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
                    if "TOTAL SALES (VAT EX.)" in t[1][0]:
                        rows = t[2:-1]
                        
                        table = {}
                        for r in rows:
                            if r[0] == "":
                                continue
                            r[0] = true_names[r[0]]
                            r[2] = r[2].replace(",","")
                            table[r[0]] = r[2]
                        data += [table]
                except:
                    continue
            if count == 50:
                break
            count += 1
    return data



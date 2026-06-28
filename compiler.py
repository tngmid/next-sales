import pandas as pd
import pdfplumber

pdf_path = "annual-report-and-accounts-jan-2026.pdf"

data = [["Year", "2026", "2025"]]
with pdfplumber.open(str(pdf_path)) as pdf:
    count = 1
    for p in pdf.pages:
        for t in p.extract_tables():
            try:
                if "GROUP SALES AND PROFIT SUMMARY" in t[1][1]:
                    rows = t[1][1].split("\n")
                    excluded = ["Strategic", "Report", "Governance", "Financial", "Statements", "Shareholder", "Information"]
                    rows = [x for x in rows if x not in excluded]
                    
                    start = False
                    for r in rows:
                        if "Retail" in r:
                            start = True
                        if "Statutory" in r:
                            start = False
                            
                        if start:
                            split = [x.replace(",","") for x in r.split(" ")[:-1]]
                            if "Total Group sales" in r:
                                split = ["Total", "Group", "sales"] + [x.replace(",","") for x in r.split(" ")[-3:-1]]
                            if "Other business" in r:
                                split = ["Other", "business", "activities"] + [x.replace(",","") for x in r.split(" ")[-4:-1]]
                            index = next((i for i, x in enumerate(split) if x.isdigit()), len(split))
                            result = [" ".join([i for i in split[:index] if not i.isdigit()])] + [int(x) for x in split[index:] if x.isdigit()]
                            # result = ["NEXT Online", 100, 200]
                            
                            data += [result] 
            except:
                continue
        if count == 30:
            break
        count += 1

df = pd.DataFrame(data).T
df.columns = df.iloc[0]
df = df[1:]
df.to_csv("group_sales.csv", index=False)
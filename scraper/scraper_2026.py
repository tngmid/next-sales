import pdfplumber

def scraper_2026(pdf_path):
    data = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        count = 1
        for p in pdf.pages:
            for t in p.extract_tables():
                table1 = {}
                table2 = {}
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
                                # EXAMPLE: result = ["NEXT Online", 100, 200]
                                
                                table1[result[0]] = result[1]
                                table2[result[0]] = result[2]
                        data += [table1]
                        data += [table2]
                except:
                    continue
            if count == 30:
                break
            count += 1
    return data
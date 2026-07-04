import pandas as pd
from scraper_2026 import scraper_2026
from scraper_2025 import scraper_2025
from scraper_2024 import scraper_2024
from scraper_2023 import scraper_2023

pdf_path = "../reports/annual-report-and-accounts-jan-2026.pdf"
data_2026 = scraper_2026(pdf_path)

pdf_path = "../reports/annual-report-and-accounts-jan-2025.pdf"
data_2025 = scraper_2025(pdf_path)

pdf_path = "../reports/annual-report-and-accounts-jan-2024.pdf"
data_2024 = scraper_2024(pdf_path)

pdf_path = "../reports/annual-reports-and-account-jan-2023.pdf"
data_2023 = scraper_2023(pdf_path)

total_data = data_2026 + data_2025 + data_2024 + data_2023
df = pd.DataFrame(total_data, index=["2026", "2025", "2024", "2023", "2022"])
df["Online"] = df["Online"].fillna(df["Online (UK)"].fillna(0) + df["Online (International)"].fillna(0))
df.drop(columns=["Online (UK)", "Online (International)"], inplace=True)

df.to_csv("../data/group_sales.csv", index=False, encoding="utf-8")

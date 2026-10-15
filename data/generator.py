"""
Synthetic Land Transaction Dataset Generator for JomiGuard.
Generates realistic land plots, registration deeds, and mutation records
with both clean normal chains of title and controlled benchmark anomaly cases.
"""

import random
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import pandas as pd


NAMES_POOL = [
    ("Mohammad Rafiqul Islam", "19782619827361234"),
    ("Fatema Begum", "19852619827361235"),
    ("Abdul Karim Sheikh", "19692619827361236"),
    ("Shahidul Alam", "19822619827361237"),
    ("Nasreen Akhter", "19902619827361238"),
    ("Kamal Hossain", "19752619827361239"),
    ("Salma Khatun", "19882619827361240"),
    ("Zahirul Haque", "19722619827361241"),
    ("Rokeya Sultana", "19932619827361242"),
    ("Tariqul Islam", "19802619827361243"),
    ("Mahmuda Chowdhury", "19862619827361244"),
    ("Moniruzzaman Mia", "19712619827361245"),
    ("Anisur Rahman", "19842619827361246"),
    ("Shamima Nasrin", "19912619827361247"),
    ("Habibur Rahman", "19682619827361248"),
    ("Jannatul Ferdous", "19942619827361249"),
    ("Faruk Ahmed", "19772619827361250"),
    ("Khadija Akter", "19832619827361251"),
    ("Rezaul Karim", "19702619827361252"),
    ("Suraiya Parvin", "19892619827361253"),
]

MOUZAS = [
    {"mouza": "Badda", "jl": 45, "district": "Dhaka", "upazila": "Badda"},
    {"mouza": "Uttara", "jl": 12, "district": "Dhaka", "upazila": "Uttara"},
    {"mouza": "Mirpur", "jl": 28, "district": "Dhaka", "upazila": "Mirpur"},
    {"mouza": "Gulshan", "jl": 19, "district": "Dhaka", "upazila": "Gulshan"},
    {"mouza": "Dhanmondi", "jl": 33, "district": "Dhaka", "upazila": "Dhanmondi"},
    {"mouza": "Savar", "jl": 56, "district": "Dhaka", "upazila": "Savar"},
    {"mouza": "Keraniganj", "jl": 64, "district": "Dhaka", "upazila": "Keraniganj"},
    {"mouza": "Tejgaon", "jl": 15, "district": "Dhaka", "upazila": "Tejgaon"},
]

LAND_TYPES = ["Residential", "Commercial", "Agricultural"]


def generate_synthetic_dataset(num_clean_plots: int = 35) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Generates synthetic plots, deeds, and mutations.
    Includes both clean historical records and planted benchmark anomalies.
    """
    random.seed(42)
    
    plots_data = []
    deeds_data = []
    mutations_data = []
    
    plot_idx = 100
    deed_counter = 1000
    mut_counter = 5000
    
    base_date = datetime(2021, 1, 1)

    # -------------------------------------------------------------
    # 1. Clean Benchmark Plots & Transactions
    # -------------------------------------------------------------
    for i in range(num_clean_plots):
        plot_idx += 1
        plot_id = f"P-{plot_idx}"
        mouza_info = random.choice(MOUZAS)
        dag_no = str(random.randint(100, 9999))
        khatian_no = f"RS-{random.randint(200, 850)}"
        total_area = round(random.uniform(4.0, 25.0), 2)
        land_type = random.choice(LAND_TYPES)
        
        owner_name, owner_nid = random.choice(NAMES_POOL)
        
        plots_data.append({
            "plot_id": plot_id,
            "mouza": mouza_info["mouza"],
            "jl_no": mouza_info["jl"],
            "khatian_no": khatian_no,
            "dag_no": dag_no,
            "total_area_decimals": total_area,
            "district": mouza_info["district"],
            "upazila": mouza_info["upazila"],
            "land_type": land_type,
            "initial_owner_nid": owner_nid,
            "initial_owner_name": owner_name,
        })
        
        # Decide transaction depth (0, 1, or 2 sales)
        txn_depth = random.choices([0, 1, 2], weights=[0.2, 0.5, 0.3])[0]
        curr_owner_name = owner_name
        curr_owner_nid = owner_nid
        curr_date = base_date + timedelta(days=random.randint(30, 200))
        
        for stage in range(txn_depth):
            # Select buyer different from current owner
            available_buyers = [p for p in NAMES_POOL if p[1] != curr_owner_nid]
            buyer_name, buyer_nid = random.choice(available_buyers)
            
            deed_counter += 1
            deed_no = f"REG-{curr_date.year}-{deed_counter}"
            transferred_area = total_area if stage == 0 else round(total_area * random.uniform(0.5, 1.0), 2)
            deed_value = round(transferred_area * random.uniform(300000, 800000), 2)
            
            deeds_data.append({
                "deed_no": deed_no,
                "plot_id": plot_id,
                "registration_date": curr_date.strftime("%Y-%m-%d"),
                "seller_nid": curr_owner_nid,
                "seller_name": curr_owner_name,
                "buyer_nid": buyer_nid,
                "buyer_name": buyer_name,
                "transferred_area_decimals": transferred_area,
                "deed_value_bdt": deed_value,
                "sub_registry_office": f"{mouza_info['upazila']} Sub-Registry Office",
                "status": "Active"
            })
            
            # Legitimate mutation following deed
            mut_date = curr_date + timedelta(days=random.randint(20, 90))
            mut_counter += 1
            mut_case_no = f"MUT-{mut_date.year}-{mut_counter}"
            new_khatian = f"DP-{random.randint(1000, 9999)}"
            
            mutations_data.append({
                "mutation_case_no": mut_case_no,
                "deed_no": deed_no,
                "plot_id": plot_id,
                "mutation_date": mut_date.strftime("%Y-%m-%d"),
                "applicant_nid": buyer_nid,
                "applicant_name": buyer_name,
                "mutated_area_decimals": transferred_area,  # Matches deed
                "new_khatian_no": new_khatian,
                "ac_land_office": f"AC Land Office, {mouza_info['upazila']}",
                "status": "Approved"
            })
            
            # Next owner
            curr_owner_name = buyer_name
            curr_owner_nid = buyer_nid
            curr_date = mut_date + timedelta(days=random.randint(60, 200))

    # -------------------------------------------------------------
    # 2. Planted Benchmark Anomaly Cases
    # -------------------------------------------------------------

    # Anomaly 1: Double-Selling (Plot P-201)
    # Same seller sells the full plot to Buyer A, then 15 days later sells to Buyer B!
    p1_id = "P-201"
    plots_data.append({
        "plot_id": p1_id,
        "mouza": "Badda",
        "jl_no": 45,
        "khatian_no": "RS-410",
        "dag_no": "2401",
        "total_area_decimals": 12.00,
        "district": "Dhaka",
        "upazila": "Badda",
        "land_type": "Residential",
        "initial_owner_nid": "19782619827361234",
        "initial_owner_name": "Mohammad Rafiqul Islam",
    })
    # Sale 1 to Fatema Begum
    deeds_data.append({
        "deed_no": "REG-2023-7001",
        "plot_id": p1_id,
        "registration_date": "2023-03-10",
        "seller_nid": "19782619827361234",
        "seller_name": "Mohammad Rafiqul Islam",
        "buyer_nid": "19852619827361235",
        "buyer_name": "Fatema Begum",
        "transferred_area_decimals": 12.00,
        "deed_value_bdt": 4800000.0,
        "sub_registry_office": "Badda Sub-Registry Office",
        "status": "Active"
    })
    # Sale 2 to Shahidul Alam (Double-Sale!)
    deeds_data.append({
        "deed_no": "REG-2023-7002",
        "plot_id": p1_id,
        "registration_date": "2023-03-25",
        "seller_nid": "19782619827361234",
        "seller_name": "Mohammad Rafiqul Islam",
        "buyer_nid": "19822619827361237",
        "buyer_name": "Shahidul Alam",
        "transferred_area_decimals": 12.00,
        "deed_value_bdt": 5000000.0,
        "sub_registry_office": "Badda Sub-Registry Office",
        "status": "Active"
    })
    # Mutation for Sale 1
    mutations_data.append({
        "mutation_case_no": "MUT-2023-7001",
        "deed_no": "REG-2023-7001",
        "plot_id": p1_id,
        "mutation_date": "2023-05-12",
        "applicant_nid": "19852619827361235",
        "applicant_name": "Fatema Begum",
        "mutated_area_decimals": 12.00,
        "new_khatian_no": "DP-8101",
        "ac_land_office": "AC Land Office, Badda",
        "status": "Approved"
    })

    # Anomaly 2: Area Over-Sale Conflict (Plot P-202)
    # Total area 10.0 dec. Seller sells 6.0 dec to Buyer A, then 8.0 dec to Buyer B (Cumulative 14.0 dec > 10.0 dec!)
    p2_id = "P-202"
    plots_data.append({
        "plot_id": p2_id,
        "mouza": "Uttara",
        "jl_no": 12,
        "khatian_no": "RS-522",
        "dag_no": "3104",
        "total_area_decimals": 10.00,
        "district": "Dhaka",
        "upazila": "Uttara",
        "land_type": "Commercial",
        "initial_owner_nid": "19692619827361236",
        "initial_owner_name": "Abdul Karim Sheikh",
    })
    deeds_data.append({
        "deed_no": "REG-2023-7010",
        "plot_id": p2_id,
        "registration_date": "2023-06-01",
        "seller_nid": "19692619827361236",
        "seller_name": "Abdul Karim Sheikh",
        "buyer_nid": "19902619827361238",
        "buyer_name": "Nasreen Akhter",
        "transferred_area_decimals": 6.00,
        "deed_value_bdt": 3600000.0,
        "sub_registry_office": "Uttara Sub-Registry Office",
        "status": "Active"
    })
    deeds_data.append({
        "deed_no": "REG-2023-7011",
        "plot_id": p2_id,
        "registration_date": "2023-07-15",
        "seller_nid": "19692619827361236",
        "seller_name": "Abdul Karim Sheikh",
        "buyer_nid": "19752619827361239",
        "buyer_name": "Kamal Hossain",
        "transferred_area_decimals": 8.00,
        "deed_value_bdt": 4800000.0,
        "sub_registry_office": "Uttara Sub-Registry Office",
        "status": "Active"
    })

    # Anomaly 3: Area Mismatch - Mutation Area Inflated (Plot P-203)
    # Deed transferred 7.50 dec, but Mutation approved for 12.00 dec (+4.50 dec inflation!)
    p3_id = "P-203"
    plots_data.append({
        "plot_id": p3_id,
        "mouza": "Mirpur",
        "jl_no": 28,
        "khatian_no": "RS-631",
        "dag_no": "4512",
        "total_area_decimals": 15.00,
        "district": "Dhaka",
        "upazila": "Mirpur",
        "land_type": "Residential",
        "initial_owner_nid": "19722619827361241",
        "initial_owner_name": "Zahirul Haque",
    })
    deeds_data.append({
        "deed_no": "REG-2023-7020",
        "plot_id": p3_id,
        "registration_date": "2023-08-10",
        "seller_nid": "19722619827361241",
        "seller_name": "Zahirul Haque",
        "buyer_nid": "19882619827361240",
        "buyer_name": "Salma Khatun",
        "transferred_area_decimals": 7.50,
        "deed_value_bdt": 3000000.0,
        "sub_registry_office": "Mirpur Sub-Registry Office",
        "status": "Active"
    })
    mutations_data.append({
        "mutation_case_no": "MUT-2023-7020",
        "deed_no": "REG-2023-7020",
        "plot_id": p3_id,
        "mutation_date": "2023-10-05",
        "applicant_nid": "19882619827361240",
        "applicant_name": "Salma Khatun",
        "mutated_area_decimals": 12.00,  # INFLATED from 7.50 to 12.00
        "new_khatian_no": "DP-9201",
        "ac_land_office": "AC Land Office, Mirpur",
        "status": "Approved"
    })

    # Anomaly 4: Identity Mismatch - Applicant not the Buyer (Plot P-204)
    # Deed buyer is Rokeya Sultana, but Mutation Applicant is Tariqul Islam!
    p4_id = "P-204"
    plots_data.append({
        "plot_id": p4_id,
        "mouza": "Gulshan",
        "jl_no": 19,
        "khatian_no": "RS-772",
        "dag_no": "5120",
        "total_area_decimals": 8.00,
        "district": "Dhaka",
        "upazila": "Gulshan",
        "land_type": "Commercial",
        "initial_owner_nid": "19862619827361244",
        "initial_owner_name": "Mahmuda Chowdhury",
    })
    deeds_data.append({
        "deed_no": "REG-2023-7030",
        "plot_id": p4_id,
        "registration_date": "2023-09-01",
        "seller_nid": "19862619827361244",
        "seller_name": "Mahmuda Chowdhury",
        "buyer_nid": "19932619827361242",
        "buyer_name": "Rokeya Sultana",
        "transferred_area_decimals": 8.00,
        "deed_value_bdt": 8000000.0,
        "sub_registry_office": "Gulshan Sub-Registry Office",
        "status": "Active"
    })
    mutations_data.append({
        "mutation_case_no": "MUT-2023-7030",
        "deed_no": "REG-2023-7030",
        "plot_id": p4_id,
        "mutation_date": "2023-11-20",
        "applicant_nid": "19802619827361243",  # Differing NID
        "applicant_name": "Tariqul Islam",     # Differing Applicant Name
        "mutated_area_decimals": 8.00,
        "new_khatian_no": "DP-9302",
        "ac_land_office": "AC Land Office, Gulshan",
        "status": "Approved"
    })

    # Anomaly 5: Chronological Paradox - Mutation precedes Deed (Plot P-205)
    # Deed registered on 2024-02-15, but Mutation approved on 2023-10-10!
    p5_id = "P-205"
    plots_data.append({
        "plot_id": p5_id,
        "mouza": "Dhanmondi",
        "jl_no": 33,
        "khatian_no": "RS-890",
        "dag_no": "6201",
        "total_area_decimals": 6.50,
        "district": "Dhaka",
        "upazila": "Dhanmondi",
        "land_type": "Residential",
        "initial_owner_nid": "19712619827361245",
        "initial_owner_name": "Moniruzzaman Mia",
    })
    deeds_data.append({
        "deed_no": "REG-2024-7040",
        "plot_id": p5_id,
        "registration_date": "2024-02-15",
        "seller_nid": "19712619827361245",
        "seller_name": "Moniruzzaman Mia",
        "buyer_nid": "19842619827361246",
        "buyer_name": "Anisur Rahman",
        "transferred_area_decimals": 6.50,
        "deed_value_bdt": 5200000.0,
        "sub_registry_office": "Dhanmondi Sub-Registry Office",
        "status": "Active"
    })
    mutations_data.append({
        "mutation_case_no": "MUT-2023-7040",
        "deed_no": "REG-2024-7040",
        "plot_id": p5_id,
        "mutation_date": "2023-10-10",  # 4 months before deed registration!
        "applicant_nid": "19842619827361246",
        "applicant_name": "Anisur Rahman",
        "mutated_area_decimals": 6.50,
        "new_khatian_no": "DP-9405",
        "ac_land_office": "AC Land Office, Dhanmondi",
        "status": "Approved"
    })

    # Anomaly 6: Phantom Deed Mutation (Plot P-206)
    # Mutation cites a Deed REG-2022-9999 that does not exist in deeds
    p6_id = "P-206"
    plots_data.append({
        "plot_id": p6_id,
        "mouza": "Tejgaon",
        "jl_no": 15,
        "khatian_no": "RS-999",
        "dag_no": "7044",
        "total_area_decimals": 9.00,
        "district": "Dhaka",
        "upazila": "Tejgaon",
        "land_type": "Commercial",
        "initial_owner_nid": "19912619827361247",
        "initial_owner_name": "Shamima Nasrin",
    })
    mutations_data.append({
        "mutation_case_no": "MUT-2023-7050",
        "deed_no": "REG-2022-9999",  # PHANTOM DEED
        "plot_id": p6_id,
        "mutation_date": "2023-04-18",
        "applicant_nid": "19682619827361248",
        "applicant_name": "Habibur Rahman",
        "mutated_area_decimals": 9.00,
        "new_khatian_no": "DP-9508",
        "ac_land_office": "AC Land Office, Tejgaon",
        "status": "Approved"
    })

    # Convert to DataFrames
    df_plots = pd.DataFrame(plots_data)
    df_deeds = pd.DataFrame(deeds_data)
    df_mutations = pd.DataFrame(mutations_data)
    
    return df_plots, df_deeds, df_mutations


def seed_database(db_path: str = "jomiguard.db", schema_path: str = "data/schema.sql") -> Tuple[int, int, int]:
    """
    Initializes the SQLite database schema and inserts synthetic records.
    Returns (num_plots, num_deeds, num_mutations).
    """
    df_plots, df_deeds, df_mutations = generate_synthetic_dataset()
    
    with open(schema_path, "r") as f:
        schema_sql = f.read()
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript(schema_sql)
    
    # Clear existing data before reseeding
    cursor.execute("DELETE FROM alerts")
    cursor.execute("DELETE FROM mutations")
    cursor.execute("DELETE FROM deeds")
    cursor.execute("DELETE FROM plots")
    
    df_plots.to_sql("plots", conn, if_exists="append", index=False)
    df_deeds.to_sql("deeds", conn, if_exists="append", index=False)
    df_mutations.to_sql("mutations", conn, if_exists="append", index=False)
    
    conn.commit()
    conn.close()
    
    return len(df_plots), len(df_deeds), len(df_mutations)


if __name__ == "__main__":
    p_cnt, d_cnt, m_cnt = seed_database()
    print(f"Database seeded successfully with {p_cnt} plots, {d_cnt} deeds, {m_cnt} mutations.")

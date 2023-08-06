#!/usr/bin/env python
# coding: utf-8

# In[6]:


import json
import pandas as pd
import re

from datetime import date
from pathlib import Path

import o2_google_spreadsheet as g
from money2float import money


# In[8]:


def get_json_data(json_filename):
    if json_filename.exists():
        print("Exists")
        with open(json_filename) as json_data:
            data = json.load(json_data)
    return data


# In[10]:


def create_dataframe_from_json(json_data):
    json_lines = json_data["content"]["line_items"]
    line_df = pd.DataFrame(json_lines)
    line_df["group"] = (
        line_df["description"]
        .apply(lambda x: x if "***" in x else None)
        .fillna(method="ffill")
    )
    line_df["group"] = line_df["group"].apply(lambda x: x.strip("***"))
    line_df = line_df.set_index(["group"])
    line_df["qty"] = line_df["qty"].apply(lambda x: money(f"{x}"))
    line_df["unit_price"] = line_df["unit_price"].apply(lambda x: money(f"{x}"))
    line_df["line_total"] = line_df["line_total"].apply(lambda x: money(f"{x}"))
    return line_df


# In[12]:


def get_resources_from_lines(line_df):
    resources_df = line_df.loc["One month salary for different services"]
    resources_df = resources_df.reset_index()
    resources_df = resources_df.drop("group", axis=1)
    resources_df["full_name"] = (
        resources_df["description"]
        .apply(lambda x: x if "Resource:" in x else None)
        .fillna(method="ffill")
    )
    resources_df["full_name"] = resources_df["full_name"].apply(
        lambda x: f"{x}".replace("Resource: ", "")
    )
    resources_df["description"] = resources_df["description"].apply(
        lambda x: "Employee Salary and Direct Cost" if "Resource:" in x else x
    )
    return resources_df


# In[14]:


def get_cloudstaff_fee_from_lines(resources_df, online_data):
    cloudstaff_fee_df = resources_df[resources_df["description"] == "Cloudstaff Fee"]
    cloudstaff_fee_df = cloudstaff_fee_df.groupby(["full_name"]).sum().reset_index()
    cloudstaff_fee_df = cloudstaff_fee_df.merge(online_data, how="left", on="full_name")
    cloudstaff_fee_df["description"] = cloudstaff_fee_df["full_name"] + " service fee"
    cloudstaff_fee_df = cloudstaff_fee_df[
        [
            "billable_client",
            "full_name",
            "description",
            "qty",
            "unit_price",
            "line_total",
        ]
    ]
    return cloudstaff_fee_df


# In[16]:


def get_employee_salary_from_lines(resources_df, online_data):
    employee_salary_df = resources_df[
        resources_df["description"] == "Employee Salary and Direct Cost"
    ]
    employee_salary_df = employee_salary_df.groupby(["full_name"]).sum().reset_index()
    employee_salary_df = employee_salary_df.merge(
        online_data, how="left", on="full_name"
    )
    employee_salary_df["description"] = employee_salary_df["full_name"] + " direct cost"
    employee_salary_df = employee_salary_df[
        [
            "billable_client",
            "full_name",
            "description",
            "qty",
            "unit_price",
            "line_total",
        ]
    ]
    employee_salary_df = employee_salary_df[employee_salary_df["line_total"] != 0]
    return employee_salary_df


# In[ ]:


def get_sss_benefit_from_lines(resources_df, online_data):
    employee_salary_df = resources_df[
        resources_df["description"] == "Employee Salary and Direct Cost"
    ]
    employee_salary_df = employee_salary_df.groupby(["full_name"]).sum().reset_index()
    employee_salary_df = employee_salary_df.merge(
        online_data, how="left", on="full_name"
    )
    employee_salary_df["description"] = employee_salary_df["full_name"] + " direct cost"
    employee_salary_df = employee_salary_df[
        [
            "billable_client",
            "full_name",
            "description",
            "qty",
            "unit_price",
            "line_total",
        ]
    ]
    employee_salary_df = employee_salary_df[employee_salary_df["line_total"] != 0]
    return employee_salary_df


# In[18]:


def get_resource(row):
    if row["line_total"] > 0:
        return row["description"]
    else:
        return None


def get_pay_increase_from_lines(line_df, online_data):
    pay_increase_df = line_df.loc["Synchronization of Pay Increase"].copy()
    pay_increase_df["full_name"] = pay_increase_df.apply(get_resource, axis=1).fillna(
        method="ffill"
    )
    pay_increase_df = pay_increase_df.reset_index()
    pay_increase_description = (
        pay_increase_df.groupby("full_name")["description"]
        .agg(lambda col: " ".join(col))
        .to_frame()
    )
    pay_increase_df = pay_increase_df[pay_increase_df["line_total"] != 0]
    pay_increase_df = pay_increase_df[["full_name", "qty", "unit_price", "line_total"]]
    #     pay_increase_df = pay_increase_df.set_index(['full_name'])
    pay_increase_df = pay_increase_df.join(pay_increase_description)
    pay_increase_df = pay_increase_df.merge(online_data, how="left", on="full_name")
    pay_increase_df = pay_increase_df[
        [
            "billable_client",
            "full_name",
            "description",
            "qty",
            "unit_price",
            "line_total",
        ]
    ]
    return pay_increase_df


# In[71]:


def get_other_charges_from_lines(line_df):
    i = re.compile(r"([A-Z][a-z]+[A-Z]?[a-z]+[A-Z])")
    all_categories = list(line_df.index.unique())
    categories_to_include = [
        "Additional Monthly Charges",
        "Other Charges",
        "Additional PC Items",
        "Visa and Training Costs",
    ]
    categories_to_exclude = [
        "One month salary for different services",
        "Synchronization of Pay Increase",
    ]
    other_charges_df = line_df.loc[categories_to_include]
    other_charges_df = other_charges_df.reset_index()
    other_charges_df["resource"] = other_charges_df.apply(get_resource, axis=1).fillna(
        method="ffill"
    )
    other_charges_description = (
        other_charges_df.groupby("resource")["description"]
        .agg(lambda col: " ".join(col))
        .to_frame()
    )
    other_charges_description["resource_list"] = other_charges_description[
        "description"
    ].apply(lambda x: i.findall(x))
    other_charges_df = other_charges_df.drop(["description"], axis=1)
    other_charges_df = other_charges_df[other_charges_df["line_total"] != 0]
    other_charges_df = other_charges_df.set_index(["resource"]).sort_index()
    other_charges_df = other_charges_df.join(other_charges_description)
    other_charges_df["resource_count"] = other_charges_df["resource_list"].apply(
        lambda x: len(x)
    )
    other_charges_df = other_charges_df.reset_index()
    other_charges_df = other_charges_df.drop(["resource"], axis=1)
    other_charges_df = other_charges_df[
        [
            "group",
            "description",
            "resource_list",
            "resource_count",
            "qty",
            "unit_price",
            "line_total",
        ]
    ]
    return other_charges_df


# In[73]:


def get_unallocated_charges_from_lines(other_charges_df):
    return other_charges_df.loc[other_charges_df["resource_count"] == 0]


# In[75]:


def get_allocated_charges_from_lines(other_charges_df, online_data):
    allocated_charges_df = other_charges_df.loc[
        other_charges_df["resource_count"] > 0
    ].copy()
    allocated_charges_df["id"] = allocated_charges_df.index
    allocated_charges_df = (
        allocated_charges_df["resource_list"]
        .apply(pd.Series)
        .merge(allocated_charges_df, left_index=True, right_index=True)
        .drop(["resource_list"], axis=1)
        .melt(
            id_vars=[
                "id",
                "group",
                "description",
                "resource_count",
                "unit_price",
                "qty",
                "line_total",
            ],
            value_name="cloudstaff_id",
        )
    )

    allocated_charges_df["variable"] = pd.to_numeric(
        allocated_charges_df["variable"], errors="coerce"
    )
    allocated_charges_df = allocated_charges_df.dropna(
        subset=["variable", "cloudstaff_id"]
    )

    def split_fee(row):
        split = row["line_total"] / row["resource_count"]
        return money(split)

    allocated_charges_df["split_fee"] = allocated_charges_df.apply(split_fee, axis=1)
    allocated_charges_df = allocated_charges_df.rename(
        columns={"line_total": "split_total"}
    )
    allocated_charges_df = allocated_charges_df.rename(
        columns={"split_fee": "line_total"}
    )
    allocated_charges_df = allocated_charges_df.merge(
        online_data, how="left", on="cloudstaff_id"
    )
    allocated_charges_df = allocated_charges_df.sort_values("id")
    allocated_charges_df = allocated_charges_df[
        [
            "billable_client",
            "cloudstaff_id",
            "group",
            "description",
            "resource_count",
            "unit_price",
            "qty",
            "split_total",
            "line_total",
        ]
    ]
    return allocated_charges_df


# In[20]:


def write_excel(
    filename,
    employee_salary_df,
    cloudstaff_fee_df,
    sss_benefit_df="",
    pay_increase_df="",
    allocated_charges_df="",
    unallocated_charges_df="",
):
    with pd.ExcelWriter(filename) as writer:
        employee_salary_df.to_excel(
            writer, sheet_name="employee_salary_df", index=False
        )
        cloudstaff_fee_df.to_excel(writer, sheet_name="cloudstaff_fee_df", index=False)
        sss_benefit_df.to_excel(writer, sheet_name="sss_benefit_df", index=False)
        pay_increase_df.to_excel(writer, sheet_name="pay_increase_df", index=False)
        allocated_charges_df.to_excel(
            writer, sheet_name="allocated_charges_df", index=False
        )
        unallocated_charges_df.to_excel(
            writer, sheet_name="unallocated_charges_df", index=False
        )
    return "File written"


# In[79]:


def convert_df_to_xero(
    df, invoice_number, due_date, markup=1, account_code="", tax_type=""
):
    xero_headers = [
        "ContactName",
        "InvoiceNumber",
        "InvoiceDate",
        "DueDate",
        "Description",
        "Quantity",
        "UnitAmount",
        "AccountCode",
        "TaxType",
    ]

    today = date.strftime(date.today(), "%d/%m/%Y")

    column_renamed = {
        "billable_client": "ContactName",
        "line_total": "UnitAmount",
        "description": "Description",
    }
    xero_df = df.rename(columns=column_renamed)
    xero_df["InvoiceNumber"] = invoice_number
    xero_df["InvoiceDate"] = today
    xero_df["DueDate"] = due_date
    xero_df["Quantity"] = "1"
    xero_df["AccountCode"] = account_code
    xero_df["TaxType"] = tax_type
    xero_df = xero_df[xero_headers]
    xero_df["UnitAmount"] = xero_df["UnitAmount"].apply(lambda x: money(x * markup))
    return xero_df


# In[ ]:

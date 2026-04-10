# Project-1---Personal-Closet-Inventory-Resale-Tracker
Personal closet tracker — log fits, tag style, and manage what's for sale.

---
hel
## Description:
This system is a personal closet inventory and resale tracker. It allows a user to log every item they own, like shoes, clothing, handbags, accessories, and more. Each item will have details like brand, size, color, condition, purchase price, and so on. Items will also be tagged with style descriptors (i.e. “vintage,” “streetwear”) for filtering and browsing. You can also create a listing for when an item wants to be sold. This system is designed for personal use, utilizing the idea of digital thrifting and closet organization.

---

## Live App
[Click here to view the live app](https://project-1---personal-closet-inventory-resale-tracker.streamlit.app/)

---

## ERD

![ERD](erd.png)

---

## Table Descriptions

**items** — The core table. Stores every item in the closet with details like name, brand, category, size, color, condition, purchase price, acquired date, and notes.

**tags** — Stores style descriptor tags like "vintage," "designer," and "Y2K" that can be applied to items for flexible filtering.

**item_tags** — Junction table that connects items to tags, creating the many-to-many relationship between the two tables.

**listings** — Tracks resale listings for items. Each listing stores the asking price, platform, status (available, pending, sold), and the date it was listed.

---

## Setup Instructions

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.streamlit/secrets.toml` file with your database connection: DB_URL = "postgresql://retool:npg_Wsm47lXVABfK@ep-solitary-scene-akvttkxc-pooler.c-3.us-west-2.retooldb.com/retool?sslmode=require"
4. Run the app: `streamlit run streamlit_app.py`

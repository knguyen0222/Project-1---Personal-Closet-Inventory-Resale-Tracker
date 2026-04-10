# AI Prompts

*I followed lab 5 replacing my own data*

---

**User (Me):** This is an example code for the dashboard: *insert example code from lab 5*. Can you give me code utilizing this page-by-page plan: *insert page plan for dashboard*.

**AI (Claude):** Here's your dashboard adapted to your closet tracker: *insert dashboard page code here*.

---

**User (Me):** These are my tables for my streamlit app: *insert tables*.

Please create a page called 1_My_Closet.py that does the following:
- Displays all items in a searchable, filterable table. Users can filter by category (shoes, clothing, handbag, etc.) and condition.
- Includes a search bar to find items by name or brand.
- Each row has an Edit button and a Delete button.
- Edit opens a form pre-filled with current values.
- Delete asks for confirmation before removing the record.

**AI (Claude):** This covers everything required for this page — search by name/brand, filter by category and condition, edit form pre-filled with current values, and delete with a confirmation step before anything is removed. All SQL uses parameterized queries with %s, no f-strings. *insert my closet page code*.

---

**User (Me):** I cant see my page on the streamlit app. I pushed it to github, waited, and it's in the pages folder.

**AI (Claude):** The issue is likely that Streamlit hasn't finished redeploying yet, or it needs a manual reboot. Go to your Streamlit app and do this:
1. Click "Manage app" in the bottom right corner
2. Click the three dot menu (⋮)
3. Click "Reboot app"
4. Wait about 30 seconds and refresh the page

The sidebar should show "My Closet" after it reboots.

---

**User (Me):** Can you help me create a 2_Add_Item.py page where it's a form that logs a new item into the closet. Fields: name, brand, category (dropdown), size, condition (dropdown), notes. Also includes a multi-select for tags pulled from the tags table. Validates that name and category are not blank and that purchase price is a positive number if provided.

**AI (Claude):** *insert add item page code*.

A few things worth noting:
- The tags multi-select pulls directly from your tags table — if the table is empty it'll just show an empty multiselect. Add some tags first on the Manage Tags page once that's built.
- Category and condition dropdowns start with an empty option "" so the user is forced to make a selection — this is what triggers the validation error if they skip it.
- After inserting the item, it loops through the selected tags and inserts each one into item_tags using the new item's id from RETURNING id.
- The bottom table shows the 5 most recently added items so the user gets immediate confirmation their item was saved.

---

**User (Me):** Can you help me create a 3_Listings.py page where it displays all current listings with item name, asking price, platform, status, and listed date. Users can filter by status (available, pending, sold). Includes an Add Listing form where the user selects an item from a dropdown pulled from the items table, sets an asking price, platform, and status. Each listing row has an Edit button to update price or status, and a Delete button with confirmation.

**AI (Claude):** *insert listings page code*.

Same structure as 1_My_Closet.py so it should feel familiar. A few things to note:
- The item dropdown pulls directly from your items table and displays as "item name — brand" so it's easy to identify what you're listing.
- If your closet is empty the form disables itself and tells you to add items first.
- The platform dropdown includes the most common resale apps — you can add more if needed.
- Edit only allows changing price, platform, and status — the item itself stays locked since you wouldn't relist a different item on the same listing.

---

**User (Me):** Can you make it so that you can click on different tabs on the same page for add new listing and filter listings.

**AI (Claude):** *insert new code*.

The only real change is wrapping everything in tab1 and tab2 using st.tabs(). Everything else stays exactly the same.

---

**User (Me):** For the add item page, can you add a collapse section for only the add item, keep the recently added the same.

**AI (Claude):** Find this in 2_Add_Item.py: *insert code*.

Replace it with: *insert code*.

And at the very end of the form close out the expander by making sure everything inside the form is indented one extra level. Here's the full updated top section: *insert code*.

The expanded=True means it starts open by default — the user can click the header to collapse it when they don't need it. Everything below the expander (the recently added table) stays exactly the same.

---

**User (Me):** Can you help me create a 3_Manage_Tags.py page where it displays all existing tags in a table. Includes a form to add a new tag. Each tag has a Delete button with confirmation. This page keeps all tag dropdowns up to date.

**AI (Claude):** *insert manage tags page code*.

A couple of things to note:
- The delete confirmation warns the user that deleting a tag will remove it from all items — this works automatically because of the ON DELETE CASCADE you set up on item_tags.
- It catches UniqueViolation specifically so if someone tries to add a duplicate tag they get a clean error message instead of a raw database error.
- Since this page manages the tags that power the multiselect on Add Item, any tag added or deleted here will immediately show up there on the next page load.

---

*Other AI prompts were used to add other designs and cool functions to the pages*

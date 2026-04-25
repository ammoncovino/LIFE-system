# WhatsApp One-Click Migration Kit · v2026-04-25g

**Owner directive:** 46 chats &rarr; 20 organized groups across 4 Communities.

## Files in this folder

| File | What it does |
|------|--------------|
| `WhatsApp_Migration_Kit_v2026-04-25g.pdf` | The full kit — read this first. Group cards, day-of runbook, locked rules. |
| `01_staff_roster_template.csv` | Fill in every staff member: name, phone, site, role, group codes |
| `02_invite_link_sheet.csv` | Already lists the 20 new groups. Paste each invite link as you create them |
| `03_old_chat_inventory.csv` | List your 46 current chats and which new groups they map to |
| `generate_migration_messages.py` | Run once to produce personalized 'click here to move over' messages |
| `04_personalized_migration_messages.txt` | (Generated) one block per old chat — copy-paste, send, done |

## How to start (10 minutes today)

1. Open the PDF.
2. Set up the 4 Communities in WhatsApp (it's the third tab in WhatsApp).
3. Create the 20 groups using the names from the Group Cards section of the PDF.
4. Capture invite links into `02_invite_link_sheet.csv`.
5. Fill `03_old_chat_inventory.csv` with your 46 chats and their target groups.
6. Run `python3 generate_migration_messages.py`.
7. Copy-paste each generated block into the matching old chat.

## Locked rules

- One group = one decision domain
- "Manager on duty" — never a personal name in escalation
- Announcements channels are read-only for non-admins
- Steward orders use one format: ITEM &middot; QTY &middot; NEEDED-BY DATE
- Old chats archive (don't delete) after 48 hours
- New hires go through the roster first, then group adds

What a living thing can sense becomes its reality. Environment shapes design.

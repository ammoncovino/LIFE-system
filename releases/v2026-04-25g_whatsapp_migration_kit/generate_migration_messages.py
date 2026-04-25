#!/usr/bin/env python3
"""
WhatsApp One-Click Migration — message generator.

Reads:
  02_invite_link_sheet.csv (you fill in invite_link for each new group)
  03_old_chat_inventory.csv (you fill in old chats and which new groups they map to)

Writes:
  04_personalized_migration_messages.txt
    - One block per old chat
    - Block contains the exact text to copy-paste into that old chat
    - Each block lists the new group(s) that members of that old chat should join,
      with the actual invite link

Run from inside this folder:
    python3 generate_migration_messages.py
"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).parent
INVITES = HERE / "02_invite_link_sheet.csv"
OLD = HERE / "03_old_chat_inventory.csv"
OUT = HERE / "04_personalized_migration_messages.txt"

def load_invites():
    invites = {}
    with INVITES.open() as f:
        for row in csv.DictReader(f):
            code = row["group_code"].strip()
            if not code or code.startswith("#"):
                continue
            invites[code] = {
                "name": row["group_name"].strip(),
                "community": row["community"].strip(),
                "link": row["invite_link"].strip(),
            }
    return invites

def load_old_chats():
    rows = []
    with OLD.open() as f:
        for row in csv.DictReader(f):
            chat = (row.get("old_chat_name") or "").strip()
            if not chat or chat.startswith("#"):
                continue
            rows.append({
                "chat": chat,
                "maps": [c.strip() for c in (row.get("maps_to_new_groups") or "").split("|") if c.strip()],
                "action": (row.get("action") or "").strip(),
            })
    return rows

def build():
    invites = load_invites()
    old_chats = load_old_chats()
    if not old_chats:
        print("No old chats listed in 03_old_chat_inventory.csv. Add them and re-run.")
        return
    missing = []
    for r in old_chats:
        for code in r["maps"]:
            if code not in invites:
                missing.append((r["chat"], code))
            elif not invites[code]["link"]:
                missing.append((r["chat"], code + " (no link yet)"))
    if missing:
        print("WARNING — these mappings can't generate yet:")
        for chat, code in missing:
            print(f"  - {chat}: {code}")
        print()

    blocks = []
    for r in old_chats:
        chat = r["chat"]
        codes = r["maps"]
        action = r["action"] or "ARCHIVE_AFTER_MIGRATION"

        new_lines = []
        for code in codes:
            inv = invites.get(code)
            if not inv:
                new_lines.append(f"  - {code}: [GROUP NOT YET CREATED]")
                continue
            link = inv["link"] or "[INVITE LINK NOT YET PASTED IN 02_invite_link_sheet.csv]"
            new_lines.append(f"  - {inv['name']}  ({inv['community']})\n    {link}")

        message = (
            "We are organizing all our chats into one cleaner system. "
            "This chat is moving — nothing is lost, but going forward updates will happen in the new group(s) below.\n\n"
            "Tap the link(s) that apply to you and join. If more than one applies, join all of them:\n\n"
            + "\n".join(new_lines)
            + "\n\nQuestions go to the manager on duty. This chat will be archived after everyone has moved."
        )

        blocks.append(
            f"================================================================\n"
            f"OLD CHAT: {chat}\n"
            f"ACTION:   {action}\n"
            f"COPY-PASTE THE BLOCK BELOW INTO THIS CHAT:\n"
            f"----------------------------------------------------------------\n"
            f"{message}\n"
            f"================================================================\n"
        )

    OUT.write_text("\n".join(blocks))
    print(f"Wrote {len(blocks)} migration messages -> {OUT}")

if __name__ == "__main__":
    build()

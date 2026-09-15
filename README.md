# Gayashan & Vishmi — Wedding Invitation

A simple wedding website for **Gayashan & Vishmi**, with an invitation card and a searchable guest seating plan.

**Live site:** [gayahsan.github.io/gayashan-vishmi-wedding](https://gayahsan.github.io/gayashan-vishmi-wedding/)

## Wedding details

| | |
| --- | --- |
| **Date** | Monday, 05 October 2026 |
| **Time** | 9:30 PM |
| **Venue** | Senuri Grand Castello, Negombo Road, Divulapitiya |

## Pages

| File | Purpose |
| --- | --- |
| `index.html` | Redirects to the invitation |
| `card.html` | Wedding invitation, countdown, calendar save, and music |
| `guestList.html` | Guest seating chart with search (135 guests, 15 tables) |

## Features

- Elegant invitation layout with event countdown
- Save-the-date calendar download (`.ics`)
- Guest search by name, with tables and notes
- Soft background music on both pages (tap the music button to unmute)
- Mobile-friendly layout
- Print-friendly seating plan

## Local preview

Open the files in a browser, or serve the folder locally:

```bash
python3 -m http.server 8770
```

Then visit:

- Invitation: [http://127.0.0.1:8770/card.html](http://127.0.0.1:8770/card.html)
- Guest list: [http://127.0.0.1:8770/guestList.html](http://127.0.0.1:8770/guestList.html)

## Hosting

Hosted for free on **GitHub Pages** from the `main` branch.

## Note

Guest names on the seating page currently include placeholder/dummy entries for layout and testing. Replace them with the final guest list before sharing widely.

# Obsidian KB Kit

A pre-built knowledge base for Obsidian. Download it, open it, and start organizing your life in 5 minutes.

## What's Included

- **Clean folder structure** — Inbox, Journal, Projects, Areas, Resources, Archive
- **5 templates** — Daily Note, Project, Meeting, Person, Reading
- **Home dashboard** — Your knowledge base at a glance with live queries
- **AGENTS.md** — AI-readable guide so Claude/GPT can manage your KB for you
- **Visual setup guide** — Beautiful HTML walkthrough with step-by-step instructions

## Who It's For

Anyone who wants to organize their notes, ideas, and life in Obsidian but doesn't want to build a system from scratch. General users, creators, professionals — if you take notes, this works.

## Price

$5-10

---

## Setup Instructions

### Step 1: Install Obsidian

1. Go to [obsidian.md](https://obsidian.md)
2. Download and install Obsidian (free, works on Mac, Windows, Linux, iOS, Android)
3. Open Obsidian

### Step 2: Open the Vault

1. In Obsidian, click **Open folder as vault**
2. Navigate to the `vault` folder from this kit
3. Select it and click **Open**
4. Obsidian may ask about trust — click **Trust author and enable plugins**

### Step 3: Enable Core Plugins

1. Go to **Settings** (gear icon, bottom-left)
2. Click **Core plugins**
3. Enable these:
   - **Daily notes** — for journaling
   - **Templates** — for quick note creation
   - **Backlinks** — for connecting notes
   - **Graph view** — for visualizing connections

### Step 4: Configure Daily Notes

1. In **Settings → Core plugins → Daily notes**
2. Set **New file location** to `01-Journal`
3. Set **Template file location** to `Templates/Daily Note`
4. Now `Cmd+Alt+D` (Mac) or `Ctrl+Alt+D` (Windows) creates today's note

---

## How the System Works

### Folder Structure

```
vault/
├── Home.md              # Your dashboard — start here
├── 00-Inbox/            # Quick capture — dump anything here
├── 01-Journal/          # Daily notes and reflections
├── 02-Projects/         # Active projects with clear goals
├── 03-Areas/            # Ongoing life areas (health, finance, etc.)
├── 04-Resources/        # Reference material, articles, books
├── 05-Archive/          # Completed or inactive stuff
├── Templates/           # Note templates
└── Attachments/         # Images, PDFs, files
```

### The PARA Method

This vault uses a simplified PARA structure:

- **P**rojects — Things with a deadline and a goal
- **A**reas — Ongoing responsibilities (no end date)
- **R**esources — Reference material you want to remember
- **A**rchive — Completed or inactive items

Plus **Inbox** (quick capture) and **Journal** (daily notes).

### Linking Notes

Obsidian uses `[[double brackets]]` to link notes together. This is the core of how your knowledge base works.

**Basic linking:**
```
See also: [[Meeting with Sarah]]
Related: [[Project Alpha]]
```

**Link to a specific section:**
```
See the [[Meeting with Sarah#Action Items]] section
```

**Add display text:**
```
Check the [[Meeting with Sarah|meeting notes]] from last week
```

**Why this matters:** Links create connections between your notes. The Graph View shows you how everything relates. The more you link, the more useful your knowledge base becomes.

### Templates

Templates save time. Instead of formatting every note from scratch, use a template:

1. Create a new note
2. Press `Cmd+P` (Mac) or `Ctrl+P` (Windows)
3. Type `template` and select **Insert template**
4. Pick the template you want

**Available templates:**

| Template | Use For |
|----------|--------|
| Daily Note | Journal entries, daily planning |
| Project | Tracking projects with goals and deadlines |
| Meeting | Meeting notes and action items |
| Person | Contact notes, relationship tracking |
| Reading | Books, articles, videos you've consumed |

### Dataview Queries

The Home dashboard uses Dataview to show live data from your vault. You don't need to do anything — it updates automatically.

**Example: Show active projects**
```dataview
TABLE status, date
FROM "02-Projects"
WHERE status = "active"
SORT date DESC
```

**Example: Show recent notes**
```dataview
TABLE date, file.folder
SORT date DESC
LIMIT 10
```

You can create your own queries in any note. Just wrap the query in triple backticks with `dataview` as the language.

---

## Workflow

### Daily Workflow

1. **Morning:** Open your daily note (or create one)
2. **Throughout the day:** Capture thoughts in Inbox
3. **Evening:** Process Inbox — move notes to the right folder
4. **Weekly:** Review projects, check areas, tidy up

### Capturing Notes

**Quick capture (mobile):**
- Open Obsidian
- Tap the + button
- Type your note
- Leave it in Inbox for later

**From your phone:**
- Use the Obsidian mobile app
- Or email notes to yourself and process later

### Organizing Notes

1. Open your Inbox
2. For each note, ask: "What is this?"
3. Move it to the right folder:
   - Is it a project? → `02-Projects`
   - Is it about a person? → `03-Areas/People`
   - Is it reference material? → `04-Resources`
   - Is it done? → `05-Archive`
4. Add links to related notes
5. Add tags if needed

### Tags

Tags are optional but useful for filtering. Use them consistently:

```
#health #finance #work #learning #idea #todo
```

You can search by tag: click any tag or use `tag:#health` in search.

---

## Tips for Success

1. **Start messy.** Capture first, organize later.
2. **Process your inbox daily.** 5 minutes is enough.
3. **Link everything.** Connections make your KB valuable.
4. **Review weekly.** Look at projects, check areas, tidy up.
5. **Don't overthink it.** There's no perfect system — just use it.
6. **Use templates.** They save time and keep things consistent.
7. **Graph view is your friend.** Open it occasionally to see how things connect.

---

## AI Agent Integration

This kit includes an **AGENTS.md** file that AI agents (like Claude, ChatGPT, or custom bots) can read to understand your knowledge base structure.

**What this means for you:**
- Ask Claude to create notes for you
- Ask Claude to organize your Inbox
- Ask Claude to find related notes
- Ask Claude to generate reports from your KB

Just share the AGENTS.md file with your AI agent, and it'll understand how your vault works.

---

## Need Help?

- [Obsidian Help Docs](https://help.obsidian.md/)
- [Obsidian Forum](https://forum.obsidian.md/)
- [Obsidian Reddit](https://reddit.com/r/ObsidianMD)

---

*Built by [RelayDept](https://relaydept.com) — tools for people who build things.*

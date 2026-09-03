# AGENTS.md — Knowledge Base Agent Guide

This file describes the structure and conventions of this Obsidian knowledge base. AI agents (Claude, GPT, custom bots) should read this file to understand how to create, organize, and manage notes in this vault.

---

## Vault Structure

```
vault/
├── Home.md              # Dashboard — entry point
├── 00-Inbox/            # Unprocessed notes (quick capture)
├── 01-Journal/          # Daily notes (YYYY-MM-DD.md format)
├── 02-Projects/         # Active projects with goals
├── 03-Areas/            # Ongoing life areas
├── 04-Resources/        # Reference material, articles, books
├── 05-Archive/          # Completed/inactive items
├── Templates/           # Note templates (do not modify)
└── Attachments/         # Images, PDFs, binary files
```

---

## Folder Rules

| Folder | Naming | Purpose | Status |
|--------|--------|---------|--------|
| `00-Inbox` | Any | Quick capture, unprocessed | Temporary — process regularly |
| `01-Journal` | `YYYY-MM-DD.md` | Daily notes | Active |
| `02-Projects` | Descriptive slug | Active projects only | Active → Archive when done |
| `03-Areas` | Topic name | Ongoing life areas | Always active |
| `04-Resources` | Descriptive title | Reference material | Always active |
| `05-Archive` | Any | Completed/inactive items | Archived |

---

## Frontmatter Schema

Every note should have YAML frontmatter. Use these fields:

```yaml
---
date: YYYY-MM-DD           # When the note was created
tags: [tag1, tag2]         # Optional tags
status: active|completed|archived  # For projects
type: project|meeting|person|reading|daily  # Note type
---
```

### Required Fields
- `date` — ISO date format (YYYY-MM-DD)
- `tags` — Array, even if empty: `tags: []`

### Optional Fields
- `status` — For projects: `active`, `completed`, or `archived`
- `type` — Note type for filtering

---

## Templates

Templates live in `Templates/` and define the structure for new notes.

### Daily Note Template
**File:** `Templates/Daily Note.md`
**Use for:** Journal entries, daily planning
**Fields:** date, tags

```yaml
---
date: {{date}}
tags: [daily]
---
```

**Sections:** Today's Focus, Notes, Gratitude, Tomorrow

### Project Template
**File:** `Templates/Project.md`
**Use for:** Active projects with goals
**Fields:** date, status, tags

```yaml
---
date: {{date}}
status: active
tags: [project]
---
```

**Sections:** Goal, Status, Notes, Related

### Meeting Template
**File:** `Templates/Meeting.md`
**Use for:** Meeting notes and action items
**Fields:** date, type, tags

```yaml
---
date: {{date}}
type: meeting
tags: [meeting]
---
```

**Sections:** Attendees, Agenda, Notes, Action Items

### Person Template
**File:** `Templates/Person.md`
**Use for:** Contact notes, relationship tracking
**Fields:** date, type, tags

```yaml
---
date: {{date}}
type: person
tags: [person]
---
```

**Sections:** Context, Notes, Related

### Reading Template
**File:** `Templates/Reading.md`
**Use for:** Books, articles, videos consumed
**Fields:** date, type, status, tags

```yaml
---
date: {{date}}
type: reading
status: unread
tags: [reading]
---
```

**Sections:** Source, Key Takeaways, Notes, Rating

---

## Linking Conventions

### Internal Links
Use `[[double brackets]]` to link notes:

```markdown
See [[Meeting with Sarah]] for details.
Related: [[Project Alpha]] and [[Q3 Goals]]
```

### Section Links
Link to specific sections:

```markdown
Review the [[Meeting with Sarah#Action Items]] section.
```

### Display Text
Use display text for cleaner writing:

```markdown
Check the [[Meeting with Sarah|meeting notes]] from last week.
```

### Link Placement
- Add related links in the `## Related` section of notes
- Link inline when referencing other notes naturally
- More links = better graph view = better discoverability

---

## Creating Notes

### Process for Creating a New Note

1. **Determine the type** (daily, project, meeting, person, reading)
2. **Choose the folder** based on type
3. **Apply the template** (insert via `Cmd+P` → "Insert template")
4. **Fill in frontmatter** (date, tags, status if project)
5. **Add content** following the template sections
6. **Add links** to related notes

### Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| Daily | `YYYY-MM-DD.md` | `2026-06-25.md` |
| Project | Descriptive slug | `website-redesign.md` |
| Meeting | `YYYY-MM-DD - Topic.md` | `2026-06-25 - Q3 Planning.md` |
| Person | Full name | `Sarah Chen.md` |
| Resource | Descriptive title | `Atomic Habits Notes.md` |

### File Paths

```
# Daily note
01-Journal/2026-06-25.md

# Project
02-Projects/website-redesign.md

# Meeting
02-Projects/meetings/2026-06-25 - Q3 Planning.md
  OR
03-Areas/Work/meetings/2026-06-25 - Standup.md

# Person
03-Areas/People/Sarah Chen.md

# Resource
04-Resources/Atomic Habits Notes.md
```

---

## Organizing Notes

### Inbox Processing

When processing `00-Inbox`:

1. Read each note
2. Classify: What type of note is this?
3. Move to appropriate folder
4. Apply correct template frontmatter
5. Add links to related notes
6. Add tags if relevant

### Decision Tree

```
Is it a task or project with a deadline?
  → 02-Projects/

Is it about a person or relationship?
  → 03-Areas/People/

Is it a daily thought or journal entry?
  → 01-Journal/

Is it reference material to keep?
  → 04-Resources/

Is it done or no longer relevant?
  → 05-Archive/

Not sure?
  Leave in 00-Inbox until you decide
```

---

## Tags

### Standard Tags

Use these tags consistently:

- `#daily` — Daily journal entries
- `#project` — Project notes
- `#meeting` — Meeting notes
- `#person` — People notes
- `#reading` — Reading/media notes
- `#todo` — Notes with action items
- `#idea` — Ideas andbrainstorms
- `#health` — Health-related
- `#finance` — Financial
- `#work` — Work-related
- `#learning` — Learning and education

### Adding Tags

In frontmatter:
```yaml
tags: [daily, work]
```

In content:
```markdown
#meeting #project
```

---

## Dataview Queries

Dataview is a community plugin that shows live data from your vault.

### Basic Query Structure

````
```dataview
TABLE field1, field2
FROM "folder/path"
WHERE condition
SORT field DESC
LIMIT 10
```
````

### Useful Queries

**Active projects:**
```dataview
TABLE status, date
FROM "02-Projects"
WHERE status = "active"
SORT date DESC
```

**Recent notes:**
```dataview
TABLE date, file.folder
SORT date DESC
LIMIT 10
```

**Notes by tag:**
```dataview
TABLE date, file.folder
WHERE contains(tags, "todo")
SORT date DESC
```

**Unprocessed inbox:**
```dataview
LIST
FROM "00-Inbox"
SORT file.ctime DESC
```

---

## AI Agent Capabilities

With this structure understood, an AI agent can:

### Create Notes
- Generate new notes from templates
- Fill in frontmatter correctly
- Place notes in the right folder
- Add appropriate links and tags

### Organize Notes
- Process the Inbox and move notes
- Suggest folder placement for misplaced notes
- Add missing links between related notes
- Clean up inconsistent formatting

### Search and Retrieve
- Find notes by tag, folder, or content
- Link related notes together
- Generate summaries from multiple notes
- Answer questions about the vault contents

### Maintain the System
- Check for orphan notes (no links in or out)
- Suggest tags for untagged notes
- Archive completed projects
- Keep the structure consistent

---

## Example Agent Prompts

**Create a daily note:**
```
Create today's daily note in 01-Journal using the Daily Note template. 
Add the frontmatter with today's date and tags: [daily].
```

**Process inbox:**
```
Look at all notes in 00-Inbox. For each note, determine what type it is 
and move it to the appropriate folder. Update the frontmatter accordingly.
```

**Find related notes:**
```
Find all notes related to [topic]. Search by tags, content, and links. 
List them with their folders and a brief summary.
```

**Create a project note:**
```
Create a new project note for [project name] in 02-Projects. 
Use the Project template, set status to active, and add relevant links.
```

---

*This file enables AI agents to understand and manage the Obsidian KB Kit vault structure.*

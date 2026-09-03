# 🏠 Home

Your knowledge base at a glance.

## 🔍 Quick Capture
Drop new notes in [[00-Inbox/_index|Inbox]] and organize later.

## 📅 Today
Open your daily note from the calendar or create a new one in [[01-Journal/_index|Journal]].

## 🎯 Active Projects
```dataview
TABLE status, date
FROM "02-Projects"
WHERE status = "active"
SORT date DESC
```

## 📂 Areas
- [[03-Areas/Health|Health]]
- [[03-Areas/Finance|Finance]]
- [[03-Areas/Career|Career]]
- [[03-Areas/Learning|Learning]]

## 📚 Recently Added
```dataview
TABLE date, file.folder
SORT date DESC
LIMIT 10
```

---
*This vault is part of the **Obsidian KB Kit** by [RelayDept](https://relaydept.com).*

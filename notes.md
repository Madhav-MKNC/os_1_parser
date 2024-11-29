# Notes

- **Important:** If WhatsApp updates its export format, the code must be updated to reflect these changes.

## 01 - I straight up delete the first line from the input file (whatsapp.txt)

- The current code assumes and expects the first line of the input `.txt` file (exported from WhatsApp) is: <code>09/11/24, 22:08 - Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more.</code>

- The code removes this first line with file_text.remove_first_line()

## 02 - Code expects the following exported chat format

```
DD/MM/YY, HH:MM - CONTACT: MESSAGE
```

- "DD/MM/YY", "MM/DD/YY" and other formats are valid too.

- "HH:MM" and "HH:MM AM/PM" both valid.

- CONTACT examples - "Madhav", "+1 (647) 877-9224", "+91 97246 54616". I don't know bro I can't trust this one.

- *No regex*: It does simple string manipulation. element between first '-' and first ':' after it -> CONTACT, and rest after it -> MESSAGE.

- *Observation*: Only lines with atleast 2 ":" are relevant message lines. For example, irrelevant lines like "6/21/23, 01:18 - Bhai joined using this group's invite link" and "6/17/23, 12:08 - Bro created group 'group'" has only one ":" (*Exception*: If group name or contact name includes ":")





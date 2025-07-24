# PyCode Collaborative Editor

## Semester 5 Project
This project was developed as part of the Semester 5 curriculum. It demonstrates advanced concepts in collaborative software, real-time networking, and modern UI/UX design using Python and PyQt5.

---

## Project Timeline (July 25, 2025 – November 30, 2025)

### Gantt Chart
```mermaid
gantt
    dateFormat  YYYY-MM-DD
    title PyCode Project Timeline (Sem 5)
    section Planning & Research
    Requirements Gathering      :done,    des1, 2025-07-25, 7d
    Tech Stack Selection       :done,    des2, 2025-08-01, 3d
    section Core Editor
    Basic Editor UI            :done,    ed1, 2025-08-04, 7d
    File Open/Save             :done,    ed2, 2025-08-11, 5d
    Syntax Highlighting        :done,    ed3, 2025-08-16, 5d
    Tabbed Editing             :done,    ed4, 2025-08-21, 4d
    section Project Navigation
    File Explorer (Tree)       :done,    nav1, 2025-08-25, 7d
    Folder/File Creation       :done,    nav2, 2025-09-01, 4d
    Context Menus              :done,    nav3, 2025-09-05, 3d
    section Productivity
    Find/Search                :done,    prod1, 2025-09-08, 3d
    Theme Toggle               :done,    prod2, 2025-09-11, 2d
    Recent Files/Projects      :done,    prod3, 2025-09-13, 2d
    section Collaboration
    WebSocket Server           :done,    collab1, 2025-09-15, 5d
    Client Integration         :done,    collab2, 2025-09-20, 7d
    Real-time Sync             :done,    collab3, 2025-09-27, 7d
    File Open Sync             :done,    collab4, 2025-10-04, 4d
    Multi-file Collab          :done,    collab5, 2025-10-08, 5d
    User Presence              :done,    collab6, 2025-10-13, 3d
    section UX & Error Handling
    Home Page & Navigation     :done,    ux1, 2025-10-16, 5d
    Save Prompts/Exit Safety   :done,    ux2, 2025-10-21, 3d
    Flicker-Free Editing       :done,    ux3, 2025-10-24, 3d
    Status Bar/Presence        :done,    ux4, 2025-10-27, 2d
    section Testing & Polish
    Manual Testing             :done,    test1, 2025-10-29, 7d
    Bug Fixes & Refactoring    :done,    test2, 2025-11-05, 7d
    Documentation              :done,    doc1, 2025-11-12, 7d
    Final Review & Submission  :done,    doc2, 2025-11-19, 11d
```

### Module/Feature Breakdown
- **July 25 – Aug 3:** Requirements, research, and technology selection
- **Aug 4 – Aug 24:** Core editor UI, file open/save, syntax highlighting, tabs
- **Aug 25 – Sep 7:** File explorer, folder/file creation, context menus
- **Sep 8 – Sep 14:** Find/search, theme toggle, recent files
- **Sep 15 – Oct 15:** WebSocket server, client integration, real-time sync, file open sync, multi-file collab, user presence
- **Oct 16 – Oct 29:** Home page, navigation, save prompts, flicker-free editing, status bar
- **Oct 29 – Nov 18:** Manual testing, bug fixes, refactoring, documentation
- **Nov 19 – Nov 30:** Final review, polish, and submission

---

## Design Decisions & Rationale
- **PyQt5 + QScintilla:** Chosen for robust cross-platform GUI and advanced code editing features.
- **WebSocket-based Collaboration:** Enables real-time, low-latency sync for multiple users.
- **Tabbed UI:** Familiar, VSCode-like experience for users.
- **Tree-based File Explorer:** Allows intuitive navigation and file management.
- **Signal/Slot Architecture:** Ensures thread safety and responsive UI.
- **Status Bar for Presence:** Non-intrusive, always-visible user info.
- **Flicker-Free Editing:** Only update editor if content changes, preserve cursor.
- **Safe Exit/Save Prompts:** Prevents accidental data loss.
- **Home Page:** Central hub for project/session management.

---

## UI/UX Choices
- **Modern, clean look:** Large title, clear buttons, dark/light themes.
- **Context menus:** Right-click for file/folder actions.
- **Recent files/projects:** Quick access from home page.
- **Copy session link:** One-click copy for easy sharing.
- **Status bar:** Shows user presence and session info.
- **Responsive layout:** Editor and explorer resize smoothly.

---

## Error Handling & Edge Cases
- **WebSocket disconnects:** Handles server disconnects gracefully.
- **Thread safety:** All UI updates from background threads use signals.
- **File encoding:** Opens files as UTF-8, with error handling for decode errors.
- **Unsaved changes:** Prompts user before closing tabs or exiting.
- **Invalid session links:** Handles join errors with user feedback.

---

## Testing & Quality Assurance
- **Manual testing:** All features tested with multiple users and files.
- **Edge case testing:** File open/close, rapid edits, disconnect/reconnect.
- **Bug tracking:** Issues logged and resolved during development.
- **Code review:** Peer review of major modules and refactors.
- **Documentation:** Comprehensive README and in-code comments.

---

## Future Work & Improvements
- **Per-cursor presence:** Show each user's cursor in real time.
- **Usernames/avatars:** Allow users to set display names and icons.
- **Integrated chat:** In-app chat for session participants.
- **Operational Transform/CRDT:** For true Google Docs-style concurrent editing.
- **File upload/download:** Drag-and-drop and export features.
- **Plugin system:** Allow user extensions and themes.
- **Cloud deployment:** Host server for remote collaboration.
- **Mobile/tablet support:** Responsive UI for all devices.

---

## Acknowledgements
- **Mentors & Faculty:** Thanks to our professors and mentors for guidance.
- **Open Source:** Built on PyQt5, QScintilla, websocket-client, websockets, and more.
- **Classmates:** For feedback and testing.

---

## All Features & Modules (Minute Details)
- **Home Page:**
    - Project/session management, recent files, create/join session, copy link
- **Editor UI:**
    - Tabbed interface, syntax highlighting, line numbers, code folding, autocompletion, tooltips
- **File Explorer:**
    - Tree view, nested folders, file/folder creation, renaming, deletion, context menus
- **Collaboration:**
    - WebSocket server/client, session management, real-time sync, file open sync, multi-file support, user presence
- **Theme & UX:**
    - Light/dark toggle, status bar, responsive layout, modern look
- **Error Handling:**
    - Save prompts, exit confirmation, thread safety, encoding errors, invalid session handling
- **Testing:**
    - Manual, edge cases, bug tracking, code review
- **Documentation:**
    - README, in-code comments, diagrams

---

## Contact
For questions, support, or feedback, open an issue or contact the maintainer.

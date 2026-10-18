# Unsure items, waiting for JP

Moved here whole and unchanged on 2026-10-17 from the top of `C:\Users\jkpxb\code\Project Slowlight`, during the move into the project template. Each item holds content found nowhere else: its files were hashed as git blobs and compared with every object in the repository's history (`git rev-list --objects --all --reflog`, 116 blobs) and with every file kept in the repository folder. Whether that content still matters is JP's call.

Do not `git add` the 5 items below: the repository is public, and they include an 81,446,196-byte installer and `slowlightappv2\` at 572,917,768 bytes, 569,173,480 of them in `slowlight\node_modules\`. Since 2026-10-17 git ignores all 5 through the lines `review/unsure/*` and `!review/unsure/README.md` in `.git\info\exclude`, a rule local to this clone that is not committed. That rule leaves this README.md visible to git, so `git status` lists it and it goes into the repository when the records are committed, while `git add -A` and `git status` skip the items.

| Item | Files | Not found anywhere else | Why unsure |
|---|---|---|---|
| `slowlight\` | 3 | all 3: `app.js` (29,353 bytes), `index.html`, `README.md` | The oldest snapshot (2026-09-01); none of it is in git history. |
| `SlowlightApp\` | 10 | `slowlight\app.js` (31,190 bytes, identical to the one in `slowlightappv2\`) and `slowlight\README.md` | An earlier app.js and README than any commit. |
| `slowlightappv2\` | 7,323 (572,917,768 bytes) | `slowlight\app.js`, `slowlight\package.json`, `slowlight\README.md`, a 93-byte `package-lock.json` with no packages at the folder's top, and 2,109 of the 7,307 files in `slowlight\node_modules\` | An early desktop-app snapshot with its installed dependencies; the dependencies differ from today's `node_modules`. |
| `slowlightV3\` | 16 | `slowlight\README.md` (8,923 bytes) | Every other file is in git history; only this README version is not. |
| `Slow-Light-Setup-0.1.0-Windows.exe` | 1 (81,446,196 bytes, SHA-256 prefix f50ff881584760a7) | the whole installer | Not byte-identical to `apps\Slow-Light-Windows\Slow Light Setup 0.1.0.exe` or to the v0.1.0 release asset on GitHub (both 81,961,408 bytes). |

## Cut on 2026-10-17, with the proof

Sent to the Recycle Bin, so each one can still be restored from there.

| Item | Proof |
|---|---|
| `slowlightV4\` (19 files) | all 19 files are blobs in git history |
| `slowlightV4.zip` and `slowlight-app-git.zip` | byte-identical to each other (SHA-256 prefix c03171a0bc303170); all 19 entries are blobs in git history |
| `slowlight.zip` | all 3 entries are identical to the files in `slowlight\` above |
| `SlowlightApp.zip` | 8 entries in git history, 2 identical to files in `SlowlightApp\` above |
| `slowlightappv2.zip` | 11 entries in git history, 3 identical to files in `slowlightappv2\` and `SlowlightApp\` above |
| `slowlightV3.zip` | 15 entries in git history, 1 identical to `slowlightV3\slowlight\README.md` above |
| `app.js` (top level) | identical to `slowlight\slowlight\app.js` above |

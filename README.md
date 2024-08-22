# arc-to-sqlite

Save data from [Arc Timeline][arc_timeline]'s daily (or monthly) export to a
SQLite database.

[arc_timeline]: https://www.bigpaua.com/arcapp/

# Installation

```bash
foo@bar:~$ pip install -e git+https://github.com/myles/arc-to-sqlite.git#egg=arc-to-sqlite
```

# Usage

You can use the `arc-to-sqlite` command to save data from an Arc App export
to a SQLite database. Arc App's export directory is usually located in
iCloud Drive, `~/Library/Mobile Documents/iCloud~com~bigpaua~LearnerCoacher/`.

```bash
foo@bar:~$ arc-to-sqlite arc.db ~/Library/Mobile\ Documents/iCloud\~com\~bigpaua\~LearnerCoacher/
```


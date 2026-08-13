# Faith‑Trails Champion Test Utility

This utility prepares a separate test player with 17 of the 18 badges. Your real players and their progress are not changed.

## Setup

1. Copy `champion_test_tool.py` into the main Faith‑Trails project folder—the same folder containing `app.py` and `faith_trails.db`.
2. In PowerShell, from that folder, run:

   ```powershell
   python champion_test_tool.py setup
   ```

3. Start the application:

   ```powershell
   python app.py
   ```

4. Select **Champion Test Player**.
5. Complete **Daniel and the Lions' Den on Hard**. It is the only badge left.

The script automatically creates a timestamped database backup inside a `test_backups` folder before preparing the test player.

## Check the test player

```powershell
python champion_test_tool.py status
```

Before the final quest, it should report 17 of 18 badges. After Daniel on Hard, it should report 18 of 18.

## Remove the test player

Close the running Flask application, then run:

```powershell
python champion_test_tool.py cleanup
```

Cleanup removes only the player named **Champion Test Player** and badges tied to that player's database ID. The timestamped backup is retained.

Do not run `init_db.py` for this test.

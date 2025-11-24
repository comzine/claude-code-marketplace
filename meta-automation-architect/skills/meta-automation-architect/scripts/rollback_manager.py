#!/usr/bin/env python3
"""
Rollback Manager
Allows undoing automation if it's not helpful
Creates backups and can restore to pre-automation state
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class RollbackManager:
    """Manages rollback of automation changes"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.backup_dir = Path(f".claude/meta-automation/backups/{session_id}")
        self.manifest_path = self.backup_dir / "manifest.json"
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, description: str = "Automation setup") -> str:
        """
        Create backup before making changes

        Args:
            description: What this backup is for

        Returns:
            Backup ID
        """
        backup_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / backup_id

        # Create backup manifest
        manifest = {
            'backup_id': backup_id,
            'session_id': self.session_id,
            'created_at': datetime.now().isoformat(),
            'description': description,
            'backed_up_files': [],
            'created_files': [],  # Files that didn't exist before
            'can_rollback': True
        }

        # Save manifest
        with open(self.manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        return backup_id

    def track_file_creation(self, file_path: str):
        """
        Track that a file was created by automation

        Args:
            file_path: Path to file that was created
        """
        manifest = self._load_manifest()
        if manifest:
            if file_path not in manifest['created_files']:
                manifest['created_files'].append(file_path)
            self._save_manifest(manifest)

    def backup_file_before_change(self, file_path: str):
        """
        Backup a file before changing it

        Args:
            file_path: Path to file to backup
        """
        manifest = self._load_manifest()
        if not manifest:
            return

        source = Path(file_path)
        if not source.exists():
            return

        # Create backup
        backup_id = manifest['backup_id']
        backup_path = self.backup_dir / backup_id
        backup_path.mkdir(parents=True, exist_ok=True)

        # Preserve directory structure in backup
        rel_path = source.relative_to(Path.cwd()) if source.is_absolute() else source
        dest = backup_path / rel_path

        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)

        # Track in manifest
        if str(rel_path) not in manifest['backed_up_files']:
            manifest['backed_up_files'].append(str(rel_path))
        self._save_manifest(manifest)

    def rollback(self) -> Dict:
        """
        Rollback all automation changes

        Returns:
            Summary of what was rolled back
        """
        manifest = self._load_manifest()
        if not manifest:
            return {
                'success': False,
                'message': 'No backup found for this session'
            }

        if not manifest['can_rollback']:
            return {
                'success': False,
                'message': 'Rollback already performed or backup corrupted'
            }

        files_restored = []
        files_deleted = []
        errors = []

        # Restore backed up files
        backup_id = manifest['backup_id']
        backup_path = self.backup_dir / backup_id

        for file_path in manifest['backed_up_files']:
            try:
                source = backup_path / file_path
                dest = Path(file_path)

                if source.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, dest)
                    files_restored.append(file_path)
                else:
                    errors.append(f"Backup not found: {file_path}")
            except Exception as e:
                errors.append(f"Error restoring {file_path}: {str(e)}")

        # Delete files that were created
        for file_path in manifest['created_files']:
            try:
                path = Path(file_path)
                if path.exists():
                    path.unlink()
                    files_deleted.append(file_path)
            except Exception as e:
                errors.append(f"Error deleting {file_path}: {str(e)}")

        # Mark as rolled back
        manifest['can_rollback'] = False
        manifest['rolled_back_at'] = datetime.now().isoformat()
        self._save_manifest(manifest)

        return {
            'success': len(errors) == 0,
            'files_restored': files_restored,
            'files_deleted': files_deleted,
            'errors': errors,
            'summary': f"Restored {len(files_restored)} files, deleted {len(files_deleted)} files"
        }

    def get_backup_info(self) -> Optional[Dict]:
        """Get information about current backup"""
        manifest = self._load_manifest()
        if not manifest:
            return None

        return {
            'backup_id': manifest['backup_id'],
            'created_at': manifest['created_at'],
            'description': manifest['description'],
            'backed_up_files_count': len(manifest['backed_up_files']),
            'created_files_count': len(manifest['created_files']),
            'can_rollback': manifest['can_rollback'],
            'total_changes': len(manifest['backed_up_files']) + len(manifest['created_files'])
        }

    def preview_rollback(self) -> Dict:
        """
        Preview what would be rolled back

        Returns:
            Details of what would happen
        """
        manifest = self._load_manifest()
        if not manifest:
            return {
                'can_rollback': False,
                'message': 'No backup found'
            }

        return {
            'can_rollback': manifest['can_rollback'],
            'will_restore': manifest['backed_up_files'],
            'will_delete': manifest['created_files'],
            'total_changes': len(manifest['backed_up_files']) + len(manifest['created_files']),
            'created_at': manifest['created_at'],
            'description': manifest['description']
        }

    def _load_manifest(self) -> Optional[Dict]:
        """Load backup manifest"""
        if not self.manifest_path.exists():
            return None

        try:
            with open(self.manifest_path, 'r') as f:
                return json.load(f)
        except:
            return None

    def _save_manifest(self, manifest: Dict):
        """Save backup manifest"""
        with open(self.manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

# Convenience wrapper for use in skills
class AutomationSnapshot:
    """
    Context manager for creating automatic backups

    Usage:
        with AutomationSnapshot(session_id, "Adding security checks") as snapshot:
            # Make changes
            create_new_file("skill.md")
            snapshot.track_creation("skill.md")

            modify_file("existing.md")
            snapshot.track_modification("existing.md")

        # Automatic backup created, can rollback later
    """

    def __init__(self, session_id: str, description: str):
        self.manager = RollbackManager(session_id)
        self.description = description

    def __enter__(self):
        self.manager.create_backup(self.description)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Nothing to do on exit
        pass

    def track_creation(self, file_path: str):
        """Track file creation"""
        self.manager.track_file_creation(file_path)

    def track_modification(self, file_path: str):
        """Track file modification (backs up before change)"""
        self.manager.backup_file_before_change(file_path)

# Example usage
if __name__ == '__main__':
    import tempfile
    import os

    # Create test files
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)

        # Create some test files
        Path("existing.txt").write_text("original content")

        manager = RollbackManager("test-session")

        print("Creating backup...")
        backup_id = manager.create_backup("Test automation setup")

        # Simulate automation changes
        print("\nMaking changes...")
        manager.backup_file_before_change("existing.txt")
        Path("existing.txt").write_text("modified content")

        Path("new_skill.md").write_text("# New Skill")
        manager.track_file_creation("new_skill.md")

        Path("new_command.md").write_text("# New Command")
        manager.track_file_creation("new_command.md")

        # Show backup info
        print("\nBackup info:")
        info = manager.get_backup_info()
        print(json.dumps(info, indent=2))

        # Preview rollback
        print("\nRollback preview:")
        preview = manager.preview_rollback()
        print(json.dumps(preview, indent=2))

        # Perform rollback
        print("\nPerforming rollback...")
        result = manager.rollback()
        print(json.dumps(result, indent=2))

        # Check files
        print("\nFiles after rollback:")
        print(f"existing.txt exists: {Path('existing.txt').exists()}")
        if Path("existing.txt").exists():
            print(f"existing.txt content: {Path('existing.txt').read_text()}")
        print(f"new_skill.md exists: {Path('new_skill.md').exists()}")
        print(f"new_command.md exists: {Path('new_command.md').exists()}")

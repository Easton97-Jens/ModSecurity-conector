"""Boundary controls for explicitly reviewed inheritance metadata updates."""
from __future__ import annotations
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
import unittest
from unittest import mock

SOURCE = Path(__file__).absolute().parents[1] / "bin/update-codex-inheritance.py"
SPEC = importlib.util.spec_from_file_location("inheritance_update", SOURCE)
UPDATER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(UPDATER)

class UpdateInheritanceTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(prefix="inheritance-updater-");self.addCleanup(self.temp.cleanup)
  self.parent=Path(self.temp.name)/"parent";self.child=Path(self.temp.name)/"framework"
  self.source=self.parent/".codex/context/command.md";self.source.parent.mkdir(parents=True)
  self.source.write_bytes(b"Reviewed command boundary.\n");self.sha=UPDATER.digest(self.source.read_bytes())
  self.catalog=self.parent/".codex/inheritance-manifest.toml"
  self.catalog.write_text('schema_version = 2\nrepository = "parent"\n[[policies]]\nid = "PARENT-COMMAND"\nsource = ".codex/context/command.md"\nsha256 = "'+self.sha+'"\ninheritable = true\n')
  self.manifest=self.child/".codex/inheritance-manifest.toml";self.manifest.parent.mkdir(parents=True);self.old='0'*64
  self.initial=('# Header retained\nschema_version = 2\nrepository = "framework"\n\n[[inherit]]\nid = "PARENT-COMMAND"\nparent_sha256 = "'+self.old+'" # comment retained\n\n[[inherit]]\nid = "PARENT-UNCHANGED"\nparent_sha256 = "'+'1'*64+'"\n').encode()
  self.manifest.write_bytes(self.initial);self.manifest.chmod(0o640)
  self.identity=mock.patch.object(UPDATER,"git_identity");self.identity.start();self.addCleanup(self.identity.stop)
 def prepare(self,**changes):
  args=dict(parent=self.parent,target_name="framework",child_root=self.child,expected_manifest=UPDATER.digest(self.manifest.read_bytes()),reviewed={"PARENT-COMMAND":self.sha});args.update(changes)
  return UPDATER.prepare(**args)
 def cli(self,write=False):
  args=['--target','framework','--child-root',str(self.child),'--expected-manifest-sha256',UPDATER.digest(self.manifest.read_bytes()),'--reviewed-policy','PARENT-COMMAND='+self.sha]
  if write:args.append('--write')
  with mock.patch.object(UPDATER,'PARENT',self.parent),contextlib.redirect_stdout(io.StringIO()) as out:
   self.assertEqual(0,UPDATER.main(args))
  return json.loads(out.getvalue())
 def test_dry_run_preserves_bytes_mode_and_inode(self):
  ino=self.manifest.stat().st_ino;self.assertEqual('dry_run',self.cli()['status'])
  self.assertEqual(self.initial,self.manifest.read_bytes());self.assertEqual(ino,self.manifest.stat().st_ino);self.assertEqual(0o640,stat.S_IMODE(self.manifest.stat().st_mode))
 def test_explicit_write_changes_only_selected_bytes_and_preserves_mode(self):
  self.assertEqual('written',self.cli(True)['status'])
  self.assertEqual(self.initial.replace(self.old.encode(),self.sha.encode()),self.manifest.read_bytes());self.assertEqual(0o640,stat.S_IMODE(self.manifest.stat().st_mode))
  self.assertEqual([],list(self.manifest.parent.glob('.inheritance-update-*')))
 def test_wrong_manifest_or_review_hash_refuses_without_write(self):
  for changes in [{'expected_manifest':'f'*64},{'reviewed':{'PARENT-COMMAND':'f'*64}}]:
   with self.subTest(changes=changes),self.assertRaises(UPDATER.Refused):self.prepare(**changes)
   self.assertEqual(self.initial,self.manifest.read_bytes())
 def test_unknown_or_absent_policy_refuses(self):
  with self.assertRaises(UPDATER.Refused):self.prepare(reviewed={'PARENT-UNKNOWN':self.sha})
 def test_empty_duplicate_or_malformed_review_refuses(self):
  for values in [[],['PARENT-COMMAND='+self.sha]*2,['PARENT-COMMAND=BAD'],['OTHER='+self.sha]]:
   with self.subTest(values=values),self.assertRaises(UPDATER.Refused):UPDATER.reviewed_values(values)
 def test_reviewed_source_requires_catalog_update_before_child(self):
  self.source.write_bytes(b"New reviewed semantic contract.\n");sha=UPDATER.digest(self.source.read_bytes())
  with self.assertRaises(UPDATER.Refused):self.prepare(reviewed={'PARENT-COMMAND':sha})
  plan=UPDATER.prepare(self.parent,'parent-catalog',None,UPDATER.digest(self.catalog.read_bytes()),{'PARENT-COMMAND':sha});UPDATER.apply(plan)
  UPDATER.apply(self.prepare(reviewed={'PARENT-COMMAND':sha}));self.assertIn(sha,self.catalog.read_text());self.assertIn(sha,self.manifest.read_text())
 def test_invalid_toml_duplicate_id_or_wrong_role_refuses(self):
  for data in [b'broken = [\n',self.initial.replace(b'"framework"',b'"mrts"',1),self.initial+b'\n[[inherit]]\nid = "PARENT-COMMAND"\nparent_sha256 = "'+b'2'*64+b'"\n']:
   self.manifest.write_bytes(data)
   with self.subTest(data=data[:30]),self.assertRaises(UPDATER.Refused):self.prepare()
   self.assertEqual(data,self.manifest.read_bytes())
 def test_source_traversal_refuses(self):
  self.catalog.write_text(self.catalog.read_text().replace('.codex/context/command.md','.codex/context/../../outside.md'))
  with self.assertRaises(UPDATER.Refused):self.prepare()
 def test_source_symlink_refuses(self):
  real=self.source.with_suffix('.real');self.source.rename(real);self.source.symlink_to(real)
  with self.assertRaises(UPDATER.Refused):self.prepare()
 def test_target_symlink_and_hardlink_refuse(self):
  real=self.manifest.with_suffix('.real');self.manifest.rename(real);self.manifest.symlink_to(real)
  with self.assertRaises(UPDATER.Refused):self.prepare()
  self.manifest.unlink();os.link(real,self.manifest)
  with self.assertRaises(UPDATER.Refused):self.prepare()
 def test_symlinked_ancestor_refuses(self):
  alias=self.parent.parent/'alias';alias.symlink_to(self.child,target_is_directory=True)
  with self.assertRaises(UPDATER.Refused):self.prepare(child_root=alias)
 def test_changed_target_preserves_competing_writer(self):
  plan=self.prepare();other=self.initial+b'# Other writer\n';self.manifest.write_bytes(other)
  with self.assertRaises(UPDATER.Refused):UPDATER.apply(plan)
  self.assertEqual(other,self.manifest.read_bytes())
 def test_changed_source_or_catalog_refuses(self):
  for name in ['source','catalog']:
   plan=self.prepare();path=getattr(self,name);old=path.read_bytes();path.write_bytes(old+b'\n')
   with self.subTest(name=name),self.assertRaises(UPDATER.Refused):UPDATER.apply(plan)
   self.assertEqual(self.initial,self.manifest.read_bytes());path.write_bytes(old)
 def test_replace_failure_preserves_original_and_cleans_temp(self):
  plan=self.prepare()
  with mock.patch.object(UPDATER.os,'replace',side_effect=OSError('fixture failure')):
   with self.assertRaises(OSError):UPDATER.apply(plan)
  self.assertEqual(self.initial,self.manifest.read_bytes());self.assertEqual([],list(self.manifest.parent.glob('.inheritance-update-*')))
 def test_noop_does_not_create_tempfile(self):
  self.manifest.write_bytes(self.initial.replace(self.old.encode(),self.sha.encode()));plan=self.prepare()
  with mock.patch.object(UPDATER.tempfile,'mkstemp',side_effect=AssertionError('no-op writes forbidden')):UPDATER.apply(plan)
 def test_fixed_target_root_contract_refuses_wrong_argument(self):
  with self.assertRaises(UPDATER.Refused):self.prepare(child_root=None)
  with self.assertRaises(UPDATER.Refused):self.prepare(target_name='parent-catalog')
 def test_git_identity_rejects_wrong_top_level_or_origin(self):
  self.identity.stop()
  for outputs in [(str(self.child/'nested'),'https://github.com/Easton97-Jens/ModSecurity-test-Framework.git'),(str(self.child),'https://github.com/other/repository.git')]:
   results=[subprocess.CompletedProcess([],0,(text+'\n').encode()) for text in outputs]
   with self.subTest(outputs=outputs),mock.patch.object(UPDATER.subprocess,'run',side_effect=results),self.assertRaises(UPDATER.Refused):UPDATER.git_identity(self.child,'framework')
  self.identity.start()
 def test_git_identity_accepts_expected_origin(self):
  self.identity.stop();outputs=[str(self.child),'https://github.com/Easton97-Jens/ModSecurity-test-Framework.git'];results=[subprocess.CompletedProcess([],0,(text+'\n').encode()) for text in outputs]
  with mock.patch.object(UPDATER.subprocess,'run',side_effect=results) as calls:UPDATER.git_identity(self.child,'framework')
  self.assertEqual(2,calls.call_count);self.identity.start()

 def test_nonregular_and_oversized_inputs_refuse_without_blocking(self):
  directory=self.parent/'directory';directory.mkdir()
  with self.assertRaises(UPDATER.Refused):UPDATER.read_regular(directory)
  fifo=self.parent/'fifo';os.mkfifo(fifo)
  with self.assertRaises(UPDATER.Refused):UPDATER.read_regular(fifo)
  oversized=self.parent/'oversized';oversized.write_bytes(b'x'*(UPDATER.LIMIT+1))
  with self.assertRaises(UPDATER.Refused):UPDATER.read_regular(oversized)
 def test_fsync_failure_keeps_original_and_cleans_temp(self):
  plan=self.prepare()
  with mock.patch.object(UPDATER.os,'fsync',side_effect=OSError('fixture fsync failure')):
   with self.assertRaises(OSError):UPDATER.apply(plan)
  self.assertEqual(self.initial,self.manifest.read_bytes());self.assertEqual([],list(self.manifest.parent.glob('.inheritance-update-*')))
 def test_noninheritable_policy_refuses_child_write(self):
  self.catalog.write_text(self.catalog.read_text().replace('inheritable = true','inheritable = false'))
  with self.assertRaises(UPDATER.Refused):self.prepare()
 def test_wrong_schema_refuses(self):
  self.manifest.write_bytes(self.initial.replace(b'schema_version = 2',b'schema_version = 99'))
  with self.assertRaises(UPDATER.Refused):self.prepare()

if __name__ == '__main__':unittest.main()

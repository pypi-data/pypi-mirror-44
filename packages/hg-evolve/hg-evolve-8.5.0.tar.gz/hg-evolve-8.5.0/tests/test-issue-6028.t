This test file test the #6028 issue

evolve fails with mercurial.error.ProgrammingError: unsupported changeid '' of type <type 'str'>

https://bz.mercurial-scm.org/show_bug.cgi?id=6028

Global setup
============

  $ . $TESTDIR/testlib/common.sh
  $ cat >> $HGRCPATH <<EOF
  > [ui]
  > interactive = true
  > [phases]
  > publish=False
  > [extensions]
  > evolve =
  > topic =
  > EOF

Test
====

  $ hg init $TESTTMP/issue-6028
  $ cd $TESTTMP/issue-6028

create initial commit
  $ echo "0" > 0
  $ hg ci -Am 0
  adding 0


  $ hg up default
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg topics a
  marked working directory as topic: a
  $ echo "a" > a
  $ hg ci -Am a
  adding a
  active topic 'a' grew its first changeset
  (see 'hg help topics' for more information)


  $ hg up default
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ hg topics b
  marked working directory as topic: b
  $ echo "b" > b
  $ hg ci -Am b
  adding b
  active topic 'b' grew its first changeset
  (see 'hg help topics' for more information)

  $ hg up default
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ hg branch integration
  marked working directory as branch integration

  $ hg merge a
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ hg ci -m "merged a"

  $ hg merge b
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ hg ci -m "merged b"

  $ hg up a
  switching to topic a
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo "a bad commit" >> a_bad_commit
  $ hg add a_bad_commit
  $ hg ci -m "a bad commit"
  $ hg up integration
  1 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ hg merge a
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ hg ci -m "merged a bad commit"

  $ hg up a
  switching to topic a
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo "aa" >> a
  $ hg ci -m "aa"
  $ hg up integration
  2 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge a
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ hg ci -m "merged aa"

  $ hg up b
  switching to topic b
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ echo "bb" >> b
  $ hg ci -m "bb"
  $ hg up integration
  3 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg merge b
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  (branch merge, don't forget to commit)
  $ hg ci -m "merged bb"

create instability by pruning two changesets, one in a topic, one in a merge
  $ hg prune -r 5:6
  2 changesets pruned
  3 new orphan changesets

  $ hg up 4
  2 files updated, 0 files merged, 1 files removed, 0 files unresolved

start the evolve
  $ hg evolve
  move:[8] merged aa
  atop:[4] merged b
  working directory is now at c920dd828523

evolve creates an obsolete changeset above as 11
  $ hg evolve -r .
  cannot solve instability of c920dd828523, skipping
  cannot solve instability of c920dd828523, skipping

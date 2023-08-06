=================================================
Tests the resolution of content divergence: stack
=================================================

This file intend to cover case with stacks of divergent changesets

  $ cat >> $HGRCPATH <<EOF
  > [alias]
  > glog = log -GT "{rev}:{node|short} {desc|firstline}\n ({bookmarks}) [{branch}] {phase}"
  > [phases]
  > publish = False
  > [extensions]
  > rebase =
  > EOF
  $ echo "evolve=$(echo $(dirname $TESTDIR))/hgext3rd/evolve/" >> $HGRCPATH

Resolving content-divergence of a stack with same parents
---------------------------------------------------------

  $ hg init stacktest
  $ cd stacktest
  $ echo ".*\.orig" > .hgignore
  $ hg add .hgignore
  $ hg ci -m "added hgignore"
  $ for ch in a b c d; do echo foo > $ch; hg add $ch; hg ci -qm "added "$ch; done;

  $ hg glog
  @  4:c41c793e0ef1 added d
  |   () [default] draft
  o  3:ca1b80f7960a added c
  |   () [default] draft
  o  2:b1661037fa25 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ cd ..
  $ hg init stack2
  $ cd stack2
  $ hg pull ../stacktest
  pulling from ../stacktest
  requesting all changes
  adding changesets
  adding manifests
  adding file changes
  added 5 changesets with 5 changes to 5 files
  new changesets 8fa14d15e168:c41c793e0ef1 (5 drafts)
  (run 'hg update' to get a working copy)
  $ hg glog
  o  4:c41c793e0ef1 added d
  |   () [default] draft
  o  3:ca1b80f7960a added c
  |   () [default] draft
  o  2:b1661037fa25 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg up c7586e2a9264
  2 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ echo bar > a
  $ hg amend -m "watbar to a"
  3 new orphan changesets
  $ echo wat > a
  $ hg amend -m "watbar to a"
  $ hg evolve --all
  move:[2] added b
  atop:[6] watbar to a
  move:[3] added c
  move:[4] added d
  working directory is now at 15c781f93cac
  $ hg glog
  @  9:15c781f93cac added d
  |   () [default] draft
  o  8:9e5fb1d5b955 added c
  |   () [default] draft
  o  7:88516dccf68a added b
  |   () [default] draft
  o  6:82b74d5dc678 watbar to a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ cd ../stacktest
  $ hg up .^^^
  0 files updated, 0 files merged, 3 files removed, 0 files unresolved
  $ echo wat > a
  $ hg amend -m "watbar to a"
  3 new orphan changesets
  $ hg evolve --all
  move:[2] added b
  atop:[5] watbar to a
  move:[3] added c
  move:[4] added d
  working directory is now at c72d2885eb51
  $ hg glog
  @  8:c72d2885eb51 added d
  |   () [default] draft
  o  7:3ce4be6d8e5e added c
  |   () [default] draft
  o  6:d5f148423c16 added b
  |   () [default] draft
  o  5:8e222f257bbf watbar to a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg pull ../stack2
  pulling from ../stack2
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 4 changesets with 0 changes to 4 files (+1 heads)
  5 new obsolescence markers
  8 new content-divergent changesets
  new changesets 82b74d5dc678:15c781f93cac (4 drafts)
  (run 'hg heads' to see heads, 'hg merge' to merge)

  $ hg glog
  *  12:15c781f93cac added d
  |   () [default] draft
  *  11:9e5fb1d5b955 added c
  |   () [default] draft
  *  10:88516dccf68a added b
  |   () [default] draft
  *  9:82b74d5dc678 watbar to a
  |   () [default] draft
  | @  8:c72d2885eb51 added d
  | |   () [default] draft
  | *  7:3ce4be6d8e5e added c
  | |   () [default] draft
  | *  6:d5f148423c16 added b
  | |   () [default] draft
  | *  5:8e222f257bbf watbar to a
  |/    () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg evolve --all --content-divergent
  merge:[5] watbar to a
  with: [9] watbar to a
  base: [1] added a
  updating to "local" side of the conflict: 8e222f257bbf
  merging "other" content-divergent changeset '82b74d5dc678'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  6 new orphan changesets
  merge:[6] added b
  with: [10] added b
  base: [2] added b
  updating to "local" side of the conflict: d5f148423c16
  merging "other" content-divergent changeset '88516dccf68a'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  merge:[7] added c
  with: [11] added c
  base: [3] added c
  updating to "local" side of the conflict: 3ce4be6d8e5e
  merging "other" content-divergent changeset '9e5fb1d5b955'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  merge:[8] added d
  with: [12] added d
  base: [4] added d
  updating to "local" side of the conflict: c72d2885eb51
  merging "other" content-divergent changeset '15c781f93cac'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory is now at 038fe7db3d88

  $ hg glog
  @  16:038fe7db3d88 added d
  |   () [default] draft
  o  15:b2cac10f3836 added c
  |   () [default] draft
  o  14:eadfd9d70680 added b
  |   () [default] draft
  o  13:f66f262fff6c watbar to a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft
Resolving content-divergence of a stack with different parents
---------------------------------------------------------

  $ cd ..
  $ hg init stackrepo1
  $ cd stackrepo1
  $ echo ".*\.orig" > .hgignore
  $ hg add .hgignore
  $ hg ci -m "added hgignore"

  $ for ch in a b c d;
  > do echo foo > $ch;
  > hg add $ch;
  > hg ci -qm "added "$ch;
  > done;

  $ hg glog
  @  4:c41c793e0ef1 added d
  |   () [default] draft
  o  3:ca1b80f7960a added c
  |   () [default] draft
  o  2:b1661037fa25 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ cd ..
  $ hg init stackrepo2
  $ cd stackrepo2
  $ hg pull ../stackrepo1
  pulling from ../stackrepo1
  requesting all changes
  adding changesets
  adding manifests
  adding file changes
  added 5 changesets with 5 changes to 5 files
  new changesets 8fa14d15e168:c41c793e0ef1 (5 drafts)
  (run 'hg update' to get a working copy)

  $ hg glog
  o  4:c41c793e0ef1 added d
  |   () [default] draft
  o  3:ca1b80f7960a added c
  |   () [default] draft
  o  2:b1661037fa25 added b
  |   () [default] draft
  o  1:c7586e2a9264 added a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg up 8fa14d15e168
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ echo newfile > newfile
  $ hg ci -Am "add newfile"
  adding newfile
  created new head
  $ hg rebase -s c7586e2a9264 -d .
  rebasing 1:c7586e2a9264 "added a"
  rebasing 2:b1661037fa25 "added b"
  rebasing 3:ca1b80f7960a "added c"
  rebasing 4:c41c793e0ef1 "added d"

  $ hg glog
  o  9:d45f050514c2 added d
  |   () [default] draft
  o  8:8ed612937375 added c
  |   () [default] draft
  o  7:6eb54b5af3fb added b
  |   () [default] draft
  o  6:c04ff147ef79 added a
  |   () [default] draft
  @  5:2228e3b74514 add newfile
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ cd ../stackrepo1
  $ hg up .^^^
  0 files updated, 0 files merged, 3 files removed, 0 files unresolved
  $ echo wat > a
  $ hg amend -m "watbar to a"
  3 new orphan changesets
  $ hg evolve --all
  move:[2] added b
  atop:[5] watbar to a
  move:[3] added c
  move:[4] added d
  working directory is now at c72d2885eb51

  $ hg glog
  @  8:c72d2885eb51 added d
  |   () [default] draft
  o  7:3ce4be6d8e5e added c
  |   () [default] draft
  o  6:d5f148423c16 added b
  |   () [default] draft
  o  5:8e222f257bbf watbar to a
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg pull ../stackrepo2
  pulling from ../stackrepo2
  searching for changes
  adding changesets
  adding manifests
  adding file changes
  added 5 changesets with 1 changes to 5 files (+1 heads)
  4 new obsolescence markers
  8 new content-divergent changesets
  new changesets 2228e3b74514:d45f050514c2 (5 drafts)
  (run 'hg heads' to see heads, 'hg merge' to merge)

  $ hg glog
  *  13:d45f050514c2 added d
  |   () [default] draft
  *  12:8ed612937375 added c
  |   () [default] draft
  *  11:6eb54b5af3fb added b
  |   () [default] draft
  *  10:c04ff147ef79 added a
  |   () [default] draft
  o  9:2228e3b74514 add newfile
  |   () [default] draft
  | @  8:c72d2885eb51 added d
  | |   () [default] draft
  | *  7:3ce4be6d8e5e added c
  | |   () [default] draft
  | *  6:d5f148423c16 added b
  | |   () [default] draft
  | *  5:8e222f257bbf watbar to a
  |/    () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft

  $ hg evolve --all --content-divergent
  merge:[10] added a
  with: [5] watbar to a
  base: [1] added a
  rebasing "other" content-divergent changeset 8e222f257bbf on 2228e3b74514
  updating to "local" side of the conflict: c04ff147ef79
  merging "other" content-divergent changeset '186bdc2cdfa2'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  6 new orphan changesets
  merge:[11] added b
  with: [6] added b
  base: [2] added b
  rebasing "other" content-divergent changeset d5f148423c16 on c04ff147ef79
  updating to "local" side of the conflict: 6eb54b5af3fb
  merging "other" content-divergent changeset '8542f15656e7'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  merge:[12] added c
  with: [7] added c
  base: [3] added c
  rebasing "other" content-divergent changeset 3ce4be6d8e5e on 6eb54b5af3fb
  updating to "local" side of the conflict: 8ed612937375
  merging "other" content-divergent changeset 'a690ce53104a'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  merge:[13] added d
  with: [8] added d
  base: [4] added d
  rebasing "other" content-divergent changeset c72d2885eb51 on 8ed612937375
  updating to "local" side of the conflict: d45f050514c2
  merging "other" content-divergent changeset '1d1772990a3b'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory is now at 5f7a38bdb75c

  $ hg glog
  @  21:5f7a38bdb75c added d
  |   () [default] draft
  o  19:9865d598f0e0 added c
  |   () [default] draft
  o  17:ac70b8c8eb63 added b
  |   () [default] draft
  o  15:74fbf3e6a0b6 watbar to a
  |   () [default] draft
  o  9:2228e3b74514 add newfile
  |   () [default] draft
  o  0:8fa14d15e168 added hgignore
      () [default] draft
  $ cd ..

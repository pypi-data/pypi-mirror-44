+====================================================
+Tests the resolution of content divergence: metadata
+====================================================

This file intend to cover cases focused around meta data merging.

Setup
-----

  $ cat >> $HGRCPATH <<EOF
  > [alias]
  > glog = log -GT "{rev}:{node|short} {desc|firstline}\n {phase} {troubles}\n\n"
  > [phases]
  > publish = False
  > [extensions]
  > rebase =
  > EOF
  $ echo "evolve=$(echo $(dirname $TESTDIR))/hgext3rd/evolve/" >> $HGRCPATH

Check we preserve the author properly
-------------------------------------

Testing issue6113 to make sure that content-divergence resolution don't
replace initial author with the user running the resolution command:

  $ hg init userfoo
  $ cd userfoo
  $ unset HGUSER
  $ echo "[ui]" >> ./.hg/hgrc
  $ echo "username = foo <foo@test.com>" >> ./.hg/hgrc
  $ for ch in a b c; do
  > echo $ch > $ch;
  > hg add $ch;
  > hg ci -m "added "$ch;
  > done;

  $ cd ..
  $ hg init userbar
  $ cd userbar
  $ unset HGUSER
  $ echo "[ui]" >> ./.hg/hgrc
  $ echo "username = bar <bar@test.com>" >> ./.hg/hgrc
  $ hg pull ./../userfoo -q

  $ cd ../userfoo
  $ hg up -r "desc('added b')"
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo c > c
  $ echo e > e
  $ hg add c e
  $ hg ci -m "added c e"
  created new head

  $ hg up -r "desc('added b')"
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ echo cc > c
  $ hg add c
  $ hg ci -m "added c"
  created new head

  $ hg prune -r "min(desc('added c'))" -s "desc('added c e')"
  1 changesets pruned
  $ hg prune -r "min(desc('added c'))" -s "max(desc('added c'))" --hidden
  1 changesets pruned
  2 new content-divergent changesets

  $ hg glog
  @  4:6c06cda6dc99 added c
  |   draft content-divergent
  |
  | *  3:0c9267e23c9d added c e
  |/    draft content-divergent
  |
  o  1:1740ad2a1eda added b
  |   draft
  |
  o  0:f863f39764c4 added a
      draft
  

  $ cd ../userbar
  $ hg pull ./../userfoo -q
  2 new content-divergent changesets

  $ hg evolve --content-divergent --any
  merge:[3] added c e
  with: [4] added c
  base: [2] added c
  updating to "local" side of the conflict: 0c9267e23c9d
  merging "other" content-divergent changeset '6c06cda6dc99'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  working directory is now at 443bd2972210

Make sure resultant cset don't replace the initial user with user running the command:
  $ hg log -r tip
  changeset:   5:443bd2972210
  tag:         tip
  parent:      1:1740ad2a1eda
  user:        foo <foo@test.com>
  date:        Thu Jan 01 00:00:00 1970 +0000
  summary:     added c e
  

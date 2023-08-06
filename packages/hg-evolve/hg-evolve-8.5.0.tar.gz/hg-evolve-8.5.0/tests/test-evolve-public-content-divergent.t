Test for handling of content divergence with public cset using `hg evolve`
==========================================================================

Setup
=====
  $ cat >> $HGRCPATH <<EOF
  > [alias]
  > glog = log -GT "{rev}:{node|short} {desc|firstline}\n {phase} {troubles}\n\n"
  > [phases]
  > publish = False
  > [extensions]
  > rebase =
  > EOF
  $ echo "evolve=$(echo $(dirname $TESTDIR))/hgext3rd/evolve/" >> $HGRCPATH

Testing the case when both divergent cset are on the same parent and no-conflict in merging:
-------------------------------------------------------------------------------------

Prepare the repository:

  $ hg init pubdiv
  $ cd pubdiv
  $ for ch in a b; do
  >   echo $ch > $ch;
  >   hg ci -Aqm "added "$ch;
  > done;
  $ hg glog
  @  1:5f6d8a4bf34a added b
  |   draft
  |
  o  0:9092f1db7931 added a
      draft
  

Make an amend and change phase to public:

  $ sed -i "1 i I am first" b
  $ hg amend
  $ hg phase --public

Amend again to create a cset divergent to public one:

  $ hg up 1 --hidden -q
  updated to hidden changeset 5f6d8a4bf34a
  (hidden revision '5f6d8a4bf34a' was rewritten as: 44f360db368f)
  working directory parent is obsolete! (5f6d8a4bf34a)

  $ echo "I am second" >> b
  $ hg ci --amend -m "updated b"
  1 new content-divergent changesets

  $ hg glog
  @  3:dcdaf152280a updated b
  |   draft content-divergent
  |
  | o  2:44f360db368f added b
  |/    public
  |
  o  0:9092f1db7931 added a
      public
  

Lets resolve the public content-divergence:

  $ hg evolve --content-divergent
  merge:[2] added b
  with: [3] updated b
  base: [1] added b
  updating to "local" side of the conflict: 44f360db368f
  merging "other" content-divergent changeset 'dcdaf152280a'
  merging b
  0 files updated, 1 files merged, 0 files removed, 0 files unresolved
  committed as c1aa9cfb6cf8
  working directory is now at c1aa9cfb6cf8

Following graph log shows that it correctly merged the two divergent csets:

  $ hg glog -p
  @  5:c1aa9cfb6cf8 phase-divergent update to 44f360db368f:
  |   draft
  |
  |  diff -r 44f360db368f -r c1aa9cfb6cf8 b
  |  --- a/b	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/b	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -1,2 +1,3 @@
  |   I am first
  |   b
  |  +I am second
  |
  o  2:44f360db368f added b
  |   public
  |
  |  diff -r 9092f1db7931 -r 44f360db368f b
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/b	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,2 @@
  |  +I am first
  |  +b
  |
  o  0:9092f1db7931 added a
      public
  
     diff -r 000000000000 -r 9092f1db7931 a
     --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
     +++ b/a	Thu Jan 01 00:00:00 1970 +0000
     @@ -0,0 +1,1 @@
     +a
  
  $ hg evolve -l

  $ cd ..

Testing the case when both divergent cset has same parent and has conflict in merging:
------------------------------------------------------------------------------

Prepare the repository:

  $ hg init pubdiv1
  $ cd pubdiv1
  $ for ch in a b; do
  >   echo $ch > $ch;
  >   hg ci -Aqm "added "$ch;
  > done;
  $ hg glog
  @  1:5f6d8a4bf34a added b
  |   draft
  |
  o  0:9092f1db7931 added a
      draft
  

Make an amend and change phase to public:

  $ echo "I am foo" > b
  $ hg amend
  $ hg phase --public

Amend again to create a cset divergent to public one:

  $ hg up 1 --hidden -q
  updated to hidden changeset 5f6d8a4bf34a
  (hidden revision '5f6d8a4bf34a' was rewritten as: 580f2d01e52c)
  working directory parent is obsolete! (5f6d8a4bf34a)

  $ echo "I am bar" > b
  $ hg ci --amend -m "updated b"
  1 new content-divergent changesets

  $ hg glog
  @  3:0e805383168e updated b
  |   draft content-divergent
  |
  | o  2:580f2d01e52c added b
  |/    public
  |
  o  0:9092f1db7931 added a
      public
  

Lets resolve the divergence:

  $ hg evolve --content-divergent
  merge:[2] added b
  with: [3] updated b
  base: [1] added b
  updating to "local" side of the conflict: 580f2d01e52c
  merging "other" content-divergent changeset '0e805383168e'
  merging b
  warning: conflicts while merging b! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ echo "I am foobar" > b
  $ hg resolve -m --tool union
  (no more unresolved files)
  continue: hg evolve --continue
  $ hg evolve --continue
  committed as 1a739394e9d4
  working directory is now at 1a739394e9d4

  $ hg glog
  @  5:1a739394e9d4 phase-divergent update to 580f2d01e52c:
  |   draft
  |
  o  2:580f2d01e52c added b
  |   public
  |
  o  0:9092f1db7931 added a
      public
  
Testing the case when divergence is not created by actual diff change, but because of rebasing:
------------------------------------------------------------------------------------------------

Prepare the repo:

  $ cd ..
  $ hg init rebasediv
  $ cd rebasediv
  $ for ch in a b c; do
  >   echo $ch > $ch;
  >   hg ci -Am "added "$ch;
  > done;
  adding a
  adding b
  adding c

  $ hg glog
  @  2:155349b645be added c
  |   draft
  |
  o  1:5f6d8a4bf34a added b
  |   draft
  |
  o  0:9092f1db7931 added a
      draft
  

On server side: a new cset is added based on rev 1 and rev 2 is rebased on newly added cset:

  $ hg up .^ -q
  $ echo d > d
  $ hg ci -Am "added d"
  adding d
  created new head

  $ hg rebase -r 2 -d .
  rebasing 2:155349b645be "added c"

  $ hg glog
  o  4:c0d7ee6604ea added c
  |   draft
  |
  @  3:c9241b0f2d5b added d
  |   draft
  |
  o  1:5f6d8a4bf34a added b
  |   draft
  |
  o  0:9092f1db7931 added a
      draft
  

On user side: user has not pulled yet and amended the rev 2 which created the divergence after pull:
  $ hg up 2 --hidden -q
  updated to hidden changeset 155349b645be
  (hidden revision '155349b645be' was rewritten as: c0d7ee6604ea)
  working directory parent is obsolete! (155349b645be)

  $ echo cc >> c
  $ hg ci --amend -m "updated c"
  2 new content-divergent changesets

Lets change the phase to --public of branch which is pulled from server:
  $ hg phase --public -r 4
  $ hg glog -p
  @  5:f5f9b4fc8b77 updated c
  |   draft content-divergent
  |
  |  diff -r 5f6d8a4bf34a -r f5f9b4fc8b77 c
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/c	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,2 @@
  |  +c
  |  +cc
  |
  | o  4:c0d7ee6604ea added c
  | |   public
  | |
  | |  diff -r c9241b0f2d5b -r c0d7ee6604ea c
  | |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  | |  +++ b/c	Thu Jan 01 00:00:00 1970 +0000
  | |  @@ -0,0 +1,1 @@
  | |  +c
  | |
  | o  3:c9241b0f2d5b added d
  |/    public
  |
  |    diff -r 5f6d8a4bf34a -r c9241b0f2d5b d
  |    --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |    +++ b/d	Thu Jan 01 00:00:00 1970 +0000
  |    @@ -0,0 +1,1 @@
  |    +d
  |
  o  1:5f6d8a4bf34a added b
  |   public
  |
  |  diff -r 9092f1db7931 -r 5f6d8a4bf34a b
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/b	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,1 @@
  |  +b
  |
  o  0:9092f1db7931 added a
      public
  
     diff -r 000000000000 -r 9092f1db7931 a
     --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
     +++ b/a	Thu Jan 01 00:00:00 1970 +0000
     @@ -0,0 +1,1 @@
     +a
  

Evolve:
  $ hg evolve --content-divergent
  merge:[4] added c
  with: [5] updated c
  base: [2] added c
  rebasing "other" content-divergent changeset f5f9b4fc8b77 on c9241b0f2d5b
  updating to "local" side of the conflict: c0d7ee6604ea
  merging "other" content-divergent changeset 'c3d442d80993'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  committed as 3b336cbee992
  working directory is now at 3b336cbee992

  $ hg glog -p
  @  8:3b336cbee992 phase-divergent update to c0d7ee6604ea:
  |   draft
  |
  |  diff -r c0d7ee6604ea -r 3b336cbee992 c
  |  --- a/c	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/c	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -1,1 +1,2 @@
  |   c
  |  +cc
  |
  o  4:c0d7ee6604ea added c
  |   public
  |
  |  diff -r c9241b0f2d5b -r c0d7ee6604ea c
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/c	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,1 @@
  |  +c
  |
  o  3:c9241b0f2d5b added d
  |   public
  |
  |  diff -r 5f6d8a4bf34a -r c9241b0f2d5b d
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/d	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,1 @@
  |  +d
  |
  o  1:5f6d8a4bf34a added b
  |   public
  |
  |  diff -r 9092f1db7931 -r 5f6d8a4bf34a b
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/b	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,1 @@
  |  +b
  |
  o  0:9092f1db7931 added a
      public
  
     diff -r 000000000000 -r 9092f1db7931 a
     --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
     +++ b/a	Thu Jan 01 00:00:00 1970 +0000
     @@ -0,0 +1,1 @@
     +a
  
Check that we don't have any unstable cset now:
  $ hg evolve -l
  $ cd ..

Testing the case when csets are on different parent and no conflict in relocation and merging:
----------------------------------------------------------------------------------------------

  $ hg init pubdiv2
  $ cd pubdiv2
  $ for ch in a b c d; do
  >   echo $ch > $ch;
  >   hg ci -Aqm "added "$ch;
  > done;

  $ hg up .^
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo dd > d
  $ hg add d
  $ hg ci -m "added d"
  created new head

  $ hg up 1
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ echo dd > d
  $ echo e > e
  $ hg add d e
  $ hg ci -m "added d e"
  created new head

  $ hg glog
  @  5:4291d72ee19a added d e
  |   draft
  |
  | o  4:93cd84bbdaca added d
  | |   draft
  | |
  | | o  3:9150fe93bec6 added d
  | |/    draft
  | |
  | o  2:155349b645be added c
  |/    draft
  |
  o  1:5f6d8a4bf34a added b
  |   draft
  |
  o  0:9092f1db7931 added a
      draft
  

  $ hg prune 3 -s 5
  1 changesets pruned
  $ hg prune 3 -s 4 --hidden
  1 changesets pruned
  2 new content-divergent changesets

Change phase to public for one head:
  $ hg phase -r 4 --public

  $ hg glog
  @  5:4291d72ee19a added d e
  |   draft content-divergent
  |
  | o  4:93cd84bbdaca added d
  | |   public
  | |
  | o  2:155349b645be added c
  |/    public
  |
  o  1:5f6d8a4bf34a added b
  |   public
  |
  o  0:9092f1db7931 added a
      public
  

  $ hg evolve --content-divergent --any
  merge:[4] added d
  with: [5] added d e
  base: [3] added d
  rebasing "other" content-divergent changeset 4291d72ee19a on 155349b645be
  updating to "local" side of the conflict: 93cd84bbdaca
  merging "other" content-divergent changeset 'f88581407163'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  committed as 4cbe48a0c3d9
  working directory is now at 4cbe48a0c3d9

  $ hg glog -l 1
  @  8:4cbe48a0c3d9 phase-divergent update to 93cd84bbdaca:
  |   draft
  ~

  $ hg evolve -l
  $ cd ..

Different parents, relocation conflict
--------------------------------------

Testing the case when csets are on different parent and conflict in relocation
but not in merging.

  $ hg init pubdiv3
  $ cd pubdiv3
  $ for ch in a b c d; do
  >   echo $ch > $ch;
  >   hg ci -Aqm "added "$ch;
  > done;

  $ hg up .^^
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ echo d > d
  $ echo cfoo > c
  $ echo e > e
  $ hg add d c e
  $ hg ci -m "added d c e"
  created new head

  $ hg up 'desc("added c")'
  1 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ echo dd > d
  $ hg add d
  $ hg ci -m "added d"
  created new head

  $ hg glog
  @  5:93cd84bbdaca added d
  |   draft
  |
  | o  4:f31bcc378766 added d c e
  | |   draft
  | |
  +---o  3:9150fe93bec6 added d
  | |     draft
  | |
  o |  2:155349b645be added c
  |/    draft
  |
  o  1:5f6d8a4bf34a added b
  |   draft
  |
  o  0:9092f1db7931 added a
      draft
  
  $ hg prune 'min(desc("re:added d$"))' -s 'max(desc("re:added d$"))'
  1 changesets pruned
  $ hg prune 'min(desc("re:added d$"))' -s 'desc("added d c e")' --hidden
  1 changesets pruned
  2 new content-divergent changesets

Change phase to public for one head:
  $ hg phase --public -r 'max(desc("re:added d$"))'

  $ hg glog
  @  5:93cd84bbdaca added d
  |   public
  |
  | *  4:f31bcc378766 added d c e
  | |   draft content-divergent
  | |
  o |  2:155349b645be added c
  |/    public
  |
  o  1:5f6d8a4bf34a added b
  |   public
  |
  o  0:9092f1db7931 added a
      public
  
  $ hg evolve --content-divergent --any
  merge:[5] added d
  with: [4] added d c e
  base: [3] added d
  rebasing "other" content-divergent changeset f31bcc378766 on 155349b645be
  merging c
  warning: conflicts while merging c! (edit, then use 'hg resolve --mark')
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ hg diff
  diff -r 155349b645be c
  --- a/c	Thu Jan 01 00:00:00 1970 +0000
  +++ b/c	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,5 @@
  +<<<<<<< destination: 155349b645be - test: added c
   c
  +=======
  +cfoo
  +>>>>>>> evolving:    f31bcc378766 - test: added d c e
  diff -r 155349b645be d
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/d	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +d
  diff -r 155349b645be e
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/e	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +e

  $ echo c > c
  $ hg res -m
  (no more unresolved files)
  continue: hg evolve --continue

  $ hg evolve --continue
  evolving 4:f31bcc378766 "added d c e"
  updating to "local" side of the conflict: 93cd84bbdaca
  merging "other" content-divergent changeset 'bd28d3e4a228'
  1 files updated, 0 files merged, 0 files removed, 0 files unresolved
  committed as 412dde898967
  working directory is now at 412dde898967
  $ hg export
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID 412dde898967b50e7d334aefff778a9af46d29d1
  # Parent  93cd84bbdacaeb8f881c29a609dbdd30c38cbc57
  phase-divergent update to 93cd84bbdaca:
  
  added d c e
  
  diff -r 93cd84bbdaca -r 412dde898967 e
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/e	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +e

  $ hg evolve -l
  $ cd ..

Testing the case when merging leads to conflicts but relocation won't:
---------------------------------------------------------------------

  $ hg init pubdiv3.5
  $ cd pubdiv3.5
  $ for ch in a b c d; do
  >   echo $ch > $ch;
  >   hg ci -Aqm "added "$ch;
  > done;

  $ hg up .^^
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ echo dconflict > d
  $ hg add d
  $ hg ci -m "added d"
  created new head

  $ hg up 2
  1 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo dd > d
  $ hg add d
  $ hg ci -m "added d"
  created new head

  $ hg glog
  @  5:93cd84bbdaca added d
  |   draft
  |
  | o  4:9411ad1fe615 added d
  | |   draft
  | |
  +---o  3:9150fe93bec6 added d
  | |     draft
  | |
  o |  2:155349b645be added c
  |/    draft
  |
  o  1:5f6d8a4bf34a added b
  |   draft
  |
  o  0:9092f1db7931 added a
      draft
  
  $ hg prune 3 -s 5
  1 changesets pruned
  $ hg prune 3 -s 4 --hidden
  1 changesets pruned
  2 new content-divergent changesets

Change phase to public for one head:
  $ hg phase --public -r 5

  $ hg glog
  @  5:93cd84bbdaca added d
  |   public
  |
  | *  4:9411ad1fe615 added d
  | |   draft content-divergent
  | |
  o |  2:155349b645be added c
  |/    public
  |
  o  1:5f6d8a4bf34a added b
  |   public
  |
  o  0:9092f1db7931 added a
      public
  
  $ hg evolve --content-divergent --any
  merge:[5] added d
  with: [4] added d
  base: [3] added d
  rebasing "other" content-divergent changeset 9411ad1fe615 on 155349b645be
  updating to "local" side of the conflict: 93cd84bbdaca
  merging "other" content-divergent changeset 'b5c690cdf1d5'
  merging d
  warning: conflicts while merging d! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ echo d > d
  $ hg res -m
  (no more unresolved files)
  continue: hg evolve --continue

  $ hg evolve --continue
  committed as 2a0f44767904
  working directory is now at 2a0f44767904

  $ hg evolve -l
  $ cd ..

Testing the case when relocation and merging both leads to conflicts:
--------------------------------------------------------------------

  $ hg init pubdiv4
  $ cd pubdiv4
  $ for ch in a b c d; do
  >   echo $ch > $ch;
  >   hg ci -Aqm "added "$ch;
  > done;

  $ hg up .^^
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ echo cfoo > c
  $ echo e > e
  $ echo dconflict > d
  $ hg add c e d
  $ hg ci -m "added c e"
  created new head

  $ hg up 2
  1 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ echo dd > d
  $ hg add d
  $ hg ci -m "added d"
  created new head

  $ hg glog
  @  5:93cd84bbdaca added d
  |   draft
  |
  | o  4:3c17c7afaf6e added c e
  | |   draft
  | |
  +---o  3:9150fe93bec6 added d
  | |     draft
  | |
  o |  2:155349b645be added c
  |/    draft
  |
  o  1:5f6d8a4bf34a added b
  |   draft
  |
  o  0:9092f1db7931 added a
      draft
  
  $ hg prune 3 -s 5
  1 changesets pruned
  $ hg prune 3 -s 4 --hidden
  1 changesets pruned
  2 new content-divergent changesets

Change phase to public for one head:
  $ hg phase --public -r 5

  $ hg glog
  @  5:93cd84bbdaca added d
  |   public
  |
  | *  4:3c17c7afaf6e added c e
  | |   draft content-divergent
  | |
  o |  2:155349b645be added c
  |/    public
  |
  o  1:5f6d8a4bf34a added b
  |   public
  |
  o  0:9092f1db7931 added a
      public
  
  $ hg evolve --content-divergent --any
  merge:[5] added d
  with: [4] added c e
  base: [3] added d
  rebasing "other" content-divergent changeset 3c17c7afaf6e on 155349b645be
  merging c
  warning: conflicts while merging c! (edit, then use 'hg resolve --mark')
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ hg diff
  diff -r 155349b645be c
  --- a/c	Thu Jan 01 00:00:00 1970 +0000
  +++ b/c	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,5 @@
  +<<<<<<< destination: 155349b645be - test: added c
   c
  +=======
  +cfoo
  +>>>>>>> evolving:    3c17c7afaf6e - test: added c e
  diff -r 155349b645be d
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/d	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +dconflict
  diff -r 155349b645be e
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/e	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +e

  $ echo cfoo > c
  $ hg res -m
  (no more unresolved files)
  continue: hg evolve --continue

  $ hg evolve --continue
  evolving 4:3c17c7afaf6e "added c e"
  updating to "local" side of the conflict: 93cd84bbdaca
  merging "other" content-divergent changeset 'c4ce3d34e784'
  merging d
  warning: conflicts while merging d! (edit, then use 'hg resolve --mark')
  2 files updated, 0 files merged, 0 files removed, 1 files unresolved
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ echo d > d
  $ hg res -m
  (no more unresolved files)
  continue: hg evolve --continue

  $ hg evolve --continue
  committed as b9082a9e66ce
  working directory is now at b9082a9e66ce

  $ hg evolve -l
  $ cd ..

Different parent, simple conflict on relocate, deleted file on actual merge
---------------------------------------------------------------------------

Changeset "added c e" is also removing 'd'. This should conflict with the update
to 'd' in the successors of 'adding d' when solving the content divergence.

  $ hg init pubdiv-parent-deleted-file
  $ cd pubdiv-parent-deleted-file
  $ for ch in a b c d; do
  >   echo $ch > $ch;
  >   hg ci -Aqm "added "$ch;
  > done;

  $ hg up 'desc("added b")'
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ echo cfoo > c
  $ echo e > e
  $ hg add c e
  $ hg ci -m "added c e"
  created new head

  $ hg up 'desc("re:added c$")'
  1 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo dd > d
  $ hg add d
  $ hg ci -m "added d"
  created new head

  $ hg glog --patch --rev 'sort(all(), "topo")'
  @  5:93cd84bbdaca added d
  |   draft
  |
  |  diff -r 155349b645be -r 93cd84bbdaca d
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/d	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,1 @@
  |  +dd
  |
  | o  3:9150fe93bec6 added d
  |/    draft
  |
  |    diff -r 155349b645be -r 9150fe93bec6 d
  |    --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |    +++ b/d	Thu Jan 01 00:00:00 1970 +0000
  |    @@ -0,0 +1,1 @@
  |    +d
  |
  o  2:155349b645be added c
  |   draft
  |
  |  diff -r 5f6d8a4bf34a -r 155349b645be c
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/c	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,1 @@
  |  +c
  |
  | o  4:e568fd1029bb added c e
  |/    draft
  |
  |    diff -r 5f6d8a4bf34a -r e568fd1029bb c
  |    --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |    +++ b/c	Thu Jan 01 00:00:00 1970 +0000
  |    @@ -0,0 +1,1 @@
  |    +cfoo
  |    diff -r 5f6d8a4bf34a -r e568fd1029bb e
  |    --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |    +++ b/e	Thu Jan 01 00:00:00 1970 +0000
  |    @@ -0,0 +1,1 @@
  |    +e
  |
  o  1:5f6d8a4bf34a added b
  |   draft
  |
  |  diff -r 9092f1db7931 -r 5f6d8a4bf34a b
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/b	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,1 @@
  |  +b
  |
  o  0:9092f1db7931 added a
      draft
  
     diff -r 000000000000 -r 9092f1db7931 a
     --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
     +++ b/a	Thu Jan 01 00:00:00 1970 +0000
     @@ -0,0 +1,1 @@
     +a
  
  $ hg prune 'min(desc("added d"))' -s 'max(desc("added d"))'
  1 changesets pruned
  $ hg prune 'min(desc("added d"))' -s 'desc("added c e")' --hidden
  1 changesets pruned
  2 new content-divergent changesets

Change phase to public for one head:
  $ hg phase --public -r 'max(desc("added d"))'

  $ hg glog
  @  5:93cd84bbdaca added d
  |   public
  |
  | *  4:e568fd1029bb added c e
  | |   draft content-divergent
  | |
  o |  2:155349b645be added c
  |/    public
  |
  o  1:5f6d8a4bf34a added b
  |   public
  |
  o  0:9092f1db7931 added a
      public
  

  $ hg glog --patch --rev 'sort(all(), "topo")' --hidden
  @  5:93cd84bbdaca added d
  |   public
  |
  |  diff -r 155349b645be -r 93cd84bbdaca d
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/d	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,1 @@
  |  +dd
  |
  | x  3:9150fe93bec6 added d
  |/    draft
  |
  |    diff -r 155349b645be -r 9150fe93bec6 d
  |    --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |    +++ b/d	Thu Jan 01 00:00:00 1970 +0000
  |    @@ -0,0 +1,1 @@
  |    +d
  |
  o  2:155349b645be added c
  |   public
  |
  |  diff -r 5f6d8a4bf34a -r 155349b645be c
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/c	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,1 @@
  |  +c
  |
  | *  4:e568fd1029bb added c e
  |/    draft content-divergent
  |
  |    diff -r 5f6d8a4bf34a -r e568fd1029bb c
  |    --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |    +++ b/c	Thu Jan 01 00:00:00 1970 +0000
  |    @@ -0,0 +1,1 @@
  |    +cfoo
  |    diff -r 5f6d8a4bf34a -r e568fd1029bb e
  |    --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |    +++ b/e	Thu Jan 01 00:00:00 1970 +0000
  |    @@ -0,0 +1,1 @@
  |    +e
  |
  o  1:5f6d8a4bf34a added b
  |   public
  |
  |  diff -r 9092f1db7931 -r 5f6d8a4bf34a b
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/b	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,1 @@
  |  +b
  |
  o  0:9092f1db7931 added a
      public
  
     diff -r 000000000000 -r 9092f1db7931 a
     --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
     +++ b/a	Thu Jan 01 00:00:00 1970 +0000
     @@ -0,0 +1,1 @@
     +a
  

  $ hg obslog --all --rev tip --patch
  @  93cd84bbdaca (5) added d
  |
  | *  e568fd1029bb (4) added c e
  |/
  x  9150fe93bec6 (3) added d
       rewritten(content) as 93cd84bbdaca using prune by test (Thu Jan 01 00:00:00 1970 +0000)
         diff -r 9150fe93bec6 -r 93cd84bbdaca d
         --- a/d	Thu Jan 01 00:00:00 1970 +0000
         +++ b/d	Thu Jan 01 00:00:00 1970 +0000
         @@ -1,1 +1,1 @@
         -d
         +dd
  
       rewritten(description, parent, content) as e568fd1029bb using prune by test (Thu Jan 01 00:00:00 1970 +0000)
         (No patch available, changesets rebased)
  

  $ hg evolve --content-divergent --any
  merge:[5] added d
  with: [4] added c e
  base: [3] added d
  rebasing "other" content-divergent changeset e568fd1029bb on 155349b645be
  merging c
  warning: conflicts while merging c! (edit, then use 'hg resolve --mark')
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ hg diff
  diff -r 155349b645be c
  --- a/c	Thu Jan 01 00:00:00 1970 +0000
  +++ b/c	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,5 @@
  +<<<<<<< destination: 155349b645be - test: added c
   c
  +=======
  +cfoo
  +>>>>>>> evolving:    e568fd1029bb - test: added c e
  diff -r 155349b645be e
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/e	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +e

  $ echo c > c
  $ hg res -m
  (no more unresolved files)
  continue: hg evolve --continue

  $ hg evolve --continue
  evolving 4:e568fd1029bb "added c e"
  updating to "local" side of the conflict: 93cd84bbdaca
  merging "other" content-divergent changeset '2af3359250d3'
  file 'd' was deleted in other but was modified in local.
  What do you want to do?
  use (c)hanged version, (d)elete, or leave (u)nresolved? u
  1 files updated, 0 files merged, 0 files removed, 1 files unresolved
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ hg sum
  parent: 5:93cd84bbdaca 
   added d
  parent: 6:2af3359250d3 tip (content-divergent)
   added c e
  branch: default
  commit: 1 modified, 1 unknown, 1 unresolved (merge)
  update: (current)
  phases: 1 draft
  content-divergent: 1 changesets
  evolve: (evolve --continue)

  $ echo resolved > d
  $ hg resolve -m d
  (no more unresolved files)
  continue: hg evolve --continue

  $ hg evolve --continue
  committed as bc1f4610744c
  working directory is now at bc1f4610744c

  $ hg export
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID bc1f4610744c6aa0e851d3876a61bfff6243b31c
  # Parent  93cd84bbdacaeb8f881c29a609dbdd30c38cbc57
  phase-divergent update to 93cd84bbdaca:
  
  added c e
  
  diff -r 93cd84bbdaca -r bc1f4610744c d
  --- a/d	Thu Jan 01 00:00:00 1970 +0000
  +++ b/d	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,1 @@
  -dd
  +resolved
  diff -r 93cd84bbdaca -r bc1f4610744c e
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/e	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +e

  $ hg evolve -l
  $ cd ..

Testing the case when "merging results in same as public cset" where:
both the csets are on same parent and no conflict in merging.
---------------------------------------------------------------------

Prepare the repo:

  $ hg init pubdiv5
  $ cd pubdiv5
  $ for ch in a b c; do
  >   echo $ch > $ch;
  >   hg ci -Am "added "$ch;
  > done;
  adding a
  adding b
  adding c

  $ hg up .^
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo ch > ch
  $ hg add ch
  $ hg ci -m "added ch"
  created new head

  $ hg up .^
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo ch > ch
  $ hg add ch
  $ hg ci -m "added c"
  created new head

  $ hg glog
  @  4:f7c1071f1e7c added c
  |   draft
  |
  | o  3:90522bccf499 added ch
  |/    draft
  |
  | o  2:155349b645be added c
  |/    draft
  |
  o  1:5f6d8a4bf34a added b
  |   draft
  |
  o  0:9092f1db7931 added a
      draft
  

  $ hg prune 2 -s 3
  1 changesets pruned
  $ hg prune 2 -s 4 --hidden
  1 changesets pruned
  2 new content-divergent changesets
  $ hg phase --public -r 4

  $ hg glog
  @  4:f7c1071f1e7c added c
  |   public
  |
  | *  3:90522bccf499 added ch
  |/    draft content-divergent
  |
  o  1:5f6d8a4bf34a added b
  |   public
  |
  o  0:9092f1db7931 added a
      public
  
  $ hg evolve --content-divergent --any
  merge:[4] added c
  with: [3] added ch
  base: [2] added c
  merging "other" content-divergent changeset '90522bccf499'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  content-divergent changesets differ by descriptions only, discarding 90522bccf499

  $ hg evolve -l

  $ hg par
  changeset:   4:f7c1071f1e7c
  tag:         tip
  parent:      1:5f6d8a4bf34a
  user:        test
  date:        Thu Jan 01 00:00:00 1970 +0000
  summary:     added c
  

Testing the case when "merging results in same as public cset" where:
both the csets are on different parent and no conflict in merging and relocation.
---------------------------------------------------------------------------------

Prepare the repo:

  $ cd ..
  $ hg init pubdiv6
  $ cd pubdiv6
  $ for ch in a b c d; do
  >   echo $ch > $ch;
  >   hg ci -Am "added "$ch;
  > done;
  adding a
  adding b
  adding c
  adding d

  $ hg up 1
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ echo dh > dh
  $ hg add dh
  $ hg ci -m "added dh"
  created new head

  $ hg up 2
  1 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo dh > dh
  $ hg add dh
  $ hg ci -m "added d"
  created new head

  $ hg glog
  @  5:e800202333a4 added d
  |   draft
  |
  | o  4:5acd58ef5066 added dh
  | |   draft
  | |
  +---o  3:9150fe93bec6 added d
  | |     draft
  | |
  o |  2:155349b645be added c
  |/    draft
  |
  o  1:5f6d8a4bf34a added b
  |   draft
  |
  o  0:9092f1db7931 added a
      draft
  

  $ hg prune 3 -s 4
  1 changesets pruned
  $ hg prune 3 -s 5 --hidden
  1 changesets pruned
  2 new content-divergent changesets
  $ hg phase --public -r 5

  $ hg glog
  @  5:e800202333a4 added d
  |   public
  |
  | *  4:5acd58ef5066 added dh
  | |   draft content-divergent
  | |
  o |  2:155349b645be added c
  |/    public
  |
  o  1:5f6d8a4bf34a added b
  |   public
  |
  o  0:9092f1db7931 added a
      public
  
  $ hg evolve --content-divergent --any
  merge:[5] added d
  with: [4] added dh
  base: [3] added d
  rebasing "other" content-divergent changeset 5acd58ef5066 on 155349b645be
  updating to "local" side of the conflict: e800202333a4
  merging "other" content-divergent changeset 'ae3429430ef1'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  content-divergent changesets differ by descriptions only, discarding ae3429430ef1

  $ hg evolve -l

  $ hg par
  changeset:   5:e800202333a4
  tag:         tip
  parent:      2:155349b645be
  user:        test
  date:        Thu Jan 01 00:00:00 1970 +0000
  summary:     added d
  
Testing the case when "merging results in same as public cset" where:
both the csets are on same parent and merging leads to conflict.
---------------------------------------------------------------------

Prepare the repo:

  $ cd ..
  $ hg init pubdiv7
  $ cd pubdiv7
  $ for ch in a b c; do
  >   echo $ch > $ch;
  >   hg ci -Am "added "$ch;
  > done;
  adding a
  adding b
  adding c

  $ hg up .^
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo chconflict > ch
  $ hg add ch
  $ hg ci -m "added ch"
  created new head

  $ hg up .^
  0 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo ch > ch
  $ hg add ch
  $ hg ci -m "added c"
  created new head

  $ hg glog
  @  4:f7c1071f1e7c added c
  |   draft
  |
  | o  3:229da2719b19 added ch
  |/    draft
  |
  | o  2:155349b645be added c
  |/    draft
  |
  o  1:5f6d8a4bf34a added b
  |   draft
  |
  o  0:9092f1db7931 added a
      draft
  

  $ hg prune 2 -s 3
  1 changesets pruned
  $ hg prune 2 -s 4 --hidden
  1 changesets pruned
  2 new content-divergent changesets
  $ hg phase --public -r 4

  $ hg glog
  @  4:f7c1071f1e7c added c
  |   public
  |
  | *  3:229da2719b19 added ch
  |/    draft content-divergent
  |
  o  1:5f6d8a4bf34a added b
  |   public
  |
  o  0:9092f1db7931 added a
      public
  
  $ hg evolve --content-divergent --any
  merge:[4] added c
  with: [3] added ch
  base: [2] added c
  merging "other" content-divergent changeset '229da2719b19'
  merging ch
  warning: conflicts while merging ch! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ hg diff
  diff -r f7c1071f1e7c ch
  --- a/ch	Thu Jan 01 00:00:00 1970 +0000
  +++ b/ch	Thu Jan 01 00:00:00 1970 +0000
  @@ -1,1 +1,5 @@
  +<<<<<<< local: f7c1071f1e7c - test: added c
   ch
  +=======
  +chconflict
  +>>>>>>> other: 229da2719b19 - test: added ch

  $ echo ch > ch
  $ hg res -m
  (no more unresolved files)
  continue: hg evolve --continue

  $ hg evolve --continue
  content-divergent changesets differ by descriptions only, discarding 229da2719b19
  working directory is now at f7c1071f1e7c

  $ hg evolve -l

  $ hg par
  changeset:   4:f7c1071f1e7c
  tag:         tip
  parent:      1:5f6d8a4bf34a
  user:        test
  date:        Thu Jan 01 00:00:00 1970 +0000
  summary:     added c
  
Testing the case when "merging results in same as public cset" where:
both the csets are on different parent and relocation leads to conflict but merging won't.
------------------------------------------------------------------------------------------
Prepare the repo:

  $ cd ..
  $ hg init pubdiv8
  $ cd pubdiv8
  $ for ch in a b c d; do
  >   echo $ch > $ch;
  >   hg ci -Am "added "$ch;
  > done;
  adding a
  adding b
  adding c
  adding d

  $ hg up 1
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ echo dh > dh
  $ echo cc > c
  $ hg add dh c
  $ hg ci -m "added dh"
  created new head

  $ hg up 2
  1 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo dh > dh
  $ hg add dh
  $ hg ci -m "added d"
  created new head

  $ hg glog
  @  5:e800202333a4 added d
  |   draft
  |
  | o  4:f89a8e2f86ac added dh
  | |   draft
  | |
  +---o  3:9150fe93bec6 added d
  | |     draft
  | |
  o |  2:155349b645be added c
  |/    draft
  |
  o  1:5f6d8a4bf34a added b
  |   draft
  |
  o  0:9092f1db7931 added a
      draft
  

  $ hg prune 3 -s 4
  1 changesets pruned
  $ hg prune 3 -s 5 --hidden
  1 changesets pruned
  2 new content-divergent changesets
  $ hg phase --public -r 5

  $ hg glog
  @  5:e800202333a4 added d
  |   public
  |
  | *  4:f89a8e2f86ac added dh
  | |   draft content-divergent
  | |
  o |  2:155349b645be added c
  |/    public
  |
  o  1:5f6d8a4bf34a added b
  |   public
  |
  o  0:9092f1db7931 added a
      public
  
  $ hg evolve --content-divergent --any
  merge:[5] added d
  with: [4] added dh
  base: [3] added d
  rebasing "other" content-divergent changeset f89a8e2f86ac on 155349b645be
  merging c
  warning: conflicts while merging c! (edit, then use 'hg resolve --mark')
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ echo c > c
  $ hg res -m
  (no more unresolved files)
  continue: hg evolve --continue

  $ hg evolve --continue
  evolving 4:f89a8e2f86ac "added dh"
  updating to "local" side of the conflict: e800202333a4
  merging "other" content-divergent changeset 'bc309da55b88'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  content-divergent changesets differ by descriptions only, discarding bc309da55b88
  working directory is now at e800202333a4

  $ hg evolve -l

  $ hg par
  changeset:   5:e800202333a4
  tag:         tip
  parent:      2:155349b645be
  user:        test
  date:        Thu Jan 01 00:00:00 1970 +0000
  summary:     added d
  
Testing the case when "merging results in same as public cset" where:
both the csets are on different parent and merging leads to conflict but relocation won't.
------------------------------------------------------------------------------------------
Prepare the repo:

  $ cd ..
  $ hg init pubdiv9
  $ cd pubdiv9
  $ for ch in a b c d; do
  >   echo $ch > $ch;
  >   hg ci -Am "added "$ch;
  > done;
  adding a
  adding b
  adding c
  adding d

  $ hg up 1
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ echo dhconflict > dh
  $ hg add dh
  $ hg ci -m "added dh"
  created new head

  $ hg up 2
  1 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo dh > dh
  $ hg add dh
  $ hg ci -m "added d"
  created new head

  $ hg glog
  @  5:e800202333a4 added d
  |   draft
  |
  | o  4:db0b7bba0aae added dh
  | |   draft
  | |
  +---o  3:9150fe93bec6 added d
  | |     draft
  | |
  o |  2:155349b645be added c
  |/    draft
  |
  o  1:5f6d8a4bf34a added b
  |   draft
  |
  o  0:9092f1db7931 added a
      draft
  

  $ hg prune 3 -s 4
  1 changesets pruned
  $ hg prune 3 -s 5 --hidden
  1 changesets pruned
  2 new content-divergent changesets
  $ hg phase --public -r 5

  $ hg glog
  @  5:e800202333a4 added d
  |   public
  |
  | *  4:db0b7bba0aae added dh
  | |   draft content-divergent
  | |
  o |  2:155349b645be added c
  |/    public
  |
  o  1:5f6d8a4bf34a added b
  |   public
  |
  o  0:9092f1db7931 added a
      public
  
  $ hg evolve --content-divergent --any
  merge:[5] added d
  with: [4] added dh
  base: [3] added d
  rebasing "other" content-divergent changeset db0b7bba0aae on 155349b645be
  updating to "local" side of the conflict: e800202333a4
  merging "other" content-divergent changeset 'a5bbf2042450'
  merging dh
  warning: conflicts while merging dh! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ echo dh > dh
  $ hg res -m
  (no more unresolved files)
  continue: hg evolve --continue

  $ hg evolve --continue
  content-divergent changesets differ by descriptions only, discarding a5bbf2042450
  working directory is now at e800202333a4

  $ hg evolve -l

  $ hg par
  changeset:   5:e800202333a4
  tag:         tip
  parent:      2:155349b645be
  user:        test
  date:        Thu Jan 01 00:00:00 1970 +0000
  summary:     added d
  

Testing the case when "merging results in same as public cset" where:
both the csets are on different parent and relocation and merging both leads to conflict:
-----------------------------------------------------------------------------------------
Prepare the repo:

  $ cd ..
  $ hg init pubdiv10
  $ cd pubdiv10
  $ for ch in a b c d; do
  >   echo $ch > $ch;
  >   hg ci -Am "added "$ch;
  > done;
  adding a
  adding b
  adding c
  adding d

  $ hg up 1
  0 files updated, 0 files merged, 2 files removed, 0 files unresolved
  $ echo dhconflict > dh
  $ echo cc > c
  $ hg add dh c
  $ hg ci -m "added dh"
  created new head

  $ hg up 2
  1 files updated, 0 files merged, 1 files removed, 0 files unresolved
  $ echo dh > dh
  $ hg add dh
  $ hg ci -m "added d"
  created new head

  $ hg glog
  @  5:e800202333a4 added d
  |   draft
  |
  | o  4:67b19bbd770f added dh
  | |   draft
  | |
  +---o  3:9150fe93bec6 added d
  | |     draft
  | |
  o |  2:155349b645be added c
  |/    draft
  |
  o  1:5f6d8a4bf34a added b
  |   draft
  |
  o  0:9092f1db7931 added a
      draft
  

  $ hg prune 3 -s 4
  1 changesets pruned
  $ hg prune 3 -s 5 --hidden
  1 changesets pruned
  2 new content-divergent changesets
  $ hg phase --public -r 5

  $ hg glog
  @  5:e800202333a4 added d
  |   public
  |
  | *  4:67b19bbd770f added dh
  | |   draft content-divergent
  | |
  o |  2:155349b645be added c
  |/    public
  |
  o  1:5f6d8a4bf34a added b
  |   public
  |
  o  0:9092f1db7931 added a
      public
  
  $ hg evolve --content-divergent --any
  merge:[5] added d
  with: [4] added dh
  base: [3] added d
  rebasing "other" content-divergent changeset 67b19bbd770f on 155349b645be
  merging c
  warning: conflicts while merging c! (edit, then use 'hg resolve --mark')
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ echo c > c
  $ hg res -m
  (no more unresolved files)
  continue: hg evolve --continue

  $ hg evolve --continue
  evolving 4:67b19bbd770f "added dh"
  updating to "local" side of the conflict: e800202333a4
  merging "other" content-divergent changeset '09054d1f3c97'
  merging dh
  warning: conflicts while merging dh! (edit, then use 'hg resolve --mark')
  0 files updated, 0 files merged, 0 files removed, 1 files unresolved
  fix conflicts and see `hg help evolve.interrupted`
  [1]

  $ echo dh > dh
  $ hg res -m
  (no more unresolved files)
  continue: hg evolve --continue

  $ hg evolve --continue
  content-divergent changesets differ by descriptions only, discarding 09054d1f3c97
  working directory is now at e800202333a4

  $ hg evolve -l

  $ hg par
  changeset:   5:e800202333a4
  tag:         tip
  parent:      2:155349b645be
  user:        test
  date:        Thu Jan 01 00:00:00 1970 +0000
  summary:     added d
  

  $ cd ..

Test a pratical "rebase" case
=============================

Initial setup

  $ hg init rebase-divergence
  $ cd rebase-divergence
  $ echo root >> root
  $ hg add root
  $ hg commit -m root
  $ for x in c_A c_B c_C c_D; do
  >     echo $x >> $x
  >     hg add $x
  >     hg commit -m $x
  > done

  $ hg up 'desc("c_A")'
  0 files updated, 0 files merged, 3 files removed, 0 files unresolved

  $ for x in c_E c_F; do
  >     echo $x >> $x
  >     hg add $x
  >     hg commit -m $x
  > done
  created new head

(creating divergence locally for simplicity)

  $ node=`hg log --rev 'desc("c_E")' -T '{node}'`
  $ hg rebase -s $node -d 'desc("c_B")'
  rebasing 5:4ab2719bbab9 "c_E"
  rebasing 6:77ccbf8d837e "c_F" (tip)
  $ hg phase --public tip
  $ hg rebase --hidden -s $node -d 'desc("c_C")' --config experimental.evolution.allowdivergence=yes
  rebasing 5:4ab2719bbab9 "c_E"
  rebasing 6:77ccbf8d837e "c_F"
  2 new content-divergent changesets

  $ hg sum
  parent: 8:a52ac76b45f5 
   c_F
  branch: default
  commit: (clean)
  update: 4 new changesets, 3 branch heads (merge)
  phases: 4 draft
  content-divergent: 2 changesets
  $ hg evolve --list
  b4a584aea4bd: c_E
    content-divergent: c7d2d47c7240 (public) (precursor 4ab2719bbab9)
  
  8ae8db670b4a: c_F
    content-divergent: a52ac76b45f5 (public) (precursor 77ccbf8d837e)
  
  $ hg log -G --patch
  *  changeset:   10:8ae8db670b4a
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  instability: content-divergent
  |  summary:     c_F
  |
  |  diff -r b4a584aea4bd -r 8ae8db670b4a c_F
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/c_F	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,1 @@
  |  +c_F
  |
  *  changeset:   9:b4a584aea4bd
  |  parent:      3:abb77b893f28
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  instability: content-divergent
  |  summary:     c_E
  |
  |  diff -r abb77b893f28 -r b4a584aea4bd c_E
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/c_E	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,1 @@
  |  +c_E
  |
  | @  changeset:   8:a52ac76b45f5
  | |  user:        test
  | |  date:        Thu Jan 01 00:00:00 1970 +0000
  | |  summary:     c_F
  | |
  | |  diff -r c7d2d47c7240 -r a52ac76b45f5 c_F
  | |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  | |  +++ b/c_F	Thu Jan 01 00:00:00 1970 +0000
  | |  @@ -0,0 +1,1 @@
  | |  +c_F
  | |
  | o  changeset:   7:c7d2d47c7240
  | |  parent:      2:eb1b4e1205b8
  | |  user:        test
  | |  date:        Thu Jan 01 00:00:00 1970 +0000
  | |  summary:     c_E
  | |
  | |  diff -r eb1b4e1205b8 -r c7d2d47c7240 c_E
  | |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  | |  +++ b/c_E	Thu Jan 01 00:00:00 1970 +0000
  | |  @@ -0,0 +1,1 @@
  | |  +c_E
  | |
  +---o  changeset:   4:dbb960d6c97c
  | |    user:        test
  | |    date:        Thu Jan 01 00:00:00 1970 +0000
  | |    summary:     c_D
  | |
  | |    diff -r abb77b893f28 -r dbb960d6c97c c_D
  | |    --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  | |    +++ b/c_D	Thu Jan 01 00:00:00 1970 +0000
  | |    @@ -0,0 +1,1 @@
  | |    +c_D
  | |
  o |  changeset:   3:abb77b893f28
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    summary:     c_C
  |
  |    diff -r eb1b4e1205b8 -r abb77b893f28 c_C
  |    --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |    +++ b/c_C	Thu Jan 01 00:00:00 1970 +0000
  |    @@ -0,0 +1,1 @@
  |    +c_C
  |
  o  changeset:   2:eb1b4e1205b8
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B
  |
  |  diff -r e31751786014 -r eb1b4e1205b8 c_B
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/c_B	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,1 @@
  |  +c_B
  |
  o  changeset:   1:e31751786014
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A
  |
  |  diff -r 1e4be0697311 -r e31751786014 c_A
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/c_A	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,1 @@
  |  +c_A
  |
  o  changeset:   0:1e4be0697311
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     root
  
     diff -r 000000000000 -r 1e4be0697311 root
     --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
     +++ b/root	Thu Jan 01 00:00:00 1970 +0000
     @@ -0,0 +1,1 @@
     +root
  

Run automatic evolution

  $ hg evolve --content-divergent --rev 'not public() and desc("c_E")::'
  merge:[7] c_E
  with: [9] c_E
  base: [5] c_E
  rebasing "other" content-divergent changeset b4a584aea4bd on eb1b4e1205b8
  updating to "local" side of the conflict: c7d2d47c7240
  merging "other" content-divergent changeset '0773642cfa95'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  1 new orphan changesets
  merge:[8] c_F
  with: [10] c_F
  base: [6] c_F
  rebasing "other" content-divergent changeset 8ae8db670b4a on c7d2d47c7240
  updating to "local" side of the conflict: a52ac76b45f5
  merging "other" content-divergent changeset '6a87ed4aa317'
  0 files updated, 0 files merged, 0 files removed, 0 files unresolved
  $ hg sum
  parent: 8:a52ac76b45f5 tip
   c_F
  branch: default
  commit: (clean)
  update: 2 new changesets, 2 branch heads (merge)
  phases: 2 draft

  $ hg evolve --list

  $ hg log -G --patch
  @  changeset:   8:a52ac76b45f5
  |  tag:         tip
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_F
  |
  |  diff -r c7d2d47c7240 -r a52ac76b45f5 c_F
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/c_F	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,1 @@
  |  +c_F
  |
  o  changeset:   7:c7d2d47c7240
  |  parent:      2:eb1b4e1205b8
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_E
  |
  |  diff -r eb1b4e1205b8 -r c7d2d47c7240 c_E
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/c_E	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,1 @@
  |  +c_E
  |
  | o  changeset:   4:dbb960d6c97c
  | |  user:        test
  | |  date:        Thu Jan 01 00:00:00 1970 +0000
  | |  summary:     c_D
  | |
  | |  diff -r abb77b893f28 -r dbb960d6c97c c_D
  | |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  | |  +++ b/c_D	Thu Jan 01 00:00:00 1970 +0000
  | |  @@ -0,0 +1,1 @@
  | |  +c_D
  | |
  | o  changeset:   3:abb77b893f28
  |/   user:        test
  |    date:        Thu Jan 01 00:00:00 1970 +0000
  |    summary:     c_C
  |
  |    diff -r eb1b4e1205b8 -r abb77b893f28 c_C
  |    --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |    +++ b/c_C	Thu Jan 01 00:00:00 1970 +0000
  |    @@ -0,0 +1,1 @@
  |    +c_C
  |
  o  changeset:   2:eb1b4e1205b8
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_B
  |
  |  diff -r e31751786014 -r eb1b4e1205b8 c_B
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/c_B	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,1 @@
  |  +c_B
  |
  o  changeset:   1:e31751786014
  |  user:        test
  |  date:        Thu Jan 01 00:00:00 1970 +0000
  |  summary:     c_A
  |
  |  diff -r 1e4be0697311 -r e31751786014 c_A
  |  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  |  +++ b/c_A	Thu Jan 01 00:00:00 1970 +0000
  |  @@ -0,0 +1,1 @@
  |  +c_A
  |
  o  changeset:   0:1e4be0697311
     user:        test
     date:        Thu Jan 01 00:00:00 1970 +0000
     summary:     root
  
     diff -r 000000000000 -r 1e4be0697311 root
     --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
     +++ b/root	Thu Jan 01 00:00:00 1970 +0000
     @@ -0,0 +1,1 @@
     +root
  
  $ hg export tip
  # HG changeset patch
  # User test
  # Date 0 0
  #      Thu Jan 01 00:00:00 1970 +0000
  # Node ID a52ac76b45f523a039fc4a938d79874f4bdb1a85
  # Parent  c7d2d47c7240562be5cbd1a24080dd0396178709
  c_F
  
  diff -r c7d2d47c7240 -r a52ac76b45f5 c_F
  --- /dev/null	Thu Jan 01 00:00:00 1970 +0000
  +++ b/c_F	Thu Jan 01 00:00:00 1970 +0000
  @@ -0,0 +1,1 @@
  +c_F

  $ hg obslog --rev a52ac76b45f5
  @    a52ac76b45f5 (8) c_F
  |\
  x |  6a87ed4aa317 (12) c_F
  | |    rewritten as a52ac76b45f5 using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  | |
  x |  8ae8db670b4a (10) c_F
  |/     rewritten(parent) as 6a87ed4aa317 using evolve by test (Thu Jan 01 00:00:00 1970 +0000)
  |
  x  77ccbf8d837e (6) c_F
       rewritten(parent) as 8ae8db670b4a using rebase by test (Thu Jan 01 00:00:00 1970 +0000)
       rewritten(parent) as a52ac76b45f5 using rebase by test (Thu Jan 01 00:00:00 1970 +0000)
  

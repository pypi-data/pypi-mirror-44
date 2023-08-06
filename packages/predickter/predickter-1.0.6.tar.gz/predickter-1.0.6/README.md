# predickter

A Python package, to get live scores, live commentary and scorecards.

<b>Instllation</b>
<code>
pip install predickter
</code>

<b>Basic Usage</b>

Import the predickter library.

```python
from predickter import Precrickter
p=Precrickter()
```

#
print(p.liveScore('20212'))
#

print(p.get_test_rankings())

<b>Get all the matches(live,upcoming and recently finished matches)</b>
```python
   print(p.livematches())
```

Each match will have an attribute 'id'. Use this 'id' to get matchinfo, scorecard, brief score and commentary of matches.

<b>Get information about a match</b>

```
print (p.matchdetails('20212'))
```

<b>Get brief score of a match</b>

```python
print (p.liveScore('20212'))
```

<b>Get scorecard of a match</b>

```python
print(p.scoreboard('20212'))
```
<b>Get live commentary </b>
```
print(p.livecommentary('20212'))
```




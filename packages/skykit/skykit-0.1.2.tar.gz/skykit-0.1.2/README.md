# Sky kit

Out-of-the-box satellite imagery processing.

Adding **fun** to satellites coolness 😎

> Warning: This is still a work in progress. Please do not use in production, yet.

## Seriously, what is it? 🧐

Sky kit is an ensemble of methods to ease satellite imagery processing to developers and data scientists. Working with any satellite providers, should be as easy as:

```python
from skykit.providers import ProviderName
```

## Install 🚀

As with any python package, **pip** is your friend:

```
pip install skykit
```

## Usage 🎡

### Quick Start

The following code download tiles of Sentinel-1 satellite that includes Paris (France), from 01/03/2019 to 08/03/2019:

```python
from datetime import date
from skykit.providers import Sentinel

sat = Sentinel(username="xxx", password="yyy")
# Add source="Sentinel-2" if you want to query Sentine-2
# Not specifying a source will default to Sentinel-1

tiles = sat.query(
    coordinates=(2.349014, 48.864716), # Paris (FR) coordinates
    dates=(date(2019,3,1), date(2019,3,8))
    )

len(tiles) # returns 12

sat.download(tiles) # Tiles will be grouped in a .zip file
```

In the previous example, the `tiles` variable will include meta information of every tile returned from Sentinel-1 query.

## Todo 🔭

- [ ] Add Landsat provider
- [ ] Create `Tile` class to create a uniform use of tiles, no matter which provider
- [ ] Ease working with tiles meta data
- [ ] Allow querying using a polygon
- [ ] Allow querying using an address
- [ ] Use friendly dates (like text: `"26/03/2019"`), of use `from="..."` and `to="..."` instead of `date=(...)`
- [ ] Allow working on specific bands. Something like:

```python
tile = tiles[0]
image = tile.get('b04') # or tile.b04() ???
```

- [ ] What about tests? Seriously! <-- ⚠ URGENT

This list is not exhaustive.

## Contribution 💪

Please suggest contributions using Github's **Pull Requests**.

## License 🤮

Read the [LICENSE.txt](LICENSE.txt) file.

Thanks 🙏

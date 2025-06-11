# SOTAFreq
SOTA frequencies assigment

This repo tries to solve the problem of several concurrent in time line of sight (LOS) VHF activations, proposing free frequencies for each activator.

## Available frequencies

We propose leaving free 145.500 (calling frequency) so any amateur radio operator, activity participant or not, could use it as meeting point.

It would be great having a list of known local used frequencies for each zone.

## LOS calculus

First aproximation: `LOS iif d ≤ 250 km`.


## Maximum Distance Between Reused Frequencies Algorithm

1. Compute how many reused frequencies would be needed.
1. Compute distances between summits.
1. Calculate summit score coefficient (SSC) for each pairs.
1. Order set of pairs by SSC.
1. Assign the same frequency to each pair element until there is enough free frequencies.

### SSC calculus
`SSC = distance * (1 - ((summit_points1 + summit_points2)/100)

## Minimun distance algorithm

1. Choose the highest summit.
1. Compute list of LOS summits.
1. Warn if cardinality is greater than available frequencies.
1. Assign frequencies.
1. Choose next highest non-assignated summit.
1. Compute list of LOS summits.
1. List free frequencies.
1. Warn if cardinality of non-freq-assigned summits are greater than free frequencies.
1. Assigin frequencies
1. Repeat until all summits have frequencies assigned.


## Frequency assign algorithm

1. Retrieve all summits data from [SOTA API](https://api2.sota.org.uk/docs/index.html) (lat, lon, altitude, name, points).
1. Calculate «mass center» of summits without frequency assigned.
1. Calculate summit fit coefficient (SFC) for each one.
1. Order by SFC.
1. Choose highest SFC summit without frequency assigned summit, it will be for now HLS (highest local summit).
1. Assign center frequency (CF) for HLS, indicating hightest local summit (sic).
1. Build set of LOS summits around HLS, ordered by altitude: that's the current local summits set (LSS).
1. Build set of local free frequencies (LFF), given free frequencies list minus know local used frequencies.
1. Assign `CF ± i*50 KHz, i ∈ ℕ` frequency for each one of LSS without frequency assigned.
1. If there are no more LFF, assign `CF ± i*25 KHz, i ∈ { 2n - 1 | n ∈ N }`
1. If there are no more LFF, assign `CF ± i*12.5 KHz, i ∈ { 2n − 1 | n ∈ N }`
1. If there are no more LFF, skip summit (for now).
1. While exists summits without frequency, go to point 5.

### SFC calculus

`SFC = altitude (in meters) - distance_to_mass_center (in Km) * 6.378`


## Summit suggestion

Given the list of first choosen summits and the list of all activable summits, suggest not-covered zones.

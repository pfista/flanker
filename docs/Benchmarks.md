## Benchmarks

Below is a comparison between the default Python MIME parser and
`flanker.mime` in Time, Memory, and Function calls as well as other
benchmarks relating to Flanker performance.

### Test Specification:

* 2x Intel Core i7-3520M CPU @ 2.90GHz
* 2 GB RAM
* Results were averaged over 50 runs

#### Time

Full Message:

| File Size | `email.parser` (seconds) | `flanker.mime` (seconds) | Speedup |
| --------- | ------------------------ | ------------------------ | ------- |
| 11 MB     | 0.601                    | 0.073                    | 8x      |
| 1.8 MB    | 0.113                    | 0.011                    | 10x     |
| 16 KB     | 0.001                    | 0.003                    | 0.33x   |

Headers Only:

| File Size | `email.parser` (seconds) | `flanker.mime` (seconds) | Speedup |
| --------- | ------------------------ | ------------------------ | ------- |
| 11 MB     | 0.601                    | 0.029                    | 20x     |
| 1.8 MB    | 0.113                    | 0.009                    | 12x     |
| 16 KB     | 0.001                    | 0.002                    | 0.5x    |


#### Peak Memory Usage (including interpreter)

Full Message:

| File Size | `email.parser` (MB) | `flanker.mime` (MB) | Memory Difference |
| --------- | ------------------- | ------------------- | ----------------- |
| 11 MB     | 59.51               | 46.27               | 0.77x             |
| 1.8 MB    | 30.55               | 28.52               | 0.93x             |
| 16 KB     | 28.45               | 28.51               | 0x                |

Headers Only:

| File Size | `email.parser` (MB) | `flanker.mime` (MB) | Memory Difference |
| --------- | ------------------- | ------------------- | ----------------- |
| 11 MB     | 59.51               | 28.07               | 0.47x             |
| 1.8 MB    | 30.55               | 28.52               | 0.93x             |
| 16 KB     | 28.45               | 28.52               | 0x                |


#### Function Calls

Full Message:

| File Size | `email.parser` (#) | `flanker.mime` (#) | Speedup |
| --------- | ------------------ | ------------------ | ------- |
| 11 MB     | 914,741            | 2,011              | 454x    |
| 1.8 MB    | 195,062            | 11,046             | 17x     |
| 16 KB     | 3,216              | 3,5842             | -1.1x   |

Headers Only:

| File Size | `email.parser` (#) | `flanker.mime` (#) | Speedup |
| --------- | ------------------ | ------------------ | ------- |
| 11 MB     | 914,741            | 1,253              | 730x    |
| 1.8 MB    | 195,062            | 9,741              | 20x     |
| 16 KB     | 3,216              | 2,476              | 1.2x    |


#### Pinned Regex 

Even though `master` does not use a pinned version of regex, we strongly recommend
due to the 6x speedup compared to the latest version on PyPi (as of 4/15/14). It may
not be an issue for someone that handles many small files, but is an issue for large
files.

| File Size | `regex.1.20110315` (seconds) | `regex 2014.04.10` (seconds) | Speedup |
| --------- | ---------------------------- | ---------------------------- | ------- |
| [11 MB](https://github.com/mailgun/flanker/blob/master/tests/fixtures/messages/big.eml) | 0.0720 | 0.4652 | 6x |

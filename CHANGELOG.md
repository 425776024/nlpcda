# Changelog

## 2.5.9 - 2026-10-30

### Fixed

- Preserve the final token in `RandomDeleteChar`, including protected trailing numbers.
- Treat `change_rate=0` as a no-op in all six rule-based augmenters; validate counts,
  rates and character-exchange windows, and bound retries for tiny change rates.
- Give each augmenter its own random generator and Jieba tokenizer. Constructing or
  using one instance no longer changes the application's random state or another
  instance's user dictionary. Seeded output can differ from earlier releases.
- Preserve the exact input as the first result, including newlines and surrounding
  whitespace. `create_num` remains the maximum total result count, including that input.
- Read custom dictionaries with blank lines and whitespace separators, support custom
  synonym group IDs, and add entity dictionaries to the instance's tokenizer.
- Allow entity replacement in short inputs, including a single entity.
- Parse blank-line-separated BIO sentences and CRLF files, regenerate labels after
  length-changing entity replacement, report invalid BIO records with file/line
  details, and handle entity pools with no alternative without assertion failures.
- Keep BIO sentences separate and return unique changed variants per sentence;
  `augument_size` remains an upper bound, not a guarantee.
- Load SimBERT dependencies only when constructing `Simbert`. Importing the package
  or using rule-based augmentation no longer attempts to import a model backend.
- Avoid mutating a caller's SimBERT configuration and allow omitted CUDA settings.
- Use HTTPS and a configurable timeout for Baidu translation, preserve multi-line
  results, and report service errors explicitly.

### Packaging and validation

- Align package/version metadata, declare Python >=3.8, align the license metadata
  with the existing Apache-2.0 license, and build both wheels and source archives.
- Update base dependency constraints and remove committed generated egg metadata.
- Add regression tests and CI for supported Python versions and major operating
  systems, including tests against the installed wheel outside the source tree.
- SimBERT model inference and live Baidu translation require external resources;
  regression tests cover their integration boundaries without downloading models or
  making paid translation requests.

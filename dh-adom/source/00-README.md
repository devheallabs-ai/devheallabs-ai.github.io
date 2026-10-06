# DH-ADOM publication package 1.1.0

DevHeal Hierarchical Agent Development & Orchestration Model.
Canonical URL: https://devheallabs.com/dh-adom/

## Versions

- White paper: editorial edition 1.1, 7 October 2026.
- Technical specification and Python reference implementation: 1.0.
- Publication package: 1.1.0.

## Contents

01-White-Paper contains the revised PDF, text source and ordered publication data.
02-Specification contains normative text, schemas, lifecycle models and API outline.
03-Reference-Templates contains the role and delegation templates.
04-Reference-Implementation contains Python source, tests, demo and its Apache-2.0 terms.
05-Conformance-Validation-Suite contains file-presence checks and a source-review coverage map.
06-Benchmarks-Experiments contains a protocol and task catalog, not comparative results.
07-Architecture-Diagrams contains vector figures and diagram source material.
08-Research-Publications contains related work and bibliography.
09-Version-History records changes and research direction.
11-Licensing-and-Citation contains publication terms and citation metadata.

## Run the example

Use Python 3.11 or later. From 04-Reference-Implementation:

    python -m unittest discover -s tests -v
    python -m examples.demo

From the package root:

    python 05-Conformance-Validation-Suite/run-validation.py

The latter checks seven files. It does not certify all normative requirements.

## Adoption

https://devheallabs.com/dh-adom/adoption/
https://devheallabs.com/dh-adom/conformance/

Review component licenses before reuse. Publication materials retain research-and-evaluation terms; the reference code has a separate Apache-2.0 license.

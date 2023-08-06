- wrap uuid in tools-based module

- LOOK INTO: call_args -> Message becomes dict ?

- PERSISTING: keep shadow copy, to avoid redundant writes to mongo

- speed test
  - expose timing parameters are parameters

- create more tests
  - test exceptions
    - test with badly formatted messages
      - e.g. without id in tags

- stress test, break things
- check combinations (order of constructors)

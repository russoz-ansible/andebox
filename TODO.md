TO-DO
=====

## feat

* add extra dependencies (vagrant, tox-test) and make actions with unfulfilled deps unavailable
* add parameters validations to `test` action, for example:
  * `test -ei` is only valid for `sanity`
  * requirement params are only valid for `integration` and `units`
* make action accept aliases (units, unit)

## fix

## build

## chore

* add pre-commit for
  * licenses (not ready for that yet)

## ci

* make a scheduled CI run testing a lot of stuff, like all unit tests of c.g., or all integration tests of c.crypto

## docs

## style

## refactor

## perf

## test

* add tests for actions:
  * toxtest
  * vagrant

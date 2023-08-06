# /usr/bin/env python

# This file is part of error404.

# error404 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# error404 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with error404.  If not, see <http://www.gnu.org/licenses/>.

from error404 import config


def test_results():
    """Overview of test results.

    Provides extended information about how successful the tests were
    Outputted once all tests are complete

    If run explicitly, results are only returned if more than one test was run

    Returns:
        exit(1) if any test fails
    """
    if (
        config.total_tests != 0
    ):  # Output only if tests were run (or always if in interactive)
        func_time = round(config.total_time, 4)
        print("\n" * 2)
        if config.number_failed == 0:
            print(
                "Out of {0} tests, all succeeded in {1} seconds".format(
                    config.total_tests, func_time
                )
            )
        elif config.number_success == 0:
            print(
                "Out of {0} tests, all failed in {1} seconds".format(
                    config.total_tests, func_time
                )
            )
            exit(1)
        # If some tests failed and others succeeded
        else:
            print(
                "Out of {0} tests, {1} succeeded and {2} failed in {3} seconds".format(
                    config.total_tests,
                    config.number_success,
                    config.number_failed,
                    func_time,
                )
            )
            success_rate = (config.number_success / config.total_tests) * 100
            # Success rate rounded to 2 d.p.
            print("This gives a success rate of {0}%".format(round(success_rate, 2)))
            exit(1)


def clear_results():
    """Clears total test successes/failures

    Does not return any values
    """
    config.number_success = (
        config.number_failed
    ) = config.total_tests = config.total_time = config.current_test = 0

    config.func_counter = {"name": None, "counter": 1}

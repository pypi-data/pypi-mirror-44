from __future__ import print_function, absolute_import

import pytest

from .options import JuliaOptions

_USING_DEFAULT_SETUP = True


def pytest_addoption(parser):
    import os

    # Note: the help strings have to be synchronized manually with
    # ../../docs/source/pytest.rst

    parser.addoption(
        "--no-julia",
        action="store_false",
        dest="julia",
        help="Skip tests that require julia.",
    )
    parser.addoption(
        "--julia-runtime",
        help="""
        Julia executable to be used.  Defaults to environment variable
        `$PYJULIA_TEST_RUNTIME`.
        """,
        default=os.getenv("PYJULIA_TEST_RUNTIME", "julia"),
    )

    for desc in JuliaOptions.supported_options():
        parser.addoption(
            "--julia-{}".format(desc.cli_argument_name().lstrip("-")),
            **desc.cli_argument_spec()
        )


def pytest_sessionstart(session):
    if not session.config.getoption("julia"):
        return

    from .core import LibJulia, JuliaInfo, Julia, enable_debug

    options = JuliaOptions()
    for desc in JuliaOptions.supported_options():
        cli_option = "--julia-{}".format(desc.cli_argument_name().lstrip("-"))
        desc.__set__(options, session.config.getoption(cli_option))

    julia_runtime = session.config.getoption("julia_runtime")

    global _USING_DEFAULT_SETUP
    _USING_DEFAULT_SETUP = not (julia_runtime != "julia" or options.as_args())

    enable_debug()
    global _JULIA_INFO
    _JULIA_INFO = info = JuliaInfo.load(julia=julia_runtime)
    if (info.version_major, info.version_minor) < (0, 7):
        # In Julia 0.6, we have to load PyCall.jl here to do the
        # fake-julia setup.
        Julia(runtime=julia_runtime)
    else:
        api = LibJulia.from_juliainfo(info)
        api.init_julia(options)


# Initialize Julia runtime as soon as possible (or more precisely
# before importing any additional Python modules) to avoid, e.g.,
# incompatibility of `libstdc++`.
#
# See:
# https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_sessionstart


@pytest.fixture(scope="session")
def julia(request):
    """ pytest fixture for providing a `Julia` instance. """
    if not request.config.getoption("julia"):
        pytest.skip("--no-julia is given.")

    from .core import Julia

    return Julia()


@pytest.fixture(scope="session")
def juliainfo(julia):
    """ pytest fixture for providing `JuliaInfo` instance. """
    return _JULIA_INFO


def pytest_runtest_setup(item):
    if not item.config.getoption("julia"):
        for mark in item.iter_markers("julia"):
            pytest.skip("--no-julia is given.")

    if not (item.config.getoption("julia") and _USING_DEFAULT_SETUP):
        for mark in item.iter_markers("pyjulia__using_default_setup"):
            pytest.skip(
                "using non-default setup (e.g., --julia-<julia_option> is given)"
            )

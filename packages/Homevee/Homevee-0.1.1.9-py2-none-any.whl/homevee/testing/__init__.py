from homevee.Helper import Logger
from homevee.testing import benchmark
from homevee.testing.test_voice_assistant import run_voice_tests


def run_tests():
    print("running tests...")
    #run_benchmarks
    #benchmark.do_benchmarks()

    Logger.IS_DEBUG = False

    run_voice_tests()

if __name__ == "__main__":
    run_tests()
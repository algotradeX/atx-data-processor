from dynaconf import settings


def line_profiler():
    profiler = None
    try:
        if settings.PROFILER["line-profiler"]:
            import pprofile

            if settings.PROFILER["line-profiler-type"] == "deterministic":
                profiler = pprofile.Profile()
            elif settings.PROFILER["line-profiler-type"] == "statistic":
                prof = pprofile.StatisticalProfile()
                profiler = prof(
                    period=0.001,  # Sample every 1ms
                    single=True,  # Only sample current thread
                )
    except ImportError:
        print("Unable to create line_profiler : ImportError")
    except Exception as e:
        print("Unable to create line_profiler : " + str(e))
    return profiler

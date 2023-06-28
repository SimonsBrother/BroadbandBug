import broadbandbug.library.constants as consts
import broadbandbug.methods.speedtestcli as speedtestcli

import speedtest


def determineMethodFunction(method_name):
    # Get function related to method
    if method_name == consts.METHOD_SPEEDTESTCLI:  # speedtest cli method
        # Assign method function
        function = speedtestcli.performSpeedTest

        # Generate new speedtest object, and store it in tuple to be passed as parameters
        speedtest_obj = speedtest.Speedtest()
        speedtest_obj.get_best_server()
        params = (speedtest_obj,)

        return function, params

    elif method_name == consts.METHOD_BTWEBSITE:  # bt website method
        # Assign method function
        function = speedtestcli.performSpeedTest

        # Generate new speedtest object, and store it in tuple to be passed as parameters
        speedtest_obj = speedtest.Speedtest()
        speedtest_obj.get_best_server()
        params = (speedtest_obj,)

        return function, params

    else:
        return None

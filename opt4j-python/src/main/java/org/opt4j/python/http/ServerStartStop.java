package org.opt4j.python.http;

import java.io.IOException;

import org.opt4j.core.optimizer.Optimizer;
import org.opt4j.core.optimizer.OptimizerStateListener;

public class ServerStartStop implements OptimizerStateListener {

	private final String RELATIVE_URL_START = "/start";
	private final String expectedResponseStart = "good to go";
	private final String RELATIVE_ULR_STOP = "/terminate";
	private final String expectedResponseStop = "server terminated";

	@Override
	public void optimizationStarted(Optimizer optimizer) {
		// TODO Right now, we just make a get request for the startup. Later, we
		// will have to initialize all used predictors based on the Optimization
		// process.
		String serverResponse = null;
		try {
			serverResponse = RequestHandler.sendGetRequest(RELATIVE_URL_START);
		} catch (IOException ioExc) {
			ioExc.printStackTrace();
			throw new IllegalStateException("Problem during server init: IOException");
		}
		assert serverResponse != null;
		if (!serverResponse.equals(expectedResponseStart)) {
			throw new IllegalArgumentException("Problem during server init: Wrong server response");
		}
	}

	@Override
	public void optimizationStopped(Optimizer optimizer) {
		// Terminate the python server
		String serverResponse = null;
		try {
			serverResponse = RequestHandler.sendGetRequest(RELATIVE_ULR_STOP);
		} catch (IOException ioExc) {
			throw new IllegalStateException("Problem during server shutdown: IOException");
		}
		assert serverResponse != null;
		if (!serverResponse.equals(expectedResponseStop)) {
			throw new IllegalArgumentException("Problem during server init: Wrong server response");
		}
	}
}

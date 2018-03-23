package org.opt4j.python.http;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.HttpClientBuilder;

/**
 * Class to handle the HTTP requests
 * 
 * @author Fedor Smirnov
 *
 */
public class RequestHandler {
	
	private static final String PYTHON_SERVER_URL = "http://127.0.0.1:5000/";
	
	/**
	 * Makes a get request to the provided URL and returns the response as a string. 
	 * 
	 * @param requestUrl
	 * @return
	 */
	public static String sendGetRequest(String relativeUrlPath) throws ClientProtocolException, IOException{
		// make the request
		String requestUrl = PYTHON_SERVER_URL + relativeUrlPath;
		HttpClient client = HttpClientBuilder.create().build();
		HttpGet request = new HttpGet(requestUrl);
		// get the response
		HttpResponse response = client.execute(request);
		return responseToString(response);
	}
	
	/**
	 * Makes a json post request to the specified url
	 * 
	 * @param jsonString : the json object in string form  
	 * @param requestUrl : the url to make the request to
	 * @return : the server response
	 */
	public static String sendJsonPostRequest(String jsonString, String relativeUrlPath) throws ClientProtocolException, IOException{
		// make the string entity
		StringEntity requestEntity = new StringEntity(jsonString, ContentType.APPLICATION_JSON);
		// make the request
		String requestUrl = PYTHON_SERVER_URL + relativeUrlPath;
		HttpClient httpClient = HttpClientBuilder.create().build();
		HttpPost postMethod = new HttpPost(requestUrl);
		postMethod.setEntity(requestEntity);
		// execute the request 
		HttpResponse response = httpClient.execute(postMethod);
		return responseToString(response);
	}
	
	/**
	 * Reads the response and returns a string
	 * 
	 * @param response
	 * @return
	 */
	private static String responseToString(HttpResponse response) throws IOException{
		StringBuffer result = new StringBuffer();
		BufferedReader rd = new BufferedReader(new InputStreamReader(response.getEntity().getContent()));
		String line = "";
		while ((line = rd.readLine()) != null){
			result.append(line);
		}
		return result.toString();
	}
}

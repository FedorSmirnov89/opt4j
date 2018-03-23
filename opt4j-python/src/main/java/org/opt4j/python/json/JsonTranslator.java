package org.opt4j.python.json;

import com.google.gson.Gson;

public class JsonTranslator {
	
	/**
	 * Converts the given object to a json-string
	 * 
	 * @param obj
	 * @return
	 */
	public static String objToJsonString(Object obj){
		Gson gson = new Gson();
		return gson.toJson(obj);
	}
	

}

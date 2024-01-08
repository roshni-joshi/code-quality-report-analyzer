package code.quality.analyzer.model;

import java.util.Map;

/**
 * Request object to call python trend analysis service
 */
public class TrendAnalysisRequest extends AnalysisServiceRequest {
	private Map<String, String> commitsData;
	private Map<String, String> previousCommit;
	public Map<String, String> getCommitsData() {
		return commitsData;
	}
	public void setCommitsData(Map<String, String> commitsData) {
		this.commitsData = commitsData;
	}
	public Map<String, String> getPreviousCommit() {
		return previousCommit;
	}
	public void setPreviousCommit(Map<String, String> previousCommit) {
		this.previousCommit = previousCommit;
	}
}

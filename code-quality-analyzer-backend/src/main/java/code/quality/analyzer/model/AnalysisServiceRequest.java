package code.quality.analyzer.model;

/**
 * Super class for analysis service request
 */
public class AnalysisServiceRequest {
	private String reportPath;
	public String getReportPath() {
		return reportPath;
	}
	public void setReportPath(String reportPath) {
		this.reportPath = reportPath;
	}
}

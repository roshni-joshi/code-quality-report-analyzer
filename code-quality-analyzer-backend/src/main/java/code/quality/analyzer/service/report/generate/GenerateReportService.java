package code.quality.analyzer.service.report.generate;

import code.quality.analyzer.model.AnalysisServiceRequest;
import code.quality.analyzer.model.CommitAnalysisRequest;

public interface GenerateReportService {
 
	/**
	 * Generate reports for one commit analysis
	 * @param commitAnalysisRequest commits request data
	 * @return one commit analysis service request object
	 * @throws Exception
	 */
	AnalysisServiceRequest generateOneCommitReport(CommitAnalysisRequest commitAnalysisRequest) throws Exception;
	
	/**
	 * Generate reports for trend analysis
	 * @param commitAnalysisRequest commits request data
	 * @return trend analysis service request object
	 * @throws Exception
	 */
	AnalysisServiceRequest generateTrendAnalysisReport(CommitAnalysisRequest commitAnalysisRequest) throws Exception;

	/**
	 * Generate reports for hotspot analysis
	 * @param commitAnalysisRequest commits request data
	 * @return hotspot analysis service request object
	 * @throws Exception
	 */
	AnalysisServiceRequest generateHotspotReport(CommitAnalysisRequest commitAnalysisRequest) throws Exception;
}

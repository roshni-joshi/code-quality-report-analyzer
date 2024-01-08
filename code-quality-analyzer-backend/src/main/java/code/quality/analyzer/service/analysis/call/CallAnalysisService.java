package code.quality.analyzer.service.analysis.call;

import code.quality.analyzer.model.HotspotAnalysisRequest;
import code.quality.analyzer.model.OneCommitAnalysisRequest;
import code.quality.analyzer.model.TrendAnalysisRequest;

public interface CallAnalysisService {

	/**
	 * Call one commit analysis python service
	 * @param request object for one commit analysis call
	 * @return reports path
	 */
	String callOneCommitAnalysisService(OneCommitAnalysisRequest request);
	
	/**
	 * Call trend analysis python service
	 * @param request object for trend analysis call
	 * @return
	 */
	String callTrendAnalysisService(TrendAnalysisRequest request);
	
	/**
	 * Call hotspot analysis python service
	 * @param request object for hotspot analysis call
	 * @return
	 */
	String callHotspotAnalysisService(HotspotAnalysisRequest request);
}

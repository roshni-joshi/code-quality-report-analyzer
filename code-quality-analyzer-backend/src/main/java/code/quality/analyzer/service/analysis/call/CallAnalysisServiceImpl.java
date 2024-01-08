package code.quality.analyzer.service.analysis.call;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import code.quality.analyzer.model.HotspotAnalysisRequest;
import code.quality.analyzer.model.OneCommitAnalysisRequest;
import code.quality.analyzer.model.TrendAnalysisRequest;

@Service
public class CallAnalysisServiceImpl implements CallAnalysisService {

	private static Logger logger = LogManager.getLogger(CallAnalysisServiceImpl.class);

	@Value("${analysis.service.base.url}")
	private String baseUrl;
	
	@Value("${analysis.service.one.commit.url}")
	private String oneCommitUrl;
	
	@Value("${analysis.service.trend.url}")
	private String trendUrl;
	
	@Value("${analysis.service.hotspot.url}")
	private String hotspotUrl;
	
	@Override
	public String callOneCommitAnalysisService(OneCommitAnalysisRequest request) {
		logger.info("BEGIN callAnalysisServiceOneCommit()");
		RestTemplate restTemplate = new RestTemplate();
		HttpEntity<OneCommitAnalysisRequest> httpRequest = new HttpEntity<>(request);
		ResponseEntity<String> response = restTemplate
				.exchange(baseUrl + oneCommitUrl, HttpMethod.POST, httpRequest, String.class);

		return response.getBody();
	}

	@Override
	public String callTrendAnalysisService(TrendAnalysisRequest request) {
		logger.info("BEGIN callAnalysisServiceTrend()");
		RestTemplate restTemplate = new RestTemplate();
		HttpEntity<TrendAnalysisRequest> httpRequest = new HttpEntity<>(request);
		ResponseEntity<String> response = restTemplate
				.exchange(baseUrl + trendUrl, HttpMethod.POST, httpRequest, String.class);
		return response.getBody();
	}

	@Override
	public String callHotspotAnalysisService(HotspotAnalysisRequest request) {
		logger.info("BEGIN callAnalysisServiceHotspot()");
		RestTemplate restTemplate = new RestTemplate();
		HttpEntity<HotspotAnalysisRequest> httpRequest = new HttpEntity<>(request);
		ResponseEntity<String> response = restTemplate
				.exchange(baseUrl + hotspotUrl, HttpMethod.POST, httpRequest, String.class);
		return response.getBody();
	}
}

package code.quality.analyzer.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import code.quality.analyzer.model.CommitAnalysisRequest;
import code.quality.analyzer.model.HotspotAnalysisRequest;
import code.quality.analyzer.model.OneCommitAnalysisRequest;
import code.quality.analyzer.model.TrendAnalysisRequest;
import code.quality.analyzer.service.analysis.call.CallAnalysisService;
import code.quality.analyzer.service.report.generate.GenerateReportService;

@RestController
@CrossOrigin(origins = {"http://localhost:3000", "http://csci5308vm3.research.cs.dal.ca"})
public class CommitsAnalysisController {
	
	@Autowired
	GenerateReportService reportService;
	
	@Autowired
	CallAnalysisService callAnalysisService;
	
	@PostMapping("/onecommit/getanalysis")
	ResponseEntity<String> getOneCommitAnalysis(@RequestBody CommitAnalysisRequest commitsRequest) throws Exception {
		OneCommitAnalysisRequest request = (OneCommitAnalysisRequest) reportService.generateOneCommitReport(commitsRequest);
		String jsonOutput = callAnalysisService.callOneCommitAnalysisService(request);
		return new ResponseEntity<String>(jsonOutput, HttpStatus.OK);
	}
	
	@PostMapping("/trend/getanalysis")
	ResponseEntity<String> getTrendAnalysis(@RequestBody CommitAnalysisRequest commitsRequest) throws Exception {
		TrendAnalysisRequest request = (TrendAnalysisRequest) reportService.generateTrendAnalysisReport(commitsRequest);
		String jsonOutput = callAnalysisService.callTrendAnalysisService(request);
		return new ResponseEntity<String>(jsonOutput, HttpStatus.OK);
	}
	
	@PostMapping("/hotspot/getanalysis")
	ResponseEntity<String> getHotspotAnalysis(@RequestBody CommitAnalysisRequest commitsRequest) throws Exception {
		HotspotAnalysisRequest request = (HotspotAnalysisRequest) reportService.generateHotspotReport(commitsRequest);
		String jsonOutput = callAnalysisService.callHotspotAnalysisService(request);
		return new ResponseEntity<String>(jsonOutput, HttpStatus.OK);
	}
}

package code.quality.analyzer.controller;

import static code.quality.analyzer.util.Constants.*;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import com.fasterxml.jackson.databind.ObjectMapper;

import code.quality.analyzer.model.CommitAnalysisRequest;
import code.quality.analyzer.model.HotspotAnalysisRequest;
import code.quality.analyzer.model.OneCommitAnalysisRequest;
import code.quality.analyzer.model.TrendAnalysisRequest;
import code.quality.analyzer.service.analysis.call.CallAnalysisService;
import code.quality.analyzer.service.report.generate.GenerateReportService;

/**
 * Test OneCommitAnalysisController rest services
 */
@WebMvcTest
@ExtendWith(MockitoExtension.class)
public class CommitsAnalysisControllerTest {

	@InjectMocks
	CommitsAnalysisController commitsAnalysisController;
	
	@Autowired
	GenerateReportService reportService;
	
	@Autowired
	@Mock CallAnalysisService analysisService;
	
	CommitAnalysisRequest commitAnalysisRequest;
	MockMvc mockMvc;
	
	@BeforeEach
	void setUp() {
		ReflectionTestUtils.setField(commitsAnalysisController, "reportService", reportService);
		commitAnalysisRequest = new CommitAnalysisRequest();
		commitAnalysisRequest.setGitRepoLink(REPO_URL);
		commitAnalysisRequest.setBranch(BRANCH);
		mockMvc = MockMvcBuilders.standaloneSetup(commitsAnalysisController).build();
	}
	
	@Test
	void testGetOneCommitAnalysis() throws Exception {
		when(analysisService.callOneCommitAnalysisService(any(OneCommitAnalysisRequest.class))).thenReturn(ANALYSIS_RESPONSE);
		callServiceAndTest(ONE_COMMIT_URL);
	}
	
	@Test
	void testGetTrendAnalysis() throws Exception {
		commitAnalysisRequest.setNoOfCommits(TOTAL_COMMITS_2);
		when(analysisService.callTrendAnalysisService(any(TrendAnalysisRequest.class))).thenReturn(ANALYSIS_RESPONSE);
		callServiceAndTest(TREND_URL);
	}
	
	@Test
	void testGetOneCommitAnalysisForRemoteBranch() throws Exception {
		commitAnalysisRequest.setBranch(REMOTE_BRANCH);
		when(analysisService.callOneCommitAnalysisService(any(OneCommitAnalysisRequest.class))).thenReturn(ANALYSIS_RESPONSE);
		callServiceAndTest(ONE_COMMIT_URL);
	}
	
	@Test
	void testGetTrendAnalysisForRemoteBranch() throws Exception {
		commitAnalysisRequest.setBranch(REMOTE_BRANCH);
		commitAnalysisRequest.setNoOfCommits(TOTAL_COMMITS_2);
		when(analysisService.callTrendAnalysisService(any(TrendAnalysisRequest.class))).thenReturn(ANALYSIS_RESPONSE);
		callServiceAndTest(TREND_URL);
	}
	
	@Test
	void testGetHotspotAnalysis() throws Exception {
		when(analysisService.callHotspotAnalysisService(any(HotspotAnalysisRequest.class))).thenReturn(ANALYSIS_RESPONSE);
		callServiceAndTest(HOTSPOT_URL);
	}
	
	public void callServiceAndTest(String url) throws Exception {
		MvcResult mvcResult = mockMvc.perform(MockMvcRequestBuilders.post(url)
				.contentType(MediaType.APPLICATION_JSON)
				.content(new ObjectMapper().writeValueAsString(commitAnalysisRequest)))
				.andExpect(MockMvcResultMatchers.status().isOk())
				.andReturn();
		String response = mvcResult.getResponse().getContentAsString();
		assertEquals(ANALYSIS_RESPONSE, response);
	}
}

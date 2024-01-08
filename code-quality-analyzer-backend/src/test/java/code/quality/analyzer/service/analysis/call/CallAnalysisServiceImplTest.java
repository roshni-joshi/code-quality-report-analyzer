package code.quality.analyzer.service.analysis.call;

import static code.quality.analyzer.util.Constants.*;
import static com.github.tomakehurst.wiremock.client.WireMock.aResponse;
import static com.github.tomakehurst.wiremock.client.WireMock.post;
import static com.github.tomakehurst.wiremock.client.WireMock.stubFor;
import static com.github.tomakehurst.wiremock.client.WireMock.urlEqualTo;
import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.util.ReflectionTestUtils;

import com.github.tomakehurst.wiremock.WireMockServer;
import com.github.tomakehurst.wiremock.client.ResponseDefinitionBuilder;
import com.github.tomakehurst.wiremock.client.WireMock;
import com.github.tomakehurst.wiremock.core.WireMockConfiguration;

import code.quality.analyzer.model.HotspotAnalysisRequest;
import code.quality.analyzer.model.OneCommitAnalysisRequest;
import code.quality.analyzer.model.TrendAnalysisRequest;

/**
 * Test CallAnalysisServiceImpl class methods
 */
@SpringBootTest
@ExtendWith(MockitoExtension.class)
@TestPropertySource("classpath:application.properties")
class CallAnalysisServiceImplTest {
    private static CallAnalysisService analysisService;
    ResponseDefinitionBuilder builder;

    @Autowired
    private static WireMockServer wireMockServer;

    @Value("${analysis.service.base.url}")
	private String baseUrl;

	@Value("${analysis.service.one.commit.url}")
	private String oneCommitUrl;

	@Value("${analysis.service.trend.url}")
	private String trendUrl;
	
	@Value("${analysis.service.hotspot.url}")
	private String hotspotUrl;

    @BeforeEach
    void setUp() {
        analysisService = new CallAnalysisServiceImpl();
        ReflectionTestUtils.setField(analysisService, "baseUrl", baseUrl);
        ReflectionTestUtils.setField(analysisService, "oneCommitUrl", oneCommitUrl);
        ReflectionTestUtils.setField(analysisService, "trendUrl", trendUrl);
        ReflectionTestUtils.setField(analysisService, "hotspotUrl", hotspotUrl);
        builder = aResponse().withStatus(HTTP_STATUS).withHeader("Content-Type", "application/json").withBody(ANALYSIS_RESPONSE);
    }

    @Test
    void testCallAnalysisServiceOneCommit() throws Exception {
        wireMockServer = new WireMockServer(new WireMockConfiguration().port(PORT));
        wireMockServer.start();
        WireMock.configureFor(LOCALHOST, PORT);
        stubFor(post(urlEqualTo(oneCommitUrl)).willReturn(builder));
        String response = analysisService.callOneCommitAnalysisService(new OneCommitAnalysisRequest());
        assertEquals(ANALYSIS_RESPONSE, response);
        wireMockServer.stop();
    }

   @Test
    void testCallAnalysisServiceTrend() throws Exception {
        wireMockServer = new WireMockServer(new WireMockConfiguration().port(PORT));
        wireMockServer.start();
        WireMock.configureFor(LOCALHOST, PORT);
        stubFor(post(urlEqualTo(trendUrl)).willReturn(builder));
        String response = analysisService.callTrendAnalysisService(new TrendAnalysisRequest());
        assertEquals(ANALYSIS_RESPONSE, response);
        wireMockServer.stop();
    }
   
    @Test
    void testCallAnalysisServiceHotspot() throws Exception {
        wireMockServer = new WireMockServer(new WireMockConfiguration().port(PORT));
        wireMockServer.start();
        WireMock.configureFor(LOCALHOST, PORT);
        stubFor(post(urlEqualTo(hotspotUrl)).willReturn(builder));
        String response = analysisService.callHotspotAnalysisService(new HotspotAnalysisRequest());
        assertEquals(ANALYSIS_RESPONSE, response);
        wireMockServer.stop();
    }
}

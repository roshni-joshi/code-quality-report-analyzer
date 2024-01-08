package code.quality.analyzer.service.report.generate;

import static code.quality.analyzer.util.Constants.*;
import static org.junit.jupiter.api.Assertions.*;

import java.nio.file.Files;
import java.nio.file.Paths;

import org.eclipse.jgit.api.errors.InvalidRefNameException;
import org.eclipse.jgit.api.errors.RefNotFoundException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.TestPropertySource;

import code.quality.analyzer.exception.InvalidCommitsException;
import code.quality.analyzer.model.AnalysisServiceRequest;
import code.quality.analyzer.model.CommitAnalysisRequest;
import code.quality.analyzer.model.TrendAnalysisRequest;
import code.quality.analyzer.util.CommitsAnalysisUtil;

/**
 * Test GenerateReportServiceImpl class methods
 */
@SpringBootTest
@ExtendWith(MockitoExtension.class)
@TestPropertySource("classpath:application.properties")
class GenerateReportServiceImplTest {
    private static GenerateReportService reportService;
    private static String repoPath;
    CommitAnalysisRequest commitRequest;
    AnalysisServiceRequest request;

    @BeforeEach
    void setUp() {
        reportService = new GenerateReportServiceImpl();
        repoPath = CommitsAnalysisUtil.cloneRepository(REPO_URL);
        commitRequest = new CommitAnalysisRequest();
        commitRequest.setGitRepoLink(REPO_URL);
        commitRequest.setBranch(BRANCH);
        commitRequest.setCommitId(COMMIT1);
    }

    @Test
    void testGenerateOneCommitReport() throws Exception {
    	commitRequest.setCommitId(COMMIT2);
        request = reportService.generateOneCommitReport(commitRequest);
        assertTrue(Files.exists(Paths.get(request.getReportPath())));
    }
    
    @Test
    void testGenerateOneCommitReportForRemoteBranch() throws Exception {
    	commitRequest.setBranch(REMOTE_BRANCH);
    	commitRequest.setCommitId(REMOTE_COMMIT);
        request = reportService.generateOneCommitReport(commitRequest);
        assertTrue(Files.exists(Paths.get(request.getReportPath())));
    }

    @Test
    void testGenerateOneCommitReportExceptionWithInvalidBranch() throws Exception {
        commitRequest.setBranch("xyz");
        assertThrows(RefNotFoundException.class, () -> reportService.generateOneCommitReport(commitRequest));
    }

    @Test
    void testGenerateOneCommitReportExceptionWithWhitespaceBranch() throws Exception {
        commitRequest.setBranch(" ");
        assertThrows(InvalidRefNameException.class, () -> reportService.generateOneCommitReport(commitRequest));
    }

    @Test
    void testGenerateOneCommitReportExceptionWithNullBranch() throws Exception {
        commitRequest.setBranch(null);
        assertThrows(InvalidRefNameException.class, () -> reportService.generateOneCommitReport(commitRequest));
    }
   
    @Test
    void testGenerateTrendAnalysisReportCheckCommits() throws Exception {
    	commitRequest.setNoOfCommits(TOTAL_COMMITS_2);
    	TrendAnalysisRequest request = (TrendAnalysisRequest)reportService.generateTrendAnalysisReport(commitRequest);
    	assertEquals(TOTAL_COMMITS_2, request.getCommitsData().size());
    }

    @Test
    void testGenerateTrendAnalysisReportCheckUsers() throws Exception {
        commitRequest.setNoOfCommits(TOTAL_COMMITS_2);
        TrendAnalysisRequest request = (TrendAnalysisRequest)reportService.generateTrendAnalysisReport(commitRequest);
        assertEquals(USER2, request.getPreviousCommit().get(COMMIT3));
    }

    @Test
    void testGenerateTrendAnalysisReportForRemoteBranch() throws Exception {
    	commitRequest.setBranch(REMOTE_BRANCH);
    	commitRequest.setNoOfCommits(TOTAL_COMMITS_2);
    	TrendAnalysisRequest request = (TrendAnalysisRequest)reportService.generateTrendAnalysisReport(commitRequest);
    	assertEquals(TOTAL_COMMITS_2, request.getCommitsData().size());
    }
    
    @Test
    void testGenerateTrendAnalysisReportForAllCommitsCheckCommits() throws Exception {
    	repoPath = CommitsAnalysisUtil.cloneRepository(REPO_URL_ALLCOMMITS);
    	commitRequest.setGitRepoLink(REPO_URL_ALLCOMMITS);
    	commitRequest.setNoOfCommits(TOTAL_COMMITS_1);
    	TrendAnalysisRequest request = (TrendAnalysisRequest)reportService.generateTrendAnalysisReport(commitRequest);
    	assertEquals(TOTAL_COMMITS_1, request.getCommitsData().size());
    }

    @Test
    void testGenerateTrendAnalysisReportForAllCommitsCheckPreviousCommit() throws Exception {
        repoPath = CommitsAnalysisUtil.cloneRepository(REPO_URL_ALLCOMMITS);
        commitRequest.setGitRepoLink(REPO_URL_ALLCOMMITS);
        commitRequest.setNoOfCommits(TOTAL_COMMITS_1);
        TrendAnalysisRequest request = (TrendAnalysisRequest)reportService.generateTrendAnalysisReport(commitRequest);
        assertNull(request.getPreviousCommit());
    }

    @Test
    void testGenerateTrendAnalysisReportForZeroCommits() throws Exception {
    	commitRequest.setNoOfCommits(ZERO);
    	assertThrows(InvalidCommitsException.class, () -> reportService.generateTrendAnalysisReport(commitRequest));
    }

    @Test
    void testGenerateHotspotReport() throws Exception {
        request = reportService.generateHotspotReport(commitRequest);
        assertTrue(Files.exists(Paths.get(request.getReportPath())));
    }
}
